from waymo_open_dataset.protos import metrics_pb2

f = open("submit_files/predictions_SCORE0.bin","rb")
#x = open("validation_ground_truth_objects_gt.bin","rb")

#preds = metrics_pb2.Objects()
gt = metrics_pb2.Objects()

if gt.ParseFromString(f.read()): print("Okay!")
#if gt.ParseFromString(x.read()): print("Good")

#print(preds.objects[0])
#print(gt.objects[0])
#print("We have {} objects, they have {}".format(len(preds.objects), len(gt.objects)))

#context = "11048712972908676520_545_000_565_000"
#ftm = 1522684693237794
#print("There are {} of given context in gt".format(len([c for c in gt.objects if c.context_name == context])))
#print("There are {} of given context in preds".format(len([c for c in preds.objects if c.context_name == context])))

#print(preds.objects[500])
#print(gt.objects[500])

#for c in preds.objects:
#    if c.context_name == context and c.frame_timestamp_micros == ftm:
#        print(c)
#        break

#for c in gt.objects:
#    if c.context_name == context and c.frame_timestamp_micros == ftm:
#        print(c)
#        break
for i in range(2):
    print(gt.objects[10*i])
#print(gt.objects[100])
#print(gt.objects[200])

