import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import rasterio
from matplotlib.colors import ListedColormap

# Load the DEM image
image_path = 'data/puneDem.tif'
dem_data = tiff.imread(image_path).astype(float)

# Create a mask for negative values in DEM
negative_mask = dem_data < 0
dem_data[negative_mask] = np.nan  # Replace negative values with NaN

# Apply Gaussian filter for smoothing
smoothed_data = gaussian_filter(dem_data, sigma=1)

# Function to classify flood risk based on elevation and rainfall
def classify_flood_risk(interpolated_rainfall_file):
    with rasterio.open(interpolated_rainfall_file) as src:
        rainfall_data = src.read(1).astype(float)
        transform = src.transform

    # Set negative rainfall values to zero
    rainfall_data[rainfall_data < 0] = 0

    # Define flood risk zones based on combinations of elevation and rainfall
    flood_risk = np.full(rainfall_data.shape, np.nan, dtype=np.float32)

    # Define conditions for each flood risk level (all 12 combinations)
    # Low Elevation (< 570)
    flood_risk[(smoothed_data < 570) & (rainfall_data < 10)] = 0  # No Risk
    flood_risk[(smoothed_data < 570) & (10 <= rainfall_data) & (rainfall_data < 20)] = 1  # Low Risk
    flood_risk[(smoothed_data < 570) & (20 <= rainfall_data) & (rainfall_data < 24)] = 2  # Medium Risk
    flood_risk[(smoothed_data < 570) & (rainfall_data >= 24)] = 3  # High Risk

    # Medium Elevation (570–700)
    flood_risk[(570 <= smoothed_data) & (smoothed_data < 700) & (rainfall_data < 10)] = 0  # No Risk
    flood_risk[(570 <= smoothed_data) & (smoothed_data < 700) & (10 <= rainfall_data) & (rainfall_data < 20)] = 1  # Low Risk
    flood_risk[(570 <= smoothed_data) & (smoothed_data < 700) & (20 <= rainfall_data) & (rainfall_data < 24)] = 2  # Medium Risk
    flood_risk[(570 <= smoothed_data) & (smoothed_data < 700) & (rainfall_data >= 24)] = 3  # High Risk

    # High Elevation (≥ 700)
    flood_risk[(smoothed_data >= 700) & (rainfall_data < 10)] = 0  # No Risk
    flood_risk[(smoothed_data >= 700) & (10 <= rainfall_data) & (rainfall_data < 20)] = 1  # Low Risk
    flood_risk[(smoothed_data >= 700) & (20 <= rainfall_data) & (rainfall_data < 24)] = 1  # Low Risk
    flood_risk[(smoothed_data >= 700) & (rainfall_data >= 24)] = 2  # Medium Risk

    # Handle invalid data (NaN in DEM or negative rainfall)
    flood_risk[np.isnan(smoothed_data) | (rainfall_data < 0)] = np.nan

    return flood_risk

# Usage example for rainfall prediction
interpolated_rainfall_file = 'interpolated_rainfall_resized.tif'
combined_flood_risk_zones = classify_flood_risk(interpolated_rainfall_file)

# Set up the plot for visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot the smoothed elevation map on the left
cmap_elevation = plt.get_cmap('inferno_r')
img1 = ax1.imshow(smoothed_data, cmap=cmap_elevation, interpolation='bilinear', vmin=np.nanmin(smoothed_data), vmax=np.nanmax(smoothed_data))
ax1.set_title('Smoothed Elevation Visualization')
ax1.axis('off')
cbar1 = fig.colorbar(img1, ax=ax1, label='Elevation (m)', shrink=0.8)

# Plot the combined flood risk zones map on the right
risk_cmap = ListedColormap(['lightblue', 'yellow', 'orange', 'red', 'gray'])
risk_labels = ['No Risk', 'Low Risk', 'Medium Risk', 'High Risk', 'No Data']
combined_flood_risk_zones_display = np.copy(combined_flood_risk_zones)
combined_flood_risk_zones_display[np.isnan(combined_flood_risk_zones)] = 4  # Replace NaN with a unique category for display

img2 = ax2.imshow(combined_flood_risk_zones_display, cmap=risk_cmap, interpolation='bilinear', vmin=0, vmax=4)
ax2.set_title('Combined Flood Risk Zones Heatmap')
ax2.axis('off')

# Create colorbar for combined flood risk zones and set labels
cbar2 = fig.colorbar(img2, ax=ax2, ticks=[0, 1, 2, 3, 4], label='Flood Risk Level')
cbar2.ax.set_yticklabels(risk_labels)

plt.show()
