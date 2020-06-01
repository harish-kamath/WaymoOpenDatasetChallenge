import json
import numpy as np
import PIL

# INSERT PROPER BBOX FILE HERE
with open("test_results.bbox.json", "r") as read_file:
    bboxes = json.load(read_file)

data = list()
for bbox in bboxes:
    bbox_depth = dict()
    image_id = bbox["image_id"]
    category_id = int(bbox["category_id"])

    bbox_depth["image_id"] = image_id
    bbox_depth["category_id"] = category_id

    vals_filename = "testing/vals/" + image_id + '_disp.npy'
    npy_img = np.load(vals_filename)

   

    # get center x and center y coords
    xL = bbox["bbox"][0]
    yL = bbox["bbox"][1]
    w = bbox["bbox"][2]
    h = bbox["bbox"][3]

    center_x = xL + w/2
    center_y = yL + h/2

    # find size of image
    image_filepath = "/home/harish_k_kamath/data/testing/images/" + image_id + ".png"
    image = PIL.Image.open(image_filepath)
    img_width, img_height = image.size
    # divide center y by image height, multiply by 192 and cast to integer
    y_npy = int((center_y/img_height)*192)
    # divide center x by image width, multiply by 640 and cast to integer
    x_npy = int((center_x/img_width)*640)

    obj_distance = npy_img[0][0][y_npy][x_npy]
    bbox_depth["distance_to_obj"] = obj_distance

    # TYPE_UNKNOWN = 0;
    # TYPE_VEHICLE = 1;
    # TYPE_PEDESTRIAN = 2;
    # TYPE_SIGN = 3;
    # TYPE_CYCLIST = 4;
    obj_thicknesses = {1: 3, 2: 0.7, 3: 0.5, 4: 1.5} 
    bbox_depth["obj_thickness"] = obj_thicknesses[category_id]
    data.append(bbox_depth)
    

with open("object_depths.json", "w") as write_file:
    json.dump(data, write_file)
