import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

# ===== Load and Process DEM =====
# Path to your DEM file
dem_file_path = "data/puneDem.tif"  # Ensure this path is correct

# Open the DEM file
dem_ds = gdal.Open(dem_file_path)

# Ensure DEM file is loaded correctly
if dem_ds is None:
    raise FileNotFoundError(f"DEM file not found at path: {dem_file_path}")

# Get DEM georeference info
geotransform = dem_ds.GetGeoTransform()  # Affine transformation coefficients
xmin = geotransform[0]
ymax = geotransform[3]
xres = geotransform[1]
yres = -geotransform[5]
xmax = xmin + (dem_ds.RasterXSize * xres)
ymin = ymax - (dem_ds.RasterYSize * yres)

# DEM bounds and resolution
dem_bounds = [xmin, ymin, xmax, ymax]
dem_shape = (dem_ds.RasterXSize, dem_ds.RasterYSize)  # (cols, rows)

# Read the DEM raster data as an array
dem_raster_data = dem_ds.ReadAsArray()

# Convert to float to allow assignment of NaN (as NaN can't be assigned to an integer array)
dem_raster_data = dem_raster_data.astype(float)

# Set negative values as NoData (NaN)
dem_raster_data[dem_raster_data < 0] = np.nan  # Treat negative values as NoData

# Close the DEM dataset
#dem_ds = None

# ===== Interpolate Rainfall =====
# Path to your shapefile
shapefile_path = "data/DRMS_station.shp"  # Replace with your actual shapefile path
rainfall_attribute = "rainfall"  # Replace with the name of your rainfall attribute

# Use DEM extent and resolution for interpolation
output_bounds = dem_bounds
output_width, output_height = dem_shape  # Match DEM resolution

# Perform interpolation using gdal.Grid
output_raster_path = ""  # Empty string for in-memory raster
algorithm = "invdist:power=2"  # Inverse distance weighting
# algorithm = "invdist:power=2:smoothing=1.0"  # Inverse distance weighting

grid_ds = gdal.Grid(
    output_raster_path,
    shapefile_path,
    format="MEM",  # Keep the raster in memory
    outputBounds=output_bounds,
    width=output_width,
    height=output_height,
    zfield=rainfall_attribute,
    algorithm=algorithm,
)

# Read the interpolated rainfall raster into a NumPy array
rainfall_grid = grid_ds.ReadAsArray()

# Check for negative values in the interpolated rainfall grid
if np.any(rainfall_grid < 0):
    print("Warning: Negative values detected in the interpolated rainfall grid.")
    # Optionally, set negative values to NaN
    rainfall_grid[rainfall_grid < 0] = np.nan

# Close the grid dataset
grid_ds = None

# ===== Clip Rainfall to DEM Extent =====
# Mask the rainfall grid with the DEM's valid region (NaN where DEM is NaN)
rainfall_clipped = np.where(np.isnan(dem_raster_data), np.nan, rainfall_grid)

# ===== Visualization =====
# Get the range of rainfall values
min_rainfall = np.nanmin(rainfall_clipped)
max_rainfall = np.nanmax(rainfall_clipped)

# Create subplots for side-by-side visualization
fig, axes = plt.subplots(1, 3, figsize=(20, 7))

# Plot DEM
axes[0].imshow(dem_raster_data, cmap="terrain", interpolation="nearest", extent=output_bounds)
axes[0].set_title("DEM with Negative Values as NoData")
axes[0].axis("off")
dem_cbar = fig.colorbar(plt.cm.ScalarMappable(cmap="terrain"), ax=axes[0], orientation="vertical")
dem_cbar.set_label("Elevation (m)")

# Plot Interpolated Rainfall (Unclipped)
im_rainfall_unclipped = axes[1].imshow(rainfall_grid, extent=output_bounds, origin="upper", cmap="viridis", interpolation="nearest", vmin=min_rainfall, vmax=max_rainfall)
axes[1].set_title("Interpolated Rainfall (Unclipped)")
axes[1].axis("off")
rainfall_cbar = fig.colorbar(im_rainfall_unclipped, ax=axes[1], orientation="vertical")
rainfall_cbar.set_label("Rainfall (mm)")

# Plot Interpolated Rainfall (Clipped)
im_rainfall_clipped = axes[2].imshow(rainfall_clipped, extent=output_bounds, origin="upper", cmap="viridis", interpolation="nearest", vmin=min_rainfall, vmax=max_rainfall)
axes[2].set_title("Interpolated Rainfall (Clipped to DEM)")
axes[2].axis("off")
rainfall_cbar = fig.colorbar(im_rainfall_clipped, ax=axes[2], orientation="vertical")
rainfall_cbar.set_label("Rainfall (mm)")

# Adjust layout and show the plot
plt.tight_layout()
plt.show()

# ===== Optionally Save as TIFF =====
save_as_tiff = False  # Set this flag to True if you want to save the file

if save_as_tiff:
    # Define output file path
    output_tiff_path = "data/rainfall_clipped.tif"

    # Create a new GDAL dataset for the output
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(
        output_tiff_path, 
        output_width, output_height, 
        1,  # Number of bands (1 for single band data)
        gdal.GDT_Float32  # Data type (float32)
    )

    # Set the geotransform and projection
    out_ds.SetGeoTransform(geotransform)
    out_ds.SetProjection(dem_ds.GetProjection())  # Use the DEM projection

    # Write the data to the output TIFF
    out_ds.GetRasterBand(1).WriteArray(rainfall_clipped)

    # Close the dataset
    out_ds = None
    print(f"Output saved to {output_tiff_path}")
