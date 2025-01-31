import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal

def assign_integers_to_unique_colors_and_create_new_raster(lulc_file, output_file):
    # Open the LULC raster file with GDAL
    dataset = gdal.Open(lulc_file)
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
    
    # Flatten the RGB image to a 2D array of pixels (each row is [R, G, B])
    flattened_pixels = rgb_image.reshape(-1, 3)
    
    # Create a dictionary to store unique colors and their assigned integers
    unique_colors = {}
    color_id = 0
    
    # Assign integers to each unique color
    for pixel in flattened_pixels:
        pixel_tuple = tuple(pixel)
        if pixel_tuple not in unique_colors:
            unique_colors[pixel_tuple] = color_id
            color_id += 1
    
    # Create a new raster to store the integer values
    driver = gdal.GetDriverByName('GTiff')
    if driver is None:
        raise ValueError("GDAL driver for GTiff not available.")
    
    # Create a new dataset with the same dimensions and georeference as the original
    new_dataset = driver.Create(output_file, dataset.RasterXSize, dataset.RasterYSize, 4, gdal.GDT_UInt32)
    new_dataset.SetGeoTransform(dataset.GetGeoTransform())
    new_dataset.SetProjection(dataset.GetProjection())
    
    # Write the original RGB channels to the first 3 bands
    for i in range(3):
        new_band = new_dataset.GetRasterBand(i + 1)
        new_band.WriteArray(bands[i])
        new_band.SetNoDataValue(-1)
    
    # Create an array of integers to store in the fourth band
    integer_image = np.zeros_like(rgb_image[..., 0], dtype=np.uint32)  # Initialize with zeros
    
    # Assign the corresponding integer values to the integer_image
    for i, pixel in enumerate(flattened_pixels):
        color_tuple = tuple(pixel)
        integer_image.reshape(-1)[i] = unique_colors[color_tuple]
    
    # Write the integer values to the fourth band
    new_band = new_dataset.GetRasterBand(4)
    new_band.WriteArray(integer_image)
    new_band.SetNoDataValue(-1)
    
    # Save the changes and close the dataset
    new_dataset.FlushCache()
    
    # Close the datasets
    dataset = None
    new_dataset = None
    
    # Return the dictionary of unique colors and the total pixels
    total_pixels = flattened_pixels.shape[0]  # Total number of pixels
    return unique_colors, total_pixels, rgb_image, integer_image

# Path to your LULC raster file and output file
lulc_file = 'data/PuneLuLc.tif'
output_file = 'data/PuneLuLc_with_integers.tif'

# Call the function to assign integers to the unique colors and create a new raster
unique_colors, total_pixels, rgb_image, integer_image = assign_integers_to_unique_colors_and_create_new_raster(lulc_file, output_file)

# Print the total number of unique colors and pixels
print(f"Total unique colors: {len(unique_colors)}")
print(f"Total number of pixels: {total_pixels}")
print("Sample of assigned integers for colors:")
for color, color_id in list(unique_colors.items())[:10]:  # Display the first 10 unique colors
    print(f"Color {color}: {color_id}")

# Display the LULC image (original colors)
plt.imshow(rgb_image)
plt.title("LULC Image")
plt.axis('off')  # Hide axes
plt.show()

# Display the new integer values image (just for visualization)
plt.imshow(integer_image, cmap='viridis')
plt.title("Integer Values Image")
plt.axis('off')  # Hide axes
plt.show()
