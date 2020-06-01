# Lint as: python3
# Copyright 2020 The Waymo Open Dataset Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================*/
"""A simple example to generate a file that contains serialized Objects proto."""

from waymo_open_dataset import dataset_pb2
from waymo_open_dataset import label_pb2
from waymo_open_dataset.protos import metrics_pb2
import sys
from tqdm import tqdm

import json
import pickle

#{"image_id": 1, "bbox": [758.0443115234375, 604.7687377929688, 26.64288330078125, 35.4365234375], "score": 0.0606762170791626, "category_id": 1}

annotations =[] #[json.load(f)]
#f.close()
for i in range(5):
    f = open("/home/harish_k_kamath/data/testing_domain/3D/CAMERA_{}.json".format(i+1),"r")#open("/home/harish_k_kamath/data/testing/results/CAMERA_{}_results.bbox.json".format(i+1),"r")#/home/harish_k_kamath/data/testing/results/final.json","r")
    annotations += json.load(f)
    f.close()

SCORE_THRESHOLD = float(sys.argv[1])

#f = open("data/conversion/context-conversions.pickle","rb")
#contexts = pickle.load(f)
#f.close()

#f = open("data/conversion/annotations/imagetoids.json","r")
#imagetoids = json.load(f)
#f.close()

objects = metrics_pb2.Objects()

def _create_pd_file_example(annotation):
  """Creates a prediction objects file."""

  #image_id = annotation["image_id"]

  #imagepath = imagetoids[str(image_id)]
  #context = contexts['./' + imagepath]

  #idparts = image_id.split(".")
  

  o = metrics_pb2.Object()
  # The following 3 fields are used to uniquely identify a frame a prediction
  # is predicted at. Make sure you set them to values exactly the same as what
  # we provided in the raw data. Otherwise your prediction is considered as a
  # false negative.
  o.context_name = annotation["context"]#idparts[0]#(context["ContextName"])
  # The frame timestamp for the prediction. See Frame::timestamp_micros in
  # dataset.proto.
  invalid_ts = -1
  o.frame_timestamp_micros = int(annotation["timestamp_micros"])#int(idparts[1])#context["TimestampMicros"]
  # This is only needed for 2D detection or tracking tasks.
  # Set it to the camera name the prediction is for.
  #o.camera_name = int(idparts[2])#context["CAMName"]

  # Populating box and score.
  box = label_pb2.Label.Box()
  #xL = annotation["bbox"][0]
  #yL = annotation["bbox"][1]
  #w = annotation["bbox"][2]
  #h = annotation["bbox"][3]
  center = annotation["center"]
  TPL = annotation["TPL"]

  box.center_x = center[0]#(xL + w/2) * float(1920)/1080
  box.center_y = center[1]#(yL + h/2) * float(1920)/1080
  box.center_z = center[2]#0
  box.length = abs(center[0]-TPL[0])*2#w * float(1920)/1080
  box.width = abs(center[1]-TPL[1])*2#h * float(1920)/1080
  box.height = abs(center[2]-TPL[2])*2#0
  box.heading = 0
  o.object.box.CopyFrom(box)
  # This must be within [0.0, 1.0]. It is better to filter those boxes with
  # small scores to speed up metrics computation.
  o.score = annotation["score"]
  # For tracking, this must be set and it must be unique for each tracked
  # sequence.
  o.object.id = 'unique object tracking ID'
  # Use correct type.

  label = {3: label_pb2.Label.TYPE_VEHICLE, 1 : label_pb2.Label.TYPE_PEDESTRIAN, 0 : label_pb2.Label.TYPE_UNKNOWN, 12 : label_pb2.Label.TYPE_SIGN, 2 : label_pb2.Label.TYPE_CYCLIST}
  o.object.type = label[annotation["category_id"]]

  if o.score > SCORE_THRESHOLD:
      objects.objects.append(o)

  # Add more objects. Note that a reasonable detector should limit its maximum
  # number of boxes predicted per frame. A reasonable value is around 400. A
  # huge number of boxes can slow down metrics computation.


def main():
    print("Total number of annotations: {}".format(len(annotations)))
    for a in tqdm(annotations):
        _create_pd_file_example(a)
    # Write objects to a file.
    #print(len([x for x in objects.objects if x.context_name == "11450298750351730790_1431_750_1451_750" and x.frame_timestamp_micros==1508103384966609 and x.camera_name==1]))
    f = open('/home/harish_k_kamath/submit_files/predictions_SCORE'+sys.argv[1]+'.bin', 'wb')
    f.write(objects.SerializeToString())
    f.close()


if __name__ == '__main__':
  main()

