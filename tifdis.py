import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import rasterio
from rasterio.transform import from_origin

# Load the DEM image
image_path = 'data/puneDem.tif'
dem_data = tiff.imread(image_path).astype(float)  # Convert to float for NaN handling

# Create a mask for negative values
negative_mask = dem_data < 0

# Replace negative values with NaN
dem_data[negative_mask] = np.nan

# Apply Gaussian filter for smoothing (adjust sigma for more or less smoothing)
smoothed_data = gaussian_filter(dem_data, sigma=1)

# Plot the smoothed elevation data as a heat map (for visualization)
plt.figure(figsize=(10, 8))
plt.gcf().patch.set_facecolor('white')

# Choose a heat map color palette like 'hot', 'coolwarm', or 'inferno'
cmap = plt.get_cmap('inferno_r')
img = plt.imshow(smoothed_data, cmap=cmap, interpolation='bilinear',
                 vmin=np.nanmin(smoothed_data), vmax=np.nanmax(smoothed_data))
cbar = plt.colorbar(img, label='Elevation (m)', shrink=0.8)
plt.title('Smoothed Elevation as Heat Map')
plt.axis('off')
plt.savefig('elevation.png', dpi=300, bbox_inches='tight')  # Save as PNG
plt.show()

# Save the smoothed elevation data as a GeoTIFF
output_path = 'smoothed_elevation.tif'

# Set the transform based on the spatial resolution and top-left corner of the DEM
pixel_size_x, pixel_size_y = 30, 30  # Adjust pixel size to match DEM resolution
west, north = 0, 0  # Update these to match your DEM's georeferencing
transform = from_origin(west, north, pixel_size_x, pixel_size_y)

# Save the data with rasterio
with rasterio.open(
    output_path,
    'w',
    driver='GTiff',
    height=smoothed_data.shape[0],
    width=smoothed_data.shape[1],
    count=1,
    dtype=smoothed_data.dtype,
    crs='EPSG:4326',  # Adjust CRS if needed
    transform=transform,
    nodata=np.nan
) as dst:
    dst.write(smoothed_data, 1)

print(f"GeoTIFF saved at {output_path}")
