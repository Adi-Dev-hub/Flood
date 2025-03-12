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

# Optional: Apply Gaussian filter for smoothing
smoothed_data = gaussian_filter(dem_data, sigma=1)

# 3. Calculate the Slope from the smoothed DEM data
x_gradient, y_gradient = np.gradient(smoothed_data)

# Calculate slope as the arctangent of the gradient magnitude (in degrees)
slope = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2)) * (180 / np.pi)

# Mask the slope output where the DEM was originally negative
slope[negative_mask] = np.nan

# 4. Define slope risk categories
def classify_slope(slope_data):
    # Initialize risk array with NaN values
    slope_risk = np.full_like(slope_data, np.nan, dtype=float)
    
    # Classify slope into risk levels, skipping NaN values
    slope_risk[(~np.isnan(slope_data)) & (slope_data < 30)] = 3  # High flood risk (flat areas)
    slope_risk[(~np.isnan(slope_data)) & (slope_data >= 30) & (slope_data <= 50)] = 2  # Moderate flood risk
    slope_risk[(~np.isnan(slope_data)) & (slope_data > 50)] = 1  # Low flood risk (steep areas)
    
    return slope_risk

# Classify the slope data
slope_risk_map = classify_slope(slope)

# 5. Visualize Slope Map and Slope Risk Map side by side
fig, axes = plt.subplots(1, 2, figsize=(18, 9))

# Plot the Slope Map
slope_cmap = plt.get_cmap('terrain').copy()
slope_cmap.set_bad(color='gray')  # Set NaN values to gray
img1 = axes[0].imshow(slope, cmap=slope_cmap, interpolation='bilinear', origin='upper')
axes[0].set_title('Slope Map (NaN Values in Gray)')
axes[0].axis('off')
cbar1 = plt.colorbar(img1, ax=axes[0], label='Slope (degrees)')

# Plot the Slope Risk Map
risk_cmap = plt.get_cmap('RdYlGn_r').copy()  # Reverse RdYlGn for correct risk coloring
risk_cmap.set_bad(color='gray')  # Set NaN to gray
img2 = axes[1].imshow(slope_risk_map, cmap=risk_cmap, interpolation='bilinear', origin='upper')
axes[1].set_title('Slope Risk Map (NaN Values in Gray)')
axes[1].axis('off')
cbar2 = plt.colorbar(img2, ax=axes[1], label='Slope Risk Level (1=Low, 2=Moderate, 3=High)')

# Adjust layout and display the figure
plt.tight_layout()
plt.show()
