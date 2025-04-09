import sys
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import gaussian_filter

# Check for required arguments: we need 15 in total.
if len(sys.argv) < 20:
    print("Usage: python slopeelerainprox.py <dem_file_path> <rainfall_file_path> <proximity_file_path> "
          "<elevation_weight> <slope_weight> <proximity_weight> <rainfall_weight> "
          "<middle_lower_elev> <middle_upper_elev> <middle_lower_slope> <middle_upper_slope> <middle_lower_rain> <middle_upper_rain>  <middle_lower_prox> <middle_upper_prox>"
          "<High> <Medium> <Low>"
          "<save_file>")
    sys.exit(1)

# File paths
dem_file_path = sys.argv[1]
interpolated_rainfall_file = sys.argv[2]
proximity_file_path = sys.argv[3]

# Weights for combining risks (must sum to 1)
elevation_weight = float(sys.argv[4])
slope_weight     = float(sys.argv[5])
proximity_weight = float(sys.argv[6])
rainfall_weight  = float(sys.argv[7])

# Threshold ranges provided by the user:
elevation_low  = float(sys.argv[8])
elevation_high = float(sys.argv[9])
slope_low      = float(sys.argv[10])
slope_high     = float(sys.argv[11])
rainfall_low   = float(sys.argv[12])
rainfall_high  = float(sys.argv[13])
proximity_low  = float(sys.argv[14])
proximity_high = float(sys.argv[15])

#Colors for the risk levels
high_risk = sys.argv[16]
medium_risk = sys.argv[17]
low_risk = sys.argv[18]

# Save file path
save_file = sys.argv[19]

# ----- DEM & Slope Calculation -----
with rasterio.open(dem_file_path) as dem:
    dem_data = dem.read(1).astype(float)  # convert to float for NaN handling

# Create a mask for negative values in the DEM
negative_mask = dem_data < 0
dem_data[negative_mask] = np.nan

# Apply Gaussian filter for smoothing (optional)
smoothed_data = gaussian_filter(dem_data, sigma=1)

# Calculate the slope (in degrees)
x_gradient, y_gradient = np.gradient(smoothed_data)
slope = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2)) * (180 / np.pi)
slope[negative_mask] = np.nan

# Slope Classification using user-provided thresholds
def classify_slope(slope_data, low, high):
    slope_risk = np.zeros_like(slope_data, dtype=int)
    slope_risk[slope_data < low] = 3        # High flood risk (flat areas)
    slope_risk[(slope_data >= low) & (slope_data <= high)] = 2  # Moderate flood risk
    slope_risk[slope_data > high] = 1        # Low flood risk (steep areas)
    slope_risk[np.isnan(slope_data)] = 4     # No Data
    return slope_risk

slope_risk_map = classify_slope(slope, slope_low, slope_high)

# ----- Rainfall Risk Calculation -----
with rasterio.open(interpolated_rainfall_file) as src:
    rainfall_data = src.read(1).astype(float)  # Ensure float type
    transform = src.transform

rainfall_data[rainfall_data < 0] = 0

def classify_rainfall(rainfall_data, low, high):
    flood_risk_map = np.zeros_like(rainfall_data, dtype=np.uint8)
    flood_risk_map[rainfall_data >= high] = 3   # High risk
    flood_risk_map[(rainfall_data >= low) & (rainfall_data < high)] = 2   # Medium risk
    flood_risk_map[rainfall_data < low] = 1       # Low risk
    flood_risk_map[np.isnan(rainfall_data)] = 4   # No Data
    return flood_risk_map

flood_risk_map = classify_rainfall(rainfall_data, rainfall_low, rainfall_high)

# ----- Elevation Risk Calculation -----
def classify_elevation(elevation_data, low, high):
    elevation_risk = np.zeros_like(elevation_data, dtype=int)
    elevation_risk[(elevation_data < low) & (elevation_data >=0)] = 3  # High risk (low elevation)
    elevation_risk[(elevation_data >= low) & (elevation_data < high)] = 2  # Moderate risk
    elevation_risk[elevation_data >= high] = 1                           # Low risk (high elevation)
    elevation_risk[np.isnan(elevation_data)] = 4                         # No Data
    return elevation_risk

