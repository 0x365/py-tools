from geojson import Feature, FeatureCollection, Point, Polygon
from turfpy.measurement import points_within_polygon
from ipyleaflet import Map, GeoJSON
import math


coords = [(-46.653, -23.543),(-46.634, -23.5346),(-46.613, -23.543),(-46.614, -23.559),(-46.631, -23.567),(-46.653, -23.560),(-46.653, -23.543),]


poly = Polygon(
    [
        coords
    ]
)

res = 0.001
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


m = Map(center=(-23.5523, -46.6318), zoom=13)

data = result.copy()
data["features"].append(Feature(geometry=poly))

m = Map(center=(-23.5523, -46.6318), zoom=13)

geo_json = GeoJSON(
    data=data,
    style={"opacity": 1, "dashArray": "9", "fillOpacity": 0.3, "weight": 1},
    hover_style={"color": "green", "dashArray": "0", "fillOpacity": 0.5},
)
m.add_layer(geo_json)
m

m.save('my_map_example.html', title="My Map")