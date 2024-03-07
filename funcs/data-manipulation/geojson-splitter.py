import json

with open("all_features.geojson") as f:
	gj = json.load(f)

features = gj['features']

print(features[0])

for i in range(len(features)):
	with open("./all_geometry/"+str(i)+"_feature.json", "w") as f2:
		json.dump(features[i], f2)
