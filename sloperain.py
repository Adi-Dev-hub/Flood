import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter

# 1. Load the DEM
dem_file_path = 'data/puneDem.tif'
with rasterio.open(dem_file_path) as dem:
    dem_data = dem.read(1).astype(float)  # Convert to float for NaN handling

# 2. Mask for negative values in the DEM
negative_mask = dem_data < 0
dem_data[negative_mask] = np.nan

# Optional: Apply Gaussian filter for smoothing
smoothed_data = gaussian_filter(dem_data, sigma=1)

# 3. Calculate the Slope
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
flood_risk_map[rainfall_data >= 26] = 3  # High risk
flood_risk_map[(rainfall_data >= 22) & (rainfall_data < 26)] = 2  # Medium risk
flood_risk_map[ (rainfall_data < 22)] = 1  # Low risk
flood_risk_map[np.isnan(rainfall_data)] = 4  # No Data

# 6. Combine Risks with Weights
def combine_risks_weighted(slope_risk, rainfall_risk, weight_slope=0.4, weight_rainfall=0.6):
    """
    Combines slope risk and rainfall risk using a weighted approach.
    """
    # Initialize combined risk map with NaN
    combined_risk = np.full_like(slope_risk, np.nan, dtype=float)

    # Create a mask for valid data in both maps
    valid_mask = (~np.isnan(slope_risk)) & (~np.isnan(rainfall_risk))

    # Apply the weighted combination for valid pixels
    combined_risk[valid_mask] = (
        weight_slope * slope_risk[valid_mask] +
        weight_rainfall * rainfall_risk[valid_mask]
    )

    # Round to the nearest integer to match risk levels
    combined_risk = np.round(combined_risk).astype(float)

    # Ensure NaN propagation for invalid areas
    combined_risk[~valid_mask] = np.nan

    return combined_risk

combined_risk_map = combine_risks_weighted(slope_risk_map, flood_risk_map, weight_slope=0.4, weight_rainfall=0.6)

# 7. Visualize Only Slope Map and Combined Risk Map
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Slope Map
slope_cmap = plt.get_cmap('terrain').copy()
slope_cmap.set_bad(color='gray')
img1 = axes[0].imshow(slope, cmap=slope_cmap, interpolation='bilinear', origin='upper')
axes[0].set_title('Slope Map (NaN Values in Gray)')
axes[0].axis('off')
plt.colorbar(img1, ax=axes[0], label='Slope (degrees)')

# Combined Risk Map
combined_cmap = ListedColormap([ 'yellow', 'orange', 'red', 'gray'])
combined_labels = [ 'Low Risk', 'Medium Risk', 'High Risk', 'No Data']
img2 = axes[1].imshow(combined_risk_map, cmap=combined_cmap, origin='upper', extent=(
    transform[2], transform[2] + transform[0] * combined_risk_map.shape[1],
    transform[5] + transform[4] * combined_risk_map.shape[0], transform[5]
))
axes[1].set_title('Combined Risk Map (NaN Values in Gray)')
axes[1].axis('off')
cbar2 = plt.colorbar(img2, ax=axes[1], ticks=[ 1, 2, 3, 4])
cbar2.ax.set_yticklabels(combined_labels)
cbar2.set_label("Combined Risk Level")

plt.tight_layout()
plt.show()
