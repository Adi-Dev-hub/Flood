import numpy as np
import rasterio
from collections import Counter

# Define the path to your LULC raster file
lulc_file = 'data/PuneLuLc.tif'

# Open the LULC raster file
with rasterio.open(lulc_file) as src:
    # Read the bands (assuming it's a 4-band image)
    bands = [src.read(i+1) for i in range(4)]  # 1-indexed, so read i+1
    # Stack the bands together into a 3D array (rows x cols x bands)
    img = np.stack(bands, axis=-1)

# Reshape the image to a 2D array (pixels x bands)
reshaped_img = img.reshape(-1, 4)

# Convert the array into RGB by selecting the appropriate bands (e.g., bands 1, 2, and 3 for RGB)
# If your bands are in a different order or different interpretation, adjust accordingly
rgb_values = reshaped_img[:, :3]  # Assuming bands 1, 2, 3 are RGB

# Normalize to 8-bit integers for RGB (if required)
rgb_values = np.clip(rgb_values, 0, 255).astype(np.uint8)

# Get unique RGB values
unique_rgb = np.unique(rgb_values, axis=0)

# Count the occurrence of each unique RGB value
rgb_counter = Counter(tuple(row) for row in unique_rgb)

# Print the unique RGB values and their counts
for color, count in rgb_counter.items():
    print(f"RGB: {color} - Count: {count}")
    
