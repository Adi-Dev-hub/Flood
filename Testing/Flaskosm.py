from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import folium
import overpy
from affine import Affine
from flask import Flask, render_template_string

# -------------------------------
# File Paths and Parameters
# -------------------------------
risk_map_path = "C:/Users/Admin/Documents/GitHub/Flood/Testing/combined_risk_output.tif"  # Input GeoTIFF risk map
png_path = "combined_risk_output.png"       # Temporary PNG output for overlay

# -------------------------------
# Read the Risk Map using GDAL
# -------------------------------
dataset = gdal.Open(risk_map_path)
if dataset is None:
    raise FileNotFoundError(f"Cannot open risk map: {risk_map_path}")

band = dataset.GetRasterBand(1)
risk_data = band.ReadAsArray().astype(np.uint8)  # Assumes risk values: 1 (Low), 2 (Medium), 3 (High), 4 (No Data)
transform = dataset.GetGeoTransform()  # GDAL transform tuple
affine_transform = Affine.from_gdal(*transform)

# Calculate geographic bounds from the transform
min_x = transform[0]                # Left (longitude)
max_y = transform[3]                # Top (latitude)
pixel_width = transform[1]
pixel_height = transform[5]         # (usually negative)
rows, cols = risk_data.shape
max_x = min_x + cols * pixel_width   # Right (longitude)
min_y = max_y + rows * pixel_height  # Bottom (latitude); note: pixel_height is negative

dataset = None  # Close the dataset

# -------------------------------
# Save the Risk Map as PNG for Overlay
# -------------------------------
# Define a colormap: 1 = Yellow (Low), 2 = Orange (Medium), 3 = Red (High), 4 = Gray (No Data)
cmap = ListedColormap(['yellow', 'orange', 'red', 'gray'])
plt.imsave(png_path, risk_data, cmap=cmap)

# -------------------------------
# Create a Folium Map and Overlay the Risk Map
# -------------------------------
center_lat = (min_y + max_y) / 2
center_lon = (min_x + max_x) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Folium expects bounds in the form: [[south, west], [north, east]]
image_bounds = [[min_y, min_x], [max_y, max_x]]
folium.raster_layers.ImageOverlay(
    name="Flood Risk Map",
    image=png_path,
    bounds=image_bounds,
    opacity=0.6,
    interactive=True,
    cross_origin=False,
    zindex=1
).add_to(m)

# -------------------------------
# Query Hospitals using Overpass API
# -------------------------------
# Use the risk map's bounds for the query (Overpass uses: south, west, north, east)
api = overpy.Overpass()
query = f"""
node["amenity"="hospital"]({min_y},{min_x},{max_y},{max_x});
out;
"""
result = api.query(query)

# Create separate FeatureGroups for hospitals by risk level
fg_low = folium.FeatureGroup(name="Low Risk Hospitals")
fg_medium = folium.FeatureGroup(name="Moderate Risk Hospitals")
fg_high = folium.FeatureGroup(name="High Risk Hospitals")

# Inverse affine transform to convert geographic coordinates to pixel indices
inv_affine = ~affine_transform

for node in result.nodes:
    hosp_lat = float(node.lat)
    hosp_lon = float(node.lon)
    # Convert (lon, lat) to pixel (col, row)
    col, row = inv_affine * (hosp_lon, hosp_lat)
    col = int(round(col))
    row = int(round(row))
    # Skip if outside raster bounds
    if row < 0 or row >= risk_data.shape[0] or col < 0 or col >= risk_data.shape[1]:
        continue
    risk_value = risk_data[row, col]
    name = node.tags.get("name", "Hospital")
    if risk_value == 1:
        fg_low.add_child(folium.Marker(
            location=[hosp_lat, hosp_lon],
            popup=name,
            icon=folium.Icon(color='green', icon='info-sign')
        ))
    elif risk_value == 2:
        fg_medium.add_child(folium.Marker(
            location=[hosp_lat, hosp_lon],
            popup=name,
            icon=folium.Icon(color='orange', icon='info-sign')
        ))
    elif risk_value == 3:
        fg_high.add_child(folium.Marker(
            location=[hosp_lat, hosp_lon],
            popup=name,
            icon=folium.Icon(color='red', icon='info-sign')
        ))
    # If risk_value == 4 ("No Data"), we ignore it

m.add_child(fg_low)
m.add_child(fg_medium)
m.add_child(fg_high)
folium.LayerControl().add_to(m)

# -------------------------------
# Run a Flask Server to Serve the Map
# -------------------------------
app = Flask(__name__)

@app.route("/")
def index():
    map_html = m.get_root().render()
    return render_template_string(map_html)

if __name__ == "__main__":
    app.run(debug=True)
