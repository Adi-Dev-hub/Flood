import numpy as np
from osgeo import gdal

def check_integer_values_in_new_file(lulc_file_with_integers):
    # Open the LULC file with assigned integers
    dataset = gdal.Open(lulc_file_with_integers)
    if dataset is None:
        raise ValueError("Could not open the LULC file.")
    
    # Get the number of bands in the dataset
    num_bands = dataset.RasterCount
    if num_bands < 3:
        raise ValueError("The file doesn't have enough bands to form an RGB image.")
    
    # Read the bands into separate channels (assuming the first 3 bands are RGB)
    bands = []
    for i in range(1, 4):  # First 3 bands for RGB
        band = dataset.GetRasterBand(i)
        band_data = band.ReadAsArray()
        nodata = band.GetNoDataValue()
        if nodata is not None:
            band_data[band_data == nodata] = 0
        bands.append(band_data)
    
    # Stack the RGB channels to create a color image
    rgb_image = np.dstack(bands)
    
    # Read the integer values from the 4th band (if exists)
    band = dataset.GetRasterBand(4)
    integer_image = band.ReadAsArray()
    
    # Create a dictionary of RGB colors to their assigned integers
    color_to_integer = {}
    for i in range(rgb_image.shape[0]):
        for j in range(rgb_image.shape[1]):
            color_tuple = tuple(rgb_image[i, j])
            if color_tuple not in color_to_integer:
                color_to_integer[color_tuple] = integer_image[i, j]
    
    # Prompt user for input RGB color and output corresponding integer
    while True:
        user_input = input("Enter an RGB value (e.g., 255,255,255) to get its assigned integer, or type 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break
        
        try:
            rgb_input = tuple(map(int, user_input.split(',')))
            if rgb_input in color_to_integer:
                print(f"Assigned integer for {rgb_input}: {color_to_integer[rgb_input]}")
            else:
                print(f"RGB color {rgb_input} not found in the file.")
        except ValueError:
            print("Invalid input. Please enter RGB values in the format 'R,G,B'.")

# Path to the LULC raster file with assigned integers (new file)
lulc_file_with_integers = 'data/PuneLuLc_with_integers.tif'

# Call the function to check the integer values in the file
check_integer_values_in_new_file(lulc_file_with_integers)
