import os
from PIL import Image
import json
from tqdm import tqdm

folders = [f for f in os.listdir("images/")]
imagelist = [[],[],[],[],[]]
labellist = []

category_mappings = {"TYPE_VECHICLE":3, "TYPE_UNKNOWN":0,"TYPE_PEDESTRIAN":1,"TYPE_SIGN":12,"TYPE_CYCLIST":2}

image_to_ids = {}

ids = 0

for image in tqdm(folders):
    #images = ["images/{}/{}".format(track,k) for k in os.listdir("images/{}".format(track))]
    #for image in images:
    image_record = {}
    image_record["file_name"] = "images/"+image
    im = Image.open("images/"+image)
    width, height = im.size
    image_record["height"] = height
    image_record["width"] = width
        #pathsplit = image.split("/")
        #ids += 1
    image_record["id"] = image
    camera_num = int(image[-5])
        #image_to_ids[ids] = image
    imagelist[camera_num-1].append(image_record)

#    with open("labels/"+track+".txt","r") as labelfile:
#        labels = labelfile.readlines()
#        for label in labels:
#            pieces = label.split()
#            label_record = {}
#            label_record["image_id"] = image_to_ids[track+"_"+pieces[0]][0]
#            label_record["area"] = image_to_ids[track+"_"+pieces[0]][1]
#            label_record["segmentation"] = [[]]
#            label_record["bbox"] = [float(pieces[6]),float(pieces[7]),float(pieces[8]),float(pieces[9])]
#            label_record["category_id"] = category_mappings[pieces[2]]
#            label_record["iscrowd"] = 0
#            ids += 1
#            label_record["id"] = ids
#            labellist.append(label_record)

for i in range(5):
    jsonfinal = {}
    jsonfinal["images"] = imagelist[i]
    jsonfinal["categories"] = [
        {"supercategory": "other","id": 0,"name": "unlabeled"},
        {"supercategory": "person","id": 1,"name": "person"},
        {"supercategory": "vehicle","id": 2,"name": "bicycle"},
        {"supercategory": "vehicle","id": 3,"name": "car"},
        {"supercategory": "other","id":12, "name":"sign"}]
    #jsonfinal["annotations"] = labellist
    with open("annotations/CAMERA_"+str(i+1)+".json","w+") as f:
        json.dump(jsonfinal, f)

