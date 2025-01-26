import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

def clip_rainfall_to_dem(dem_path, rainfall_path):
    """
    Clips the rainfall raster to the extent of the DEM's valid region.

    Parameters:
    - dem_path (str): Path to the DEM raster file.
    - rainfall_path (str): Path to the interpolated rainfall raster file.

    Returns:
    - tuple: Clipped rainfall array, geotransform, and projection for visualization.
    """
    # Open the DEM file
    dem_ds = gdal.Open(dem_path)
    if dem_ds is None:
        raise FileNotFoundError(f"DEM file not found at path: {dem_path}")
    
    # Read DEM data as an array
    dem_raster_data = dem_ds.ReadAsArray().astype(float)
    dem_raster_data[dem_raster_data < 0] = np.nan  # Set negative values to NaN (NoData)
    
    # Open the Rainfall file
    rainfall_ds = gdal.Open(rainfall_path)
    if rainfall_ds is None:
        raise FileNotFoundError(f"Rainfall file not found at path: {rainfall_path}")
    
    # Read Rainfall data as an array
    rainfall_raster_data = rainfall_ds.ReadAsArray().astype(float)
    
    # Validate that the dimensions match
    if dem_raster_data.shape != rainfall_raster_data.shape:
        raise ValueError("DEM and Rainfall rasters must have the same dimensions.")
    
    # Clip rainfall data using DEM's valid region
    rainfall_clipped = np.where(np.isnan(dem_raster_data), np.nan, rainfall_raster_data)

    # Get geotransform and projection from the DEM
    geotransform = dem_ds.GetGeoTransform()
    projection = dem_ds.GetProjection()
    
    # Close datasets
    dem_ds = None
    rainfall_ds = None

    return rainfall_clipped, geotransform, projection

def display_grayscale_map(raster_data, geotransform):
    """
    Displays the raster data as a grayscale map.

    Parameters:
    - raster_data (numpy.ndarray): The raster data to display.
    - geotransform (tuple): Geotransform of the raster for extent.
    """
    # Calculate the extent
    xmin = geotransform[0]
    xres = geotransform[1]
    ymax = geotransform[3]
    yres = geotransform[5]
    xmax = xmin + (raster_data.shape[1] * xres)
    ymin = ymax + (raster_data.shape[0] * yres)
    extent = [xmin, xmax, ymin, ymax]

    # Display the raster
    plt.figure(figsize=(10, 8))
    plt.imshow(raster_data, cmap="gray", extent=extent, origin="upper")
    plt.colorbar(label="Rainfall (mm)")
    plt.title("Clipped Rainfall Grid (Grayscale)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

# Example usage
if __name__ == "__main__":
    # Paths to your DEM and rainfall raster files
    dem_file_path = "data/puneDem.tif"  # Replace with the path to your DEM file
    rainfall_file_path = "data/Cproximity.tif"  # Replace with the path to your rainfall file

    # Clip rainfall to DEM
    try:
        clipped_rainfall, geotransform, projection = clip_rainfall_to_dem(dem_file_path, rainfall_file_path)
        
        # Display the clipped rainfall as a grayscale map
        display_grayscale_map(clipped_rainfall, geotransform)
    except Exception as e:
        print(f"Error: {e}")
