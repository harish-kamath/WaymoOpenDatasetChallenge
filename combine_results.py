import json
from tqdm import tqdm

final_json = []
for i in range(5):
	f = open("/home/harish_k_kamath/data/testing/results/CAMERA_"+str(i+1)+"_results.bbox.json","r")
	a = json.load(f)
	f.close()
	for x in tqdm(a):
		final_json.append(a)
print("Read all!")
with open("/home/harish_k_kamath/data/testing/results/final.json", "w+") as f:
	json.dump(final_json, f)
