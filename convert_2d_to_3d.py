import json
from tqdm import tqdm
import tensorflow as tf
import pickle
import numpy as np
import os
import sys
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

cam = "CAMERA_"+sys.argv[1]

f = open("results/"+cam+"_results.bbox.json","r")
twoD = json.load(f)
f.close()

f = open("depth_results/"+cam+".json","r")
depth  = json.load(f)
f.close()


# Get conversion method
camera_model_module = tf.load_op_library('/home/harish_k_kamath/waymo-od-2/waymo-open-dataset/bazel-bin/third_party/camera/ops/camera_model_ops.so')
image_to_world = camera_model_module.image_to_world
def convert_image_to_global(calibration, image, point):
    g = tf.Graph()
    with g.as_default():
      extrinsic = tf.reshape(
          tf.constant(list(calibration.extrinsic.transform), dtype=tf.float64),
          [4, 4])
      intrinsic = tf.constant(list(calibration.intrinsic), dtype=tf.float64)
      metadata = tf.constant([
          calibration.width, calibration.height,
          calibration.rolling_shutter_direction
      ],
                             dtype=tf.int32)
      camera_image_metadata = list(image.pose.transform)
      camera_image_metadata.append(image.velocity.v_x)
      camera_image_metadata.append(image.velocity.v_y)
      camera_image_metadata.append(image.velocity.v_z)
      camera_image_metadata.append(image.velocity.w_x)
      camera_image_metadata.append(image.velocity.w_y)
      camera_image_metadata.append(image.velocity.w_z)
      camera_image_metadata.append(image.pose_timestamp)
      camera_image_metadata.append(image.shutter)
      camera_image_metadata.append(image.camera_trigger_time)
      camera_image_metadata.append(image.camera_readout_done_time)
      image_points = tf.constant([point],dtype=tf.float64)

      global_points = image_to_world(
          extrinsic, intrinsic, metadata, camera_image_metadata, image_points)

      with tf.Session(graph=g) as sess:
          global_points = sess.run([global_points])
      #print(global_points)

      return global_points

def convert_gtv(pose,point):
    transform = np.linalg.inv(np.array(pose.transform).reshape(4,4))
    point = np.append(point,1)
    comp = transform @ point
    #print(comp)
    return comp[:-1]

final_dicts = []

print("Starting")
print(len(twoD))

for i,ann in tqdm(enumerate(twoD)):
    depval  = depth[i]
    if(ann["image_id"] != depval["image_id"] or ann["category_id"] != depval["category_id"]):
        print("EEK")
    
    xL, yL, width, height = ann["bbox"]
    center_x = int((xL + width/2) / 0.5625)
    center_y = int((yL + height/2) / 0.5625)

    center_z = depval["distance_to_obj"] + 0.5*depval["obj_thickness"]

    context_name, timestamp_micros, imagenum,_ = ann["image_id"].split(".")

    f = open("contexts/{}.{}.pickle".format(context_name,timestamp_micros),"rb")
    pickledict = pickle.load(f)
    f.close()

    calibration = pickledict[str(imagenum)+"_calibration"]
    imgval = pickledict[str(imagenum)+"_image"]
    pose = pickledict["pose"]

    #Center
    gp = convert_image_to_global(calibration, imgval, [center_x,center_y,center_z])[0][0]
    center = convert_gtv(pose,gp)
    #print("\n\n")

    #Top Left
    gp = convert_image_to_global(calibration,imgval,[xL/0.5625,yL/0.5625,depval["distance_to_obj"]])
    TPL = convert_gtv(pose,gp)

    final_dict = {"center":center.tolist(), "TPL": TPL.tolist(), "context": context_name, "timestamp_micros":timestamp_micros,"score":ann["score"], "category_id":ann["category_id"]}
    final_dicts.append(final_dict)

f = open("3D/"+cam+".json","w+")
json.dump(final_dicts,f)
f.close()
    






    





