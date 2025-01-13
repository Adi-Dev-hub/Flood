import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

def analyze_lulc_colors(lulc_file):
    # Open the LULC raster file with GDAL
    dataset = gdal.Open(lulc_file)
    if dataset is None:
        raise ValueError("Could not open the LULC file.")
    
    # Get the number of bands in the dataset
    num_bands = dataset.RasterCount
    print(f"Number of bands: {num_bands}")
    
    if num_bands < 3:
        raise ValueError("The file doesn't have enough bands to form an RGB image.")

    # Read the bands into separate channels (assuming the first 3 bands are RGB)
    bands = []
    for i in range(1, 4):  # First 3 bands for RGB
        band = dataset.GetRasterBand(i)
        band_data = band.ReadAsArray()

        # Handle NoData values
        nodata = band.GetNoDataValue()
        if nodata is not None:
            band_data[band_data == nodata] = 0

        # Normalize if needed and convert to uint8
        band_data = np.clip(band_data, 0, 255).astype(np.uint8)
        bands.append(band_data)

    # Stack the RGB channels to create a color image
    rgb_image = np.dstack(bands)

    # Flatten the RGB image to a 2D array of pixels (each row is [R, G, B])
    flattened_pixels = rgb_image.reshape(-1, 3)

    # Find unique colors and their counts
    unique_colors, counts = np.unique(flattened_pixels, axis=0, return_counts=True)

    # Create a dictionary with indices assigned to each unique color
    color_to_index = {tuple(color): index for index, color in enumerate(unique_colors)}

    # Total number of pixels in the raster
    total_pixels = rgb_image.shape[0] * rgb_image.shape[1]

    # Verify if the sum of all counts equals the total number of pixels
    assert np.sum(counts) == total_pixels, "Pixel counts do not match the total number of pixels!"
    assert len(color_to_index) == len(unique_colors), "Mismatch in dictionary size and unique colors!"

    print(f"Total unique colors: {len(unique_colors)}")
    print(f"Total pixels: {total_pixels}")
    print("Verification successful: Pixel counts match the total number of pixels.")
    print("Verification successful: Dictionary key-value pairs match the number of unique colors.")

    # Input field to query the RGB value
    while True:
        query = input("Enter an RGB value (e.g., 255,255,255) to get its assigned integer, or type 'exit' to quit: ")
        if query.lower() == 'exit':
            break
        try:
            rgb = tuple(map(int, query.split(',')))
            if rgb in color_to_index:
                print(f"Assigned integer for {rgb}: {color_to_index[rgb]}")
            else:
                print(f"RGB value {rgb} not found in the dataset.")
        except ValueError:
            print("Invalid input. Please enter RGB values in the format 'R,G,B'.")
    
    # Display the original RGB image
    plt.imshow(rgb_image)
    plt.title("Original RGB Image")
    plt.axis('off')  # Hide axes
    plt.show()

# Path to your LULC raster file
lulc_file = 'data/data.tif'

# Call the function to analyze the LULC raster
analyze_lulc_colors(lulc_file)
