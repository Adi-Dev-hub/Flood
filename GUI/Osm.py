import sys
import webbrowser
import threading
import subprocess
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import folium
import overpy
from affine import Affine
from flask import Flask, render_template_string
from Osm_ui import Ui_Dialog  # Import the UI file


class FloodRiskApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect buttons to functions
        self.ui.toolButton.clicked.connect(self.browse_file)
        self.ui.pushButton.clicked.connect(self.run_analysis)

        self.risk_map_path = ""  # Store selected file path
        self.app = Flask(__name__)  # Initialize Flask server

    def browse_file(self):
        """Opens a file dialog to select a GeoTIFF file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Risk Map File", "", "GeoTIFF Files (*.tif *.tiff)")
        if file_path:
            self.ui.lineEdit.setText(file_path)
            self.risk_map_path = file_path

    def run_analysis(self):
        """Processes the flood risk map, runs Flask, and opens the browser."""
        if not self.risk_map_path:
            print("Please select a file first!")
            return

        print(f"Processing file: {self.risk_map_path}")
        png_path = "combined_risk_output.png"  # Temporary PNG output

        # -------------------------------
        # Read the Risk Map using GDAL
        # -------------------------------
        dataset = gdal.Open(self.risk_map_path)
        if dataset is None:
            print(f"Cannot open risk map: {self.risk_map_path}")
            return

        band = dataset.GetRasterBand(1)
        risk_data = band.ReadAsArray().astype(np.uint8)
        transform = dataset.GetGeoTransform()
        affine_transform = Affine.from_gdal(*transform)

        # Calculate geographic bounds
        min_x, pixel_width, _, max_y, _, pixel_height = transform
        rows, cols = risk_data.shape
        max_x = min_x + cols * pixel_width
        min_y = max_y + rows * pixel_height  # pixel_height is negative

        dataset = None  # Close dataset

        # -------------------------------
        # Save the Risk Map as PNG
        # -------------------------------
        cmap = ListedColormap(['yellow', 'orange', 'red', 'gray'])  # Colormap
        plt.imsave(png_path, risk_data, cmap=cmap)

        # -------------------------------
        # Create a Folium Map
        # -------------------------------
        center_lat = (min_y + max_y) / 2
        center_lon = (min_x + max_x) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Add risk map overlay
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
        # Query Hospitals from Overpass API
        # -------------------------------
        api = overpy.Overpass()
        query = f"""node["amenity"="hospital"]({min_y},{min_x},{max_y},{max_x});out;"""
        result = api.query(query)

        # Feature groups for hospitals
        fg_low = folium.FeatureGroup(name="Low Risk Hospitals")
        fg_medium = folium.FeatureGroup(name="Moderate Risk Hospitals")
        fg_high = folium.FeatureGroup(name="High Risk Hospitals")

        inv_affine = ~affine_transform  # Convert coordinates to pixels

        for node in result.nodes:
            hosp_lat, hosp_lon = float(node.lat), float(node.lon)
            col, row = inv_affine * (hosp_lon, hosp_lat)
            col, row = int(round(col)), int(round(row))

            if row < 0 or row >= risk_data.shape[0] or col < 0 or col >= risk_data.shape[1]:
                continue  # Skip if out of bounds

            risk_value = risk_data[row, col]
            name = node.tags.get("name", "Hospital")

            # 🚀 Handle No Data (4) → Skip the hospital
            if risk_value == 4:
                continue 
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
        # Run Flask Server
        # -------------------------------
        @self.app.route("/")
        def index():
            return render_template_string(m.get_root().render())

        def run_server():
            """Run Flask server in a separate thread."""
            self.app.run(debug=False, use_reloader=False)

        threading.Thread(target=run_server, daemon=True).start()
        webbrowser.open("http://127.0.0.1:5000/")  # Open in browser


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FloodRiskApp()
    window.show()
    sys.exit(app.exec())
