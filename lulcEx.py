import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
import sys


def display_pct_raster(raster_path):
    try:
        # Open the raster file
        dataset = gdal.Open(raster_path)
        if dataset is None:
            raise FileNotFoundError(f"Could not open raster file: {raster_path}")
        
        # Check raster metadata
        print("Raster Metadata:")
        print(f" - Projection: {dataset.GetProjection()}")
        print(f" - Geotransform: {dataset.GetGeoTransform()}")
        print(f" - Driver: {dataset.GetDriver().LongName}")
        
        # Extract the first band (PCT is usually associated with band 1)
        band = dataset.GetRasterBand(1)
        if band is None:
            raise ValueError("The raster does not have a valid first band.")
        
        # Extract raster data as array
        raster_data = band.ReadAsArray()
        print("Raster Data Type:", raster_data.dtype)
        print("Unique Values in Raster:", np.unique(raster_data))
        
        # Handle potential NoData values
        nodata_value = band.GetNoDataValue()
        print("NoData Value:", nodata_value)
        if nodata_value is not None:
            raster_data = np.where(raster_data == nodata_value, np.nan, raster_data)
        
        # Extract the PCT (color table)
        color_table = band.GetRasterColorTable()
        if color_table is None:
            raise ValueError("The raster does not have an associated color table (PCT).")
        
        # Debug: Print the color table entries
        print("\nExtracted Color Table:")
        value_color_map = {}
        for i in range(color_table.GetCount()):
            entry = color_table.GetColorEntry(i)
            value_color_map[i] = (entry[0], entry[1], entry[2])  # R, G, B
            print(f" - Value {i}: RGB {entry[0]}, {entry[1]}, {entry[2]}")
        
        # Debug: Check missing indices
        missing_values = [value for value in np.unique(raster_data) if value not in value_color_map]
        if missing_values:
            print(f"\nWarning: Some raster values are missing in the color table: {missing_values}")
        
        # Create a colormap
        max_value = max(value_color_map.keys())
        colormap = np.zeros((max_value + 1, 4))  # RGBA colormap
        for value, (r, g, b) in value_color_map.items():
            colormap[value] = [r / 255.0, g / 255.0, b / 255.0, 1.0]  # Normalize RGB to 0-1
        
        # Plot the raster with the colormap
        plt.figure(figsize=(10, 8))
        plt.imshow(raster_data, cmap=plt.cm.colors.ListedColormap(colormap), interpolation='nearest')
        plt.colorbar(label='LULC Classes')
        plt.title("PCT LULC Map")
        plt.xlabel("X (pixels)")
        plt.ylabel("Y (pixels)")
        plt.grid(False)
        plt.show()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# Input PCT raster file path
raster_file = "data/ps1.tif"

# Call the function to display the raster
display_pct_raster(raster_file)
