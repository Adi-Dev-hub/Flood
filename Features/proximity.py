from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

# File paths
lulc_file = "data/PuneLuLc_with_integers.tif"
output_proximity_file = "data/Cproximity.tif"  # Optional output file for proximity raster

# Target values in the 4th band of LULC
target_values = [330, 316]

# Load LULC dataset
lulc_dataset = gdal.Open(lulc_file)
lulc_geo_transform = lulc_dataset.GetGeoTransform()
lulc_projection = lulc_dataset.GetProjection()
lulc_band_4 = lulc_dataset.GetRasterBand(4).ReadAsArray()

# Create a mask for target values
mask_data = np.isin(lulc_band_4, target_values).astype("uint8")

# Debugging: Check mask stats
print("Mask Debugging:")
print(f"  Unique values in mask: {np.unique(mask_data)}")
print(f"  Total target pixels: {np.sum(mask_data)}")

# Create an in-memory raster for mask
driver = gdal.GetDriverByName("MEM")



# Create an in-memory raster for proximity
proximity_dataset = driver.Create(
    "", lulc_dataset.RasterXSize, lulc_dataset.RasterYSize, 1, gdal.GDT_Float32
)
proximity_dataset.SetGeoTransform(lulc_geo_transform)
proximity_dataset.SetProjection(lulc_projection)

# Compute proximity
gdal.ComputeProximity(
    lulc_dataset.GetRasterBand(4),
    proximity_dataset.GetRasterBand(1),
    ["DISTUNITS=GEO", "NODATA=0", "VALUES=330,316"],
)

# Read proximity data
proximity_data = proximity_dataset.GetRasterBand(1).ReadAsArray()

# Debugging: Check proximity stats
print("Proximity Debugging:")
print(f"  Min value: {np.min(proximity_data)}")
print(f"  Max value: {np.max(proximity_data)}")
print(f"  Mean value: {np.mean(proximity_data)}")
print(f"  Total cells: {proximity_data.size}")
print(f"  Cells with no data: {np.sum(np.isnan(proximity_data))}")


# Optionally save the proximity raster
if output_proximity_file:
    proximity_driver = gdal.GetDriverByName("GTiff")
    saved_proximity_dataset = proximity_driver.Create(
        output_proximity_file,
        proximity_dataset.RasterXSize,
        proximity_dataset.RasterYSize,
        1,
        gdal.GDT_Float32,
    )
    saved_proximity_dataset.SetGeoTransform(proximity_dataset.GetGeoTransform())
    saved_proximity_dataset.SetProjection(proximity_dataset.GetProjection())
    saved_proximity_dataset.GetRasterBand(1).WriteArray(proximity_data)
    saved_proximity_dataset.GetRasterBand(1).SetNoDataValue(-1)
    saved_proximity_dataset = None  # Close the file
    print(f"Proximity raster saved to: {output_proximity_file}")

# Visualize mask and proximity data
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Mask")
plt.imshow(mask_data, cmap="gray", interpolation="nearest")
plt.colorbar(label="Mask Values")
plt.subplot(1, 2, 2)
plt.title("Proximity Raster")
plt.imshow(proximity_data, cmap="viridis", interpolation="nearest")
plt.colorbar(label="Proximity (Distance in Pixels)")
plt.show()

# Clean up
lulc_dataset = None
proximity_dataset = None
