import numpy as np
import rasterio
import matplotlib.pyplot as plt
from scipy.ndimage import distance_transform_edt

# Step 1: Load the LULC raster data
lulc_raster_path = 'data/ps1.tif'

with rasterio.open(lulc_raster_path) as src:
    lulc_data = src.read(1)  # Read the first band
    profile = src.profile  # Store metadata for later use

# Step 2: Identify water body pixels (assuming blue is represented by a specific value)
water_body_value = 233  # Adjust this based on your dataset

# Create a binary mask where water bodies are located
water_mask = np.where(lulc_data == water_body_value, 1, 0)

# Step 3: Generate proximity map using distance transform
# The distance transform calculates the distance to the nearest non-zero pixel (water body)
proximity_map = distance_transform_edt(1 - water_mask)

# Step 4: Display both LULC and proximity maps using Matplotlib
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

# Display LULC Map
ax[0].imshow(lulc_data, cmap='tab10')  # Use a colormap suitable for your LULC classes
ax[0].set_title('LULC Map')
ax[0].axis('off')  # Hide axes

# Display Proximity Map
ax[1].imshow(proximity_map, cmap='viridis')  # Use a colormap for proximity
ax[1].set_title('Proximity Map to Water Bodies')
ax[1].axis('off')  # Hide axes

plt.tight_layout()
plt.show()
