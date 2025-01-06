import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal

def combine_and_display_rgb_image(lulc_file):
    # Open the LULC raster file with GDAL
    dataset = gdal.Open(lulc_file)
    if dataset is None:
        raise ValueError("Could not open the LULC file.")
    
    # Get the number of bands in the dataset
    num_bands = dataset.RasterCount
    print(f"Number of bands: {num_bands}")
    
    if num_bands < 3:
        print("The file doesn't have enough bands to form an RGB image.")
        return

    # Read the bands into separate channels (assuming the first 3 bands are RGB)
    red_band = dataset.GetRasterBand(1).ReadAsArray()
    green_band = dataset.GetRasterBand(2).ReadAsArray()
    blue_band = dataset.GetRasterBand(3).ReadAsArray()

    # Check the type and shape of each band
    print("Red band type:", red_band.dtype)
    print("Green band type:", green_band.dtype)
    print("Blue band type:", blue_band.dtype)
    print("Red band shape:", red_band.shape)
    print("Green band shape:", green_band.shape)
    print("Blue band shape:", blue_band.shape)

    # Set NoData values to 0 for proper visualization
    red_band = np.nan_to_num(red_band, nan=0)
    green_band = np.nan_to_num(green_band, nan=0)
    blue_band = np.nan_to_num(blue_band, nan=0)

    # Normalize the bands to 0-255 range (if they are float)
    red_band = np.clip(red_band, 0, 255).astype(np.uint8)
    green_band = np.clip(green_band, 0, 255).astype(np.uint8)
    blue_band = np.clip(blue_band, 0, 255).astype(np.uint8)

    # Stack the RGB channels to create a color image
    rgb_image = np.dstack((red_band, green_band, blue_band))

    # Display using matplotlib
    plt.imshow(rgb_image)
    plt.title("RGB Image")
    plt.axis('off')  # Hide axes
    plt.show()

    

# Path to your LULC raster file
lulc_file = 'data/data.tif'

# Call the function to combine and display the RGB image
combine_and_display_rgb_image(lulc_file)
