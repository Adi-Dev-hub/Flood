from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

def load_raster(file_path):
    """Loads a raster file and returns its dataset, array, and metadata."""
    ds = gdal.Open(file_path)
    if ds is None:
        raise ValueError(f"Failed to open raster: {file_path}")
    
    array = ds.GetRasterBand(1).ReadAsArray()
    geotransform = ds.GetGeoTransform()
    projection = ds.GetProjection()
    nodata_value = ds.GetRasterBand(1).GetNoDataValue()
    
    return ds, array, geotransform, projection, nodata_value

def compare_rasters(file1, file2):
    """Compares two raster files for differences in metadata and pixel values."""
    
    # Load both rasters
    ds1, array1, gt1, proj1, nodata1 = load_raster(file1)
    ds2, array2, gt2, proj2, nodata2 = load_raster(file2)
    
    print("\n=== Comparing Raster Metadata ===")
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")
    
    # Compare metadata
    metadata_checks = {
        "Size (Width, Height)": (ds1.RasterXSize, ds1.RasterYSize) == (ds2.RasterXSize, ds2.RasterYSize),
        "Projection (CRS)": proj1 == proj2,
        "Geotransform": gt1 == gt2,
        "NoData Value": nodata1 == nodata2,
    }

    for key, match in metadata_checks.items():
        print(f"{key}: {'MATCH' if match else 'DIFFERENT'}")

    if not metadata_checks["Size (Width, Height)"]:
        print("\nRaster dimensions are different, pixel comparison may not be valid.")
        return
    
    print("\n=== Comparing Pixel Values ===")
    
    # Compute statistics
    min1, max1 = np.nanmin(array1), np.nanmax(array1)
    min2, max2 = np.nanmin(array2), np.nanmax(array2)
    unique1, unique2 = np.unique(array1), np.unique(array2)

    print(f"Min-Max Values:")
    print(f"  File 1: {min1} to {max1}")
    print(f"  File 2: {min2} to {max2}")

    print(f"\nUnique Values (First 10 shown):")
    print(f"  File 1: {unique1[:10]}")
    print(f"  File 2: {unique2[:10]}")

    # Compute absolute difference
    diff = np.abs(array1 - array2)
    
    print(f"\nDifference Stats:")
    print(f"  Mean Difference: {np.mean(diff):.4f}")
    print(f"  Max Difference: {np.max(diff):.4f}")
    print(f"  Non-zero Differences: {np.count_nonzero(diff)} pixels")

    # Optional: Visualizing Differences
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.title("Proximity - File 1")
    plt.imshow(array1, cmap="viridis")
    plt.colorbar()

    plt.subplot(1, 3, 2)
    plt.title("Proximity - File 2")
    plt.imshow(array2, cmap="viridis")
    plt.colorbar()

    plt.subplot(1, 3, 3)
    plt.title("Difference Map")
    plt.imshow(diff, cmap="coolwarm", vmin=0, vmax=np.max(diff))
    plt.colorbar()

    plt.tight_layout()
    plt.show()

# Example Usage
file1 = "data/proximity.tif"
file2 = "data/clipped_proximity.tif"

compare_rasters(file1, file2)
