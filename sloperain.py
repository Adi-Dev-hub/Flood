import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter

# 1. Load the DEM
dem_file_path = 'data/puneDem.tif'
with rasterio.open(dem_file_path) as dem:
    dem_data = dem.read(1).astype(float)  # Convert to float for NaN handling

# 2. Create a mask for negative values in the DEM
negative_mask = dem_data < 0
dem_data[negative_mask] = np.nan

# Optional: Apply Gaussian filter for smoothing
smoothed_data = gaussian_filter(dem_data, sigma=1)

# 3. Calculate the Slope from the smoothed DEM data
x_gradient, y_gradient = np.gradient(smoothed_data)
slope = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2)) * (180 / np.pi)
slope[negative_mask] = np.nan

# 4. Define slope risk categories
def classify_slope(slope_data):
    slope_risk = np.zeros_like(slope_data, dtype=int)
    slope_risk[(slope_data < 30)] = 3  # High flood risk (flat areas)
    slope_risk[(slope_data >= 30) & (slope_data <= 50)] = 2  # Moderate flood risk
    slope_risk[(slope_data > 50)] = 1  # Low flood risk (steep areas)
    slope_risk[np.isnan(slope_data)] = 4  # NaN as No Data
    return slope_risk

slope_risk_map = classify_slope(slope)

# 5. Load the Interpolated Rainfall Data
interpolated_rainfall_file = 'interpolated_rainfall_resized.tif'
with rasterio.open(interpolated_rainfall_file) as src:
    rainfall_data = src.read(1).astype(float)  # Ensure float type for NaN handling
    transform = src.transform

rainfall_data[rainfall_data < 0] = 0

# Define rainfall flood risk categories
flood_risk_map = np.zeros_like(rainfall_data, dtype=np.uint8)
flood_risk_map[rainfall_data >= 24] = 3  # High risk
flood_risk_map[(rainfall_data >= 20) & (rainfall_data < 24)] = 2  # Medium risk
flood_risk_map[(rainfall_data >= 10) & (rainfall_data < 20)] = 1  # Low risk
flood_risk_map[np.isnan(rainfall_data)] = 4  # No Data

# 6. Combine Slope Risk and Flood Risk Maps
def combine_risks(slope_risk, flood_risk):
    combined_risk = np.full_like(slope_risk, np.nan)
    valid_mask = (~np.isnan(slope_risk)) & (~np.isnan(flood_risk))
    combined_risk[valid_mask] = np.maximum(slope_risk[valid_mask], flood_risk[valid_mask])
    return combined_risk

combined_risk_map = combine_risks(slope_risk_map, flood_risk_map)

# 7. Visualize All Maps
fig, axes = plt.subplots(1, 4, figsize=(32, 8))

# Slope Map
slope_cmap = plt.get_cmap('terrain').copy()
slope_cmap.set_bad(color='gray')
img1 = axes[0].imshow(slope, cmap=slope_cmap, interpolation='bilinear', origin='upper')
axes[0].set_title('Slope Map (NaN Values in Gray)')
axes[0].axis('off')
plt.colorbar(img1, ax=axes[0], label='Slope (degrees)')

# Slope Risk Map
risk_cmap = plt.get_cmap('RdYlGn_r').copy()
risk_cmap.set_bad(color='gray')
img2 = axes[1].imshow(slope_risk_map, cmap=risk_cmap, interpolation='bilinear', origin='upper')
axes[1].set_title('Slope Risk Map (NaN Values in Gray)')
axes[1].axis('off')
plt.colorbar(img2, ax=axes[1], label='Slope Risk Level (1=Low, 2=Moderate, 3=High)')

# Flood Risk Map
flood_cmap = ListedColormap(['lightblue', 'yellow', 'orange', 'red', 'gray'])
flood_labels = ['No Risk', 'Low Risk', 'Medium Risk', 'High Risk', 'No Data']
img3 = axes[2].imshow(flood_risk_map, cmap=flood_cmap, origin='upper', extent=(
    transform[2], transform[2] + transform[0] * flood_risk_map.shape[1],
    transform[5] + transform[4] * flood_risk_map.shape[0], transform[5]
))
axes[2].set_title('Flood Risk Map (NaN Values in Gray)')
axes[2].axis('off')
cbar3 = plt.colorbar(img3, ax=axes[2], ticks=[0, 1, 2, 3, 4])
cbar3.ax.set_yticklabels(flood_labels)
cbar3.set_label("Flood Risk Level")

# Combined Risk Map
combined_cmap = ListedColormap(['lightblue', 'yellow', 'orange', 'red', 'gray'])
combined_labels = ['No Risk', 'Low Risk', 'Medium Risk', 'High Risk', 'No Data']
img4 = axes[3].imshow(combined_risk_map, cmap=combined_cmap, origin='upper', extent=(
    transform[2], transform[2] + transform[0] * combined_risk_map.shape[1],
    transform[5] + transform[4] * combined_risk_map.shape[0], transform[5]
))
axes[3].set_title('Combined Risk Map (NaN Values in Gray)')
axes[3].axis('off')
cbar4 = plt.colorbar(img4, ax=axes[3], ticks=[0, 1, 2, 3, 4])
cbar4.ax.set_yticklabels(combined_labels)
cbar4.set_label("Combined Risk Level")

plt.tight_layout()
plt.show()
