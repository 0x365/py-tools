from geojson import Feature, FeatureCollection, Point, Polygon
from turfpy.measurement import points_within_polygon
from ipyleaflet import Map, GeoJSON
import math
import json

## NOTES
# Check if polygons from different sources overlap?
# Could just leave as is and create crossover in pixelated mode.

with open("all_features.geojson") as f:
	gj = json.load(f)

features = gj['features']

for ii in range(len(features)):
    coords = features[ii]['geometry']['coordinates'][0]

    poly = Polygon(
        [
            coords
        ]
    )

    res = 0.00001
    rounder = round(math.log(1/res,10))

    min_lon = 400
    min_lat = 400
    max_lon = -400
    max_lat = -400

    for i in range(1, len(coords)):
        coords[i] = round(coords[i][0], rounder), round(coords[i][1], rounder)
        if coords[i][0] < min_lon:
            min_lon = coords[i][0]
        if coords[i][1] < min_lat:
            min_lat = coords[i][1]
        if coords[i][0] > max_lon:
            max_lon = coords[i][0]
        if coords[i][1] > max_lat:
            max_lat = coords[i][1]


    potential_points = []
    for lon in range(round(min_lon/res), round(max_lon/res)):
        for lat in range(round(min_lat/res), round(max_lat/res)):
            potential_points.append(Feature(geometry=Point((lon*res, lat*res))))

    result = points_within_polygon(FeatureCollection(potential_points), poly)

    output = []
    for i in range(len(result['features'])):
        #print(result['features'][0]['geometry']['coordinates'])
        try:
            output.append(result['features'][0]['geometry']['coordinates'])
        except:
            continue

    #print(result)
    with open("./all_points/"+str(ii)+"_points.json", "w") as f2:
        json.dump(output, f2)
    f2.close()
    print(ii)