import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import argparse
import sys

# Path to your DEM file
# file_path = "data/PuneDem.tif"  # Ensure this path is correct

def main(file_path,colormap):
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
    print("Raster loaded successfully!")  # Debug message
    # Plot the DEM raster data
    plt.figure(figsize=(10, 6))
    # plt.imshow(raster, cmap='terrain', interpolation='nearest')
    plt.imshow(raster, colormap, interpolation='nearest')
    plt.colorbar(label='Elevation (m)')
    plt.title('DEM with Negative Values as NoData')
    plt.axis('off')  # Hide the axis
    plt.show()
    # return raster

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



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster Visualization Tool")
    parser.add_argument("--file", required=True, help="Path to raster file")
    parser.add_argument("--cmap", default="viridis", help="Matplotlib colormap")
    
    args = parser.parse_args()
    main(args.file, args.cmap)