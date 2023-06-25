#%% Get data json dari ip
import requests
ip_address = '103.101.52.72:5098'
response = requests.get(f'http://{ip_address}')

#menampilkan data json
data_json = response.json()
print (data_json)

# %% Menampilkan Map Semarang
import folium
smg_lat = -6.966667
smg_lon = 110.416664

map_semarang = folium.Map(location=[smg_lat, smg_lon], zoom_start=13)

#%% Koordinat poligon
from shapely.geometry import Polygon
polygon_geometries = []
for item in data_json:
    polygon_data = item.get('polygon')
    if polygon_data:
        coordinates = []
        for pair in polygon_data.split('),('):
            pair = pair.strip('()').strip(',')
            lat, lon = map(float, pair.split(','))
            coordinates.append([lat, lon])

        if len(coordinates) < 4:
            continue

        # folium.Polygon(locations=coordinates, color='red', fill=True, fill_color='red', fill_opacity=0.4).add_to(map_semarang)

        polygon = Polygon(coordinates)
        polygon_geometries.append(polygon)

#%% Union polygon

from shapely import unary_union
union_polygon = unary_union(polygon_geometries)

union_polygon = []
if union_polygon.geom_type == 'Polygon':
    union_polygon.append(union_polygon)
elif union_polygon.geom_type == 'MultiPolygon':
    union_polygon.extend(list(union_polygon.geoms))

final_union_polygon = []
for polygon in union_polygon:
    polygon_coordinates = list (polygon.exterior.coords)
    folium.Polygon(locations=polygon_coordinates, color = 'blue', fill = True, fill_color = 'blue', fill_opacity = 0.4).add_to(map_semarang)
    #Grouping the union polygons
    final_union_polygon.append(polygon_coordinates)

#Displaying
map_semarang

#%%
from shapely import unary_union

union_polygon = unary_union(polygon_geometries)

final_union_polygon = []
if union_polygon.geom_type == 'Polygon':
    final_union_polygon.append(list(union_polygon.exterior.coords))
elif union_polygon.geom_type == 'MultiPolygon':
    for polygon in union_polygon.geoms:
        polygon_coordinates = list(polygon.exterior.coords)
        folium.Polygon(locations=polygon_coordinates, color='blue', fill=True, fill_color='blue', fill_opacity=0.4).add_to(map_semarang)
        final_union_polygon.append(polygon_coordinates)

# Displaying
map_semarang
# %% post from list to json
import json
json_final_union_polygon = json.dumps(final_union_polygon)

  
# %%
