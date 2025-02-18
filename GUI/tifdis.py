import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

# Path to your DEM file
file_path = "data/PuneLuLc_with_integers.tif"  # Ensure this path is correct

def load_raster(file_path):
    print("load_raster() function called! hello")  # Debug message
    """Load a raster file using GDAL."""
    dataset = gdal.Open(file_path)
    if dataset is None:
        raise FileNotFoundError(f"Failed to open raster at path: {file_path}")
    #  Read the DEM raster data as an array
    raster = dataset.ReadAsArray()

    # Convert to float to allow assignment of NaN (as NaN can't be assigned to an integer array)
    raster = raster.astype(float)

    # Set negative values as NoData (NaN)
    raster[raster < 0] = np.nan  # Treat negative values as NoData

    # Close the DEM dataset
    dataset = None

    print("Raster loaded successfully!")  # Debug message
    return raster

# file=load_raster(file_path)

# Open the DEM file
# dem_ds = gdal.Open(dem_file_path)

# Ensure DEM file is loaded correctly
# if dem_ds is None:
#     raise FileNotFoundError(f"DEM file not found at path: {dem_file_path}")

# Read the DEM raster data as an array
# raster = dem_ds.ReadAsArray()

# Convert to float to allow assignment of NaN (as NaN can't be assigned to an integer array)
# raster = raster.astype(float)

# Set negative values as NoData (NaN)
# raster[raster < 0] = np.nan  # Treat negative values as NoData

# Close the DEM dataset
# dem_ds = None

# print("Raster loaded successfully!")  # Debug message
# Plot the DEM raster data
# plt.figure(figsize=(10, 6))
# plt.imshow(file, cmap='terrain', interpolation='nearest')
# plt.colorbar(label='Elevation (m)')
# plt.title('DEM with Negative Values as NoData')
# plt.axis('off')  # Hide the axis
# plt.show()
