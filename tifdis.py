import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

# Path to your DEM file
dem_file_path = "data/puneDem.tif"  # Ensure this path is correct

# Open the DEM file
dem_ds = gdal.Open(dem_file_path)

# Ensure DEM file is loaded correctly
if dem_ds is None:
    raise FileNotFoundError(f"DEM file not found at path: {dem_file_path}")

# Read the DEM raster data as an array
dem_raster_data = dem_ds.ReadAsArray()

# Convert to float to allow assignment of NaN (as NaN can't be assigned to an integer array)
dem_raster_data = dem_raster_data.astype(float)

# Set negative values as NoData (NaN)
dem_raster_data[dem_raster_data < 0] = np.nan  # Treat negative values as NoData

# Close the DEM dataset
dem_ds = None

# Plot the DEM raster data
plt.figure(figsize=(10, 6))
plt.imshow(dem_raster_data, cmap='terrain', interpolation='nearest')
plt.colorbar(label='Elevation (m)')
plt.title('DEM with Negative Values as NoData')
plt.axis('off')  # Hide the axis
plt.show()
