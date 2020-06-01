import tensorflow as tf
import tensorflow.compat.v1 as tf
import math
import numpy as np
import itertools
import matplotlib.pyplot as plt
import cv2
import os
import argparse
from tqdm import tqdm
import pickle

from waymo_open_dataset.utils import frame_utils
from waymo_open_dataset import dataset_pb2 as open_dataset

tf.enable_eager_execution()
WAYMO_CLASSES = ['TYPE_UNKNOWN', 'TYPE_VECHICLE', 'TYPE_PEDESTRIAN', 'TYPE_SIGN', 'TYPE_CYCLIST']

def extract_frame(frames_path):#, outdir_img, class_mapping, resize_ratio=1.0):

    dataset = tf.data.TFRecordDataset(frames_path, compression_type='')
    #id_dict = {}
    #bboxes_all = {}
    #scores_all = {}
    #cls_inds_all = {}
    #track_ids_all = {}
    #if not os.path.exists(outdir_img):
    #    os.mkdir(outdir_img)
    for fidx, data in enumerate(dataset):
        frame = open_dataset.Frame()
        frame.ParseFromString(bytearray(data.numpy()))

        (range_images, camera_projections, range_image_top_pose) = (
            frame_utils.parse_range_image_and_camera_projection(frame))

        final_frame_dict = {}
        pose = frame.pose
        final_frame_dict["pose"] = pose
        for i in range(5):
            final_frame_dict[str(i+1)+"_image"] = frame.images[i]
            final_frame_dict[str(i+1)+"_calibration"] = frame.context.camera_calibrations[i]
        with open("contexts/{}.{}.pickle".format(frame.context.name,frame.timestamp_micros),"wb") as f:
            pickle.dump(final_frame_dict,f,protocol=pickle.HIGHEST_PROTOCOL)
        #time = frame.context.stats.time_of_day
        #weather = frame.context.stats.weather
        #for i in range(len(frame.images)):
        #    context_name = frame.context.name
        #    ftm = frame.timestamp_micros
        #    cam_name = frame.images[i].name
        #    im = tf.image.decode_jpeg(frame.images[i].image).numpy()[:,:,::-1]
        #    target_size = (int(im.shape[1] * resize_ratio), int(im.shape[0] * resize_ratio))
        #    im = cv2.resize(im, target_size)
        #    cv2.imwrite(outdir_img + '/{}.{}.{}.png'.format(context_name,ftm,cam_name), im)

    #if len(bboxes_all) > 0:
    #    writeKITTI(outname, bboxes_all, scores_all, cls_inds_all, track_ids_all, class_mapping)

def extract_labels(camera_label):
    box_labels = camera_label.labels
    boxes = []
    types = []
    ids = []
    for box_label in box_labels:
        boxes.append([box_label.box.center_x, box_label.box.center_y, box_label.box.length, box_label.box.width])
        types.append(box_label.type)
        ids.append(box_label.id)
    return boxes, types, ids

def convert_kitti(boxes, types, ids, id_dict):
    max_id = max(id_dict.values()) + 1 if len(id_dict) > 0 else 0
    boxes = np.array(boxes)
    if len(boxes) > 0:
        bboxes = np.zeros_like(boxes)
        bboxes[:, :2] = boxes[:, :2] - boxes[:, 2:] / 2
        bboxes[:, 2:] = boxes[:, :2] + boxes[:, 2:] / 2
    else:
        bboxes = np.zeros((0,4), dtype='f')
    
    cls_inds = []
    track_ids = []
    for cls, old_id in zip(types, ids):
        if old_id in id_dict:
            track_id = id_dict[old_id]
        else:
            id_dict[old_id] = max_id
            track_id = max_id
            max_id += 1
        cls_inds.append(cls)
        track_ids.append(track_id)
    cls_inds = np.array(cls_inds)
    track_ids = np.array(track_ids)
    return bboxes, cls_inds, track_ids

def writeKITTI(filename, bboxes, scores, cls_inds, track_ids=None, classes=None):
    f = open(filename, 'w')
    for fid in bboxes:
        for bid in range(len(bboxes[fid])):
            fields = [''] * 17
            fields[0] = fid
            fields[1] = -1 if track_ids is None else int(track_ids[fid][bid])
            fields[2] = classes[int(cls_inds[fid][bid])]
            fields[3:6] = [-1] * 3
            fields[6:10] = bboxes[fid][bid]
            fields[10:16] = [-1] * 6
            fields[16] = scores[fid][bid]
            fields = map(str, fields)
            f.write(' '.join(fields) + '\n')
    f.close()

def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('record_path')
    #parser.add_argument('output_id')
    #parser.add_argument('--workdir', default='.')
    #parser.add_argument('--resize', default=0.5625, type=float)
    #args = parser.parse_args()
    #os.chdir(args.workdir)
    #if not os.path.exists('images'):
    #    os.mkdir('images')
    #image_path = os.path.join('images', args.output_id)
    #if not os.path.exists('images'):
    #    os.mkdir(image_path)
    #if not os.path.exists('labels'):
    #    os.mkdir('labels')
    records = os.listdir("tfrecords/")
    for record in tqdm(records):
        extract_frame("tfrecords/"+record)#args.record_path, os.path.join('labels', args.output_id + '.txt'), image_path, WAYMO_CLASSES, resize_ratio=args.resize)

if __name__ == "__main__":
    main()
