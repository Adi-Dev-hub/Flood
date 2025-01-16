import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from matplotlib.colors import ListedColormap
import sys

# Load the DEM image
image_path = sys.argv[1] if len(sys.argv) > 1 else 'data/puneDem.tif'
try:
    dem_data = tiff.imread(image_path).astype(float)  # Convert to float for NaN handling
except FileNotFoundError:
    print(f"Error: File not found at {image_path}")
    sys.exit(1)
except Exception as e:
    print(f"Error loading file: {e}")
    sys.exit(1)

# Create a mask for negative values
negative_mask = dem_data < 0

# Replace negative values with NaN
dem_data[negative_mask] = np.nan

# Apply Gaussian filter for smoothing (adjust sigma for more or less smoothing)
sigma = 1
smoothed_data = gaussian_filter(dem_data, sigma=sigma)

# Define flood risk zones based on smoothed data
low_risk_threshold = 700
moderate_risk_threshold = 570

flood_risk_zones = np.zeros_like(smoothed_data)
flood_risk_zones[(smoothed_data < moderate_risk_threshold) & (smoothed_data > 0)] = 3  # High risk
flood_risk_zones[(smoothed_data >= moderate_risk_threshold) & (smoothed_data < low_risk_threshold)] = 2  # Moderate risk
flood_risk_zones[smoothed_data >= low_risk_threshold] = 1  # Low risk

# Set areas where the original DEM was negative to NaN in flood risk zones
flood_risk_zones[negative_mask] = np.nan

# Apply Gaussian filter to flood risk zones for smooth heatmap effect
smoothed_flood_risk_zones = gaussian_filter(flood_risk_zones, sigma=sigma)

# Set up the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot the elevation map on the left
cmap = plt.get_cmap('inferno_r')
img1 = ax1.imshow(smoothed_data, cmap=cmap, interpolation='bilinear', vmin=np.nanmin(smoothed_data), vmax=np.nanmax(smoothed_data))
ax1.set_title('Smoothed Elevation Visualization')
ax1.axis('off')
cbar1 = fig.colorbar(img1, ax=ax1, label='Elevation (m)', shrink=0.8)

# Plot the smoothed flood risk zones map on the right
custom_cmap = ListedColormap(['green', 'yellow', 'red'])
img2 = ax2.imshow(smoothed_flood_risk_zones, cmap=custom_cmap, interpolation='bilinear', vmin=1, vmax=3)
ax2.set_title('Flood Risk Zones Heatmap')
ax2.axis('off')

# Create colorbar for flood risk zones and set labels
cbar2 = fig.colorbar(img2, ax=ax2, ticks=[1, 2, 3], label='Flood Risk', shrink=0.8)
cbar2.ax.set_yticklabels(['Low Risk', 'Moderate Risk', 'High Risk'])

# Save the plots as an image file
plt.savefig('flood_risk_map.png', dpi=300)
plt.show()
