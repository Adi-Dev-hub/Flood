from osgeo import gdal
import numpy as np

# Function to map RGB to PCT and save it
def rgb_to_pct(input_tif, output_tif):
    # Open the input raster
    dataset = gdal.Open(input_tif)
    if dataset is None:
        raise ValueError("Could not open the input raster file.")

    # Read the red, green, and blue bands
    red_band = dataset.GetRasterBand(1)
    green_band = dataset.GetRasterBand(2)
    blue_band = dataset.GetRasterBand(3)

    red_data = red_band.ReadAsArray()
    green_data = green_band.ReadAsArray()
    blue_data = blue_band.ReadAsArray()

    # Stack the RGB bands into a 3D array
    rgb_data = np.stack((red_data, green_data, blue_data), axis=-1)

    # Create a dictionary to store the unique RGB values and map them to unique integers
    rgb_to_int = {}
    current_int = 0

    # Loop through the RGB data and assign a unique integer to each unique RGB value
    pct_data = np.zeros(rgb_data.shape[:2], dtype=np.uint8)  # Output single band array
    for i in range(rgb_data.shape[0]):
        for j in range(rgb_data.shape[1]):
            rgb_tuple = tuple(rgb_data[i, j])
            if rgb_tuple not in rgb_to_int:
                rgb_to_int[rgb_tuple] = current_int
                current_int += 1
            pct_data[i, j] = rgb_to_int[rgb_tuple]

    # Create a new dataset to save the output PCT image
    driver = gdal.GetDriverByName('GTiff')
    if driver is None:
        raise ValueError("GDAL driver for GeoTIFF not found.")

    # Create the output raster with the same dimensions and georeferencing as the input
    out_dataset = driver.Create(output_tif, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte)

    # Set georeferencing information (same as the input raster)
    out_dataset.SetGeoTransform(dataset.GetGeoTransform())
    out_dataset.SetProjection(dataset.GetProjection())

    # Write the PCT data to the output band
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(pct_data)

    # Optionally, you can set the color table (PCT) for visualization
    color_table = gdal.ColorTable()
    for i, rgb_tuple in enumerate(rgb_to_int.keys()):
        color_table.SetColorEntry(i, rgb_tuple)  # Map integer value to RGB color

    out_band.SetColorTable(color_table)

    # Close the datasets
    out_dataset = None
    dataset = None
    print(f"RGB to PCT conversion completed. Output saved at {output_tif}")

# Path to your input and output raster files
input_tif = 'data/data.tif'
output_tif = 'output_raster_with_pct.tif'

# Perform the RGB to PCT conversion
rgb_to_pct(input_tif, output_tif)
