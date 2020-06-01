import sys
import os

score = sys.argv[1]

os.system("mkdir model"+score)
os.system("sudo /home/harish_k_kamath/waymo-od/waymo-open-dataset/bazel-bin/waymo_open_dataset/metrics/tools/create_submission --input_filenames='predictions_SCORE"+score+".bin' --output_filename='model"+score+"/model' --submission_filename='/home/harish_k_kamath/submission.txtpb'")
os.system("tar cvf model"+score+".tar model"+score+"/")
os.system("gzip model"+score+".tar")
