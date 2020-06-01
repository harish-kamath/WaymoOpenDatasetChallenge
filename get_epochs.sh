#Camera 1
gcloud config set project central-bulwark-278221
gcloud compute scp waymo-test:/home/harish_k_kamath/data/training/conversion/work_dirs/cascade_rcnn_r50_fpn_1x/latest.pth ./epochs/CAMERA_1.pth

#Camera 2
gcloud config set project waymo-275201
gcloud compute scp waymoimage-1:/home/harish_k_kamath/data/training/conversion/work_dirs/cascade_rcnn_r50_fpn_1x/latest.pth ./epochs/CAMERA_2.pth

#Camera 3
gcloud config set project waymoproject4
gcloud compute scp waymo-test:/home/harish_k_kamath/data/training/conversion/work_dirs/cascade_rcnn_r50_fpn_1x/latest.pth ./epochs/CAMERA_3.pth

#Camera 4
gcloud config set project waymo-camera4
gcloud compute scp waymo-test:/home/harish_k_kamath/data/training/conversion/work_dirs/cascade_rcnn_r50_fpn_1x/latest.pth ./epochs/CAMERA_4.pth

#Camera 5
gcloud config set project principal-rhino-278019
gcloud compute scp waymo-test:/home/harish_k_kamath/data/training/conversion/work_dirs/cascade_rcnn_r50_fpn_1x/latest.pth ./epochs/CAMERA_5.pth

#Reset
gcloud config set project waymo-275201
