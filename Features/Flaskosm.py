import sys
import webbrowser
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import folium
import overpy
from affine import Affine
from flask import Flask, render_template_string
import threading

# -------------------------------
# Get File Path from Command Line Argument
# -------------------------------
if len(sys.argv) < 2:
    print("Usage: python Flaskosm.py <path_to_risk_map>")
    sys.exit(1)

risk_map_path = sys.argv[1]  # File path provided by the GUI
png_path = "combined_risk_output.png"  # Temporary PNG output for overlay

# -------------------------------
# Read the Risk Map using GDAL
# -------------------------------
dataset = gdal.Open(risk_map_path)
if dataset is None:
    raise FileNotFoundError(f"Cannot open risk map: {risk_map_path}")

band = dataset.GetRasterBand(1)
risk_data = band.ReadAsArray().astype(np.uint8)
transform = dataset.GetGeoTransform()
affine_transform = Affine.from_gdal(*transform)

# Calculate geographic bounds
min_x, pixel_width, _, max_y, _, pixel_height = transform
rows, cols = risk_data.shape
max_x = min_x + cols * pixel_width
min_y = max_y + rows * pixel_height  # pixel_height is negative

dataset = None  # Close the dataset

# -------------------------------
# Save the Risk Map as PNG for Overlay
# -------------------------------
cmap = ListedColormap(['yellow', 'orange', 'red', 'gray'])  # Define a colormap
plt.imsave(png_path, risk_data, cmap=cmap)

# -------------------------------
# Create a Folium Map and Overlay the Risk Map
# -------------------------------
center_lat = (min_y + max_y) / 2
center_lon = (min_x + max_x) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

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
api = overpy.Overpass()
query = f"""
node["amenity"="hospital"]({min_y},{min_x},{max_y},{max_x});
out;
"""
result = api.query(query)

# Feature groups for hospitals by risk level
fg_low = folium.FeatureGroup(name="Low Risk Hospitals")
fg_medium = folium.FeatureGroup(name="Moderate Risk Hospitals")
fg_high = folium.FeatureGroup(name="High Risk Hospitals")

inv_affine = ~affine_transform  # Inverse transform to map coordinates to pixels

for node in result.nodes:
    hosp_lat, hosp_lon = float(node.lat), float(node.lon)
    col, row = inv_affine * (hosp_lon, hosp_lat)
    col, row = int(round(col)), int(round(row))

    if row < 0 or row >= risk_data.shape[0] or col < 0 or col >= risk_data.shape[1]:
        continue  # Skip if out of bounds

    risk_value = risk_data[row, col]
    name = node.tags.get("name", "Hospital")
    
    icon_color = "green" if risk_value == 1 else "orange" if risk_value == 2 else "red"
    fg = fg_low if risk_value == 1 else fg_medium if risk_value == 2 else fg_high

    fg.add_child(folium.Marker(
        location=[hosp_lat, hosp_lon],
        popup=name,
        icon=folium.Icon(color=icon_color, icon='info-sign')
    ))

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
    return render_template_string(m.get_root().render())

def run_server():
    """Run Flask server on a separate thread."""
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    webbrowser.open("http://127.0.0.1:5000/")