elevation_risk_map = classify_elevation(smoothed_data, elevation_low, elevation_high)

# ----- Proximity Risk Calculation -----
with rasterio.open(proximity_file_path) as src:
    proximity_data = src.read(1).astype(float)

# Normalize proximity data if needed (must be between 0 and 1)
if np.nanmax(proximity_data) > 1 or np.nanmin(proximity_data) < 0:
    print("Proximity data is not scaled between 0 and 1. Normalizing...")
    proximity_data = (proximity_data - np.nanmin(proximity_data)) / (np.nanmax(proximity_data) - np.nanmin(proximity_data))

if np.nanmax(proximity_data) == np.nanmin(proximity_data):
    proximity_data[:] = np.nan  # assign a default value

def classify_proximity(proximity_data, low, high):
    proximity_risk_map = np.zeros_like(proximity_data, dtype=int)
    proximity_risk_map[proximity_data < low] = 3   # High risk: close to water bodies
    proximity_risk_map[(proximity_data >= low) & (proximity_data < high)] = 2  # Moderate risk
    proximity_risk_map[proximity_data >= high] = 1   # Low risk: far from water bodies
    proximity_risk_map[np.isnan(proximity_data)] = 4 # No Data
    return proximity_risk_map

proximity_risk_map = classify_proximity(proximity_data, proximity_low, proximity_high)

# ----- Combine Risks Using Weights -----
def combine_risks_weighted(slope_risk, rainfall_risk, elevation_risk, proximity_risk,
                           weight_slope=0.2, weight_rainfall=0.35, weight_elevation=0.2, weight_proximity=0.25):
    total_weight = weight_slope + weight_rainfall + weight_elevation + weight_proximity
    assert np.isclose(total_weight, 1), "Weights must sum up to 1."
    combined_risk = np.full_like(slope_risk, np.nan, dtype=float)
    valid_mask = ((~np.isnan(slope_risk)) & (~np.isnan(rainfall_risk)) &
                  (~np.isnan(elevation_risk)) & (~np.isnan(proximity_risk)))
    combined_risk[valid_mask] = (weight_slope * slope_risk[valid_mask] +
                                 weight_rainfall * rainfall_risk[valid_mask] +
                                 weight_elevation * elevation_risk[valid_mask] +
                                 weight_proximity * proximity_risk[valid_mask])
    combined_risk = np.round(combined_risk).astype(float)
    combined_risk[~valid_mask] = np.nan
    return combined_risk

combined_risk_map = combine_risks_weighted(
    slope_risk_map,
    flood_risk_map,
    elevation_risk_map,
    proximity_risk_map,
    weight_slope=slope_weight,
    weight_rainfall=rainfall_weight,
    weight_elevation=elevation_weight,
    weight_proximity=proximity_weight
)

# ----- Visualization -----
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Slope Map Visualization
slope_cmap = plt.get_cmap('terrain').copy()
slope_cmap.set_bad(color='gray')
img1 = axes[0].imshow(slope, cmap=slope_cmap, interpolation='bilinear', origin='upper')
axes[0].set_title('Slope Map (NaN Values in Gray)')
axes[0].axis('off')
plt.colorbar(img1, ax=axes[0], label='Slope (degrees)')

# Combined Risk Map Visualization
combined_cmap = ListedColormap([low_risk, medium_risk, high_risk, 'gray'])
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


# ----- Save Output as TIFF (using rasterio for saving) -----
# Here, instead of using GDAL, we use rasterio's writing functionality.
import rasterio
from rasterio.transform import from_origin

# Use the transform from the rainfall file (assumed to match the DEM extent)
# output_file = "combined_risk_output.tif"

# Determine dimensions from the combined risk map
height, width = combined_risk_map.shape

# Create a new raster using rasterio
new_meta = {
    'driver': 'GTiff',
    'height': height,
    'width': width,
    'count': 1,
    'dtype': 'float32',
    'crs': None,  # If you want to add a CRS, you can extract it from the DEM
    'transform': transform
}

with rasterio.open(save_file, 'w', **new_meta) as dst:
    dst.write(combined_risk_map.astype('float32'), 1)

print(f"Output saved as {save_file}")
