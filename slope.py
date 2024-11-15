import numpy as np
import rasterio
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# 1. Load the DEM
dem_file_path = 'data/puneDem.tif'
with rasterio.open(dem_file_path) as dem:
    dem_data = dem.read(1).astype(float)  # Convert to float for NaN handling

# 2. Create a mask for negative values in the DEM
negative_mask = dem_data < 0

# Replace negative values with NaN
dem_data[negative_mask] = np.nan

# Optional: Apply Gaussian filter for smoothing, similar to your code
smoothed_data = gaussian_filter(dem_data, sigma=1)

# 3. Calculate the Slope from the smoothed DEM data
x_gradient, y_gradient = np.gradient(smoothed_data)

# Calculate slope as the arctangent of the gradient magnitude (in degrees)
slope = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2)) * (180 / np.pi)

# Mask the slope output where the DEM was originally negative
slope[negative_mask] = np.nan

# 4. Visualize the Slope Map with NaN values as white
fig, ax = plt.subplots(figsize=(10, 10))

# Plot slope with a colormap, ensuring NaN values are rendered as white
cmap = plt.get_cmap('terrain').copy()
cmap.set_bad(color='white')  # Set NaN values to white

# Use the masked slope data to handle NaNs
img = ax.imshow(slope, cmap=cmap, interpolation='bilinear', origin='upper')
ax.set_title('Slope Map (Negative Values as White)')
ax.axis('off')

# Add a colorbar for the slope map
cbar = plt.colorbar(img, ax=ax, label='Slope (degrees)')
plt.show()
