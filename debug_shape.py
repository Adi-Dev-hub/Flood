from osgeo import gdal

# Path to your DEM file
dem_file_path = "data/puneDem.tif"  # Replace with the actual DEM file path

# Open the DEM file
dem_ds = gdal.Open(dem_file_path)

# Ensure DEM file is loaded correctly
if dem_ds is None:
    raise FileNotFoundError(f"DEM file not found at path: {dem_file_path}")

# Extract width and height
width = dem_ds.RasterXSize  # Number of columns (Width)
height = dem_ds.RasterYSize  # Number of rows (Height)

# Close the dataset
dem_ds = None

# Print the results
print(f"Width (RasterXSize): {width}")
print(f"Height (RasterYSize): {height}")
