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
    # Initialize risk array
    slope_risk = np.zeros_like(slope_data, dtype=int)
    
    # Classify slope into risk levels
    slope_risk[(slope_data < 5)] = 3  # High flood risk (flat areas)
    slope_risk[(slope_data >= 5) & (slope_data <= 15)] = 2  # Moderate flood risk
    slope_risk[(slope_data > 15)] = 1  # Low flood risk (steep areas)
    
    return slope_risk

# Classify the slope data
slope_risk_map = classify_slope(slope)

# 5. Visualize the Slope Map
fig, ax = plt.subplots(figsize=(10, 10))

# Plot slope with a colormap, ensuring NaN values are rendered as white
slope_cmap = plt.get_cmap('terrain').copy()
slope_cmap.set_bad(color='white')  # Set NaN values to white

img = ax.imshow(slope, cmap=slope_cmap, interpolation='bilinear', origin='upper')
ax.set_title('Slope Map (Negative Values as White)')
ax.axis('off')

# Add a colorbar for the slope map
plt.colorbar(img, ax=ax, label='Slope (degrees)')
plt.show()

# 6. Visualize the Slope Risk Map
fig, ax = plt.subplots(figsize=(10, 10))

# Define a colormap for risk levels (green for low risk, red for high risk)
risk_cmap = plt.get_cmap('RdYlGn_r').copy()  # Reverse RdYlGn for correct risk coloring
risk_cmap.set_bad(color='white')  # Set NaN to white

# Plot the slope risk map
img = ax.imshow(slope_risk_map, cmap=risk_cmap, interpolation='bilinear', origin='upper')
ax.set_title('Slope Risk Map')
ax.axis('off')

# Add a colorbar for the risk levels
cbar = plt.colorbar(img, ax=ax, label='Slope Risk Level (1=Low, 2=Moderate, 3=High)')
plt.show()
