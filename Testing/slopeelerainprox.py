import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter

# Load the DEM for Slope and Elevation Analysis
dem_file_path = 'data/puneDem.tif'
with rasterio.open(dem_file_path) as dem:
    dem_data = dem.read(1).astype(float)  # Convert to float for NaN handling

# Create a mask for negative values in the DEM
negative_mask = dem_data < 0
dem_data[negative_mask] = np.nan

# Apply Gaussian filter for smoothing (optional)
smoothed_data = gaussian_filter(dem_data, sigma=1)

# Calculate the Slope
x_gradient, y_gradient = np.gradient(smoothed_data)
slope = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2)) * (180 / np.pi)
slope[negative_mask] = np.nan

# Define the Slope Risk Categories
def classify_slope(slope_data):
    slope_risk = np.zeros_like(slope_data, dtype=int)
    slope_risk[(slope_data < 20)] = 3  # High flood risk (flat areas)
    slope_risk[(slope_data >= 20) & (slope_data <= 40)] = 2  # Moderate flood risk
    slope_risk[(slope_data > 40)] = 1  # Low flood risk (steep areas)
    slope_risk[np.isnan(slope_data)] = 4  # No Data
    return slope_risk

slope_risk_map = classify_slope(slope)

# Load the Interpolated Rainfall Data
interpolated_rainfall_file = 'data/rainfall_clipped.tif'
with rasterio.open(interpolated_rainfall_file) as src:
    rainfall_data = src.read(1).astype(float)  # Ensure float type for NaN handling
    transform = src.transform

rainfall_data[rainfall_data < 0] = 0

# Define Rainfall Flood Risk Categories
def classify_rainfall(rainfall_data):
    flood_risk_map = np.zeros_like(rainfall_data, dtype=np.uint8)
    flood_risk_map[rainfall_data >= 40] = 3  # High risk
    flood_risk_map[(rainfall_data >= 20) & (rainfall_data < 40)] = 2  # Medium risk
    flood_risk_map[(rainfall_data < 20)] = 1  # Low risk
    flood_risk_map[np.isnan(rainfall_data)] = 4  # No Data
    return flood_risk_map

flood_risk_map = classify_rainfall(rainfall_data)

# Elevation Risk Classification
def classify_elevation(elevation_data):
    elevation_risk = np.zeros_like(elevation_data, dtype=int)
    elevation_risk[(elevation_data < 570) & (elevation_data > 0)] = 3  # Low elevation, High flood risk
    elevation_risk[(elevation_data >= 570) & (elevation_data < 700)] = 2  # Mid elevation, Moderate risk
    elevation_risk[elevation_data >= 700] = 1  # High elevation, Low flood risk
    elevation_risk[np.isnan(elevation_data)] = 4  # No Data
    return elevation_risk

elevation_risk_map = classify_elevation(smoothed_data)

# Load and Validate Proximity Map
proximity_file_path = 'data/proximity.tif'
with rasterio.open(proximity_file_path) as src:
    proximity_data = src.read(1).astype(float)  # Ensure float type for NaN handling

# Check if proximity data is within 0 to 1
if np.nanmax(proximity_data) > 1 or np.nanmin(proximity_data) < 0:
    print("Proximity data is not scaled between 0 and 1. Normalizing...")
    proximity_data = (proximity_data - np.nanmin(proximity_data)) / (np.nanmax(proximity_data) - np.nanmin(proximity_data))

# Handle uniform data case
if np.nanmax(proximity_data) == np.nanmin(proximity_data):
    proximity_data[:] = np.nan  # Assign a default value

# Define Proximity Risk Categories
proximity_risk_map = np.zeros_like(proximity_data, dtype=int)
proximity_risk_map[proximity_data < 0.3] = 3  # Close to water bodies, high flood risk
proximity_risk_map[(proximity_data >= 0.3) & (proximity_data < 0.7)] = 2  # Moderate proximity, moderate risk
proximity_risk_map[proximity_data >= 0.7] = 1  # Far from water bodies, low risk
proximity_risk_map[np.isnan(proximity_data)] = 4  # No Data

# Combine Risks Using Weights
def combine_risks_weighted(slope_risk, rainfall_risk, elevation_risk, proximity_risk, weight_slope=0.2, weight_rainfall=0.35, weight_elevation=0.2, weight_proximity=0.25):
    total_weight = weight_slope + weight_rainfall + weight_elevation + weight_proximity
    assert np.isclose(total_weight, 1), "Weights must sum up to 1."

    # Initialize combined risk map with NaN
    combined_risk = np.full_like(slope_risk, np.nan, dtype=float)

    # Create a mask for valid data in all maps
    valid_mask = (
        (~np.isnan(slope_risk)) &
        (~np.isnan(rainfall_risk)) &
        (~np.isnan(elevation_risk)) &
        (~np.isnan(proximity_risk))
    )

    # Apply the weighted combination for valid pixels
    combined_risk[valid_mask] = (
        weight_slope * slope_risk[valid_mask] +
        weight_rainfall * rainfall_risk[valid_mask] +
        weight_elevation * elevation_risk[valid_mask] +
        weight_proximity * proximity_risk[valid_mask]
    )

    # Round to the nearest integer to match risk levels
    combined_risk = np.round(combined_risk).astype(float)

    # Ensure NaN propagation for invalid areas
    combined_risk[~valid_mask] = np.nan

    return combined_risk

# Combine all risks with their respective weights
combined_risk_map = combine_risks_weighted(
    slope_risk_map,
    flood_risk_map,
    elevation_risk_map,
    proximity_risk_map,
    weight_slope=0.2,
    weight_rainfall=0.35,
    weight_elevation=0.2,
    weight_proximity=0.25
)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Slope Map
slope_cmap = plt.get_cmap('terrain').copy()
slope_cmap.set_bad(color='gray')
img1 = axes[0].imshow(slope, cmap=slope_cmap, interpolation='bilinear', origin='upper')
axes[0].set_title('Slope Map (NaN Values in Gray)')
axes[0].axis('off')
plt.colorbar(img1, ax=axes[0], label='Slope (degrees)')

# Combined Risk Map
combined_cmap = ListedColormap(['yellow', 'orange', 'red', 'gray'])
combined_labels = ['Low Risk', 'Moderate Risk', 'High Risk', 'No Data']
img2 = axes[1].imshow(combined_risk_map, cmap=combined_cmap, origin='upper', extent=(
    transform[2], transform[2] + transform[0] * combined_risk_map.shape[1],
    transform[5] + transform[4] * combined_risk_map.shape[0], transform[5]
))
axes[1].set_title('Combined Risk Map (NaN Values in Gray)')
axes[1].axis('off')
cbar2 = plt.colorbar(img2, ax=axes[1], ticks=[1, 2, 3, 4], label='Combined Risk Level')
cbar2.ax.set_yticklabels(['Low Risk', 'Moderate Risk', 'High Risk', 'No Data'])
plt.tight_layout()
plt.show()
