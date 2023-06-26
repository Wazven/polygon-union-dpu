from fastapi import FastAPI
from shapely.geometry import Polygon
from shapely import unary_union
import folium
import json
import requests
from dotenv import load_dotenv
import os

app = FastAPI()

@app.get("/union_polygon")
async def get_union_polygon():
    ip_address = '103.101.52.72:5098'
    response = requests.get(f'http://{ip_address}')
    data_json = response.json()

    smg_lat = -6.966667
    smg_lon = 110.416664
    map_semarang = folium.Map(location=[smg_lat, smg_lon], zoom_start=13)

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

            polygon = Polygon(coordinates)
            polygon_geometries.append(polygon)

    union_polygon = unary_union(polygon_geometries)

    final_union_polygon = []
    if union_polygon.geom_type == 'Polygon':
        final_union_polygon.append(list(union_polygon.exterior.coords))
    elif union_polygon.geom_type == 'MultiPolygon':
        for polygon in union_polygon.geoms:
            polygon_coordinates = list(polygon.exterior.coords)
            folium.Polygon(locations=polygon_coordinates, color='blue', fill=True, fill_color='blue', fill_opacity=0.4).add_to(map_semarang)
            final_union_polygon.append(polygon_coordinates)

    json_final_union_polygon = json.dumps(final_union_polygon)
    return json_final_union_polygon

# uvicorn main:app --reload

