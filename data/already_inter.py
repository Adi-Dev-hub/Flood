#interpollate rainfall

import numpy as np
import rasterio
from scipy.ndimage import zoom
import matplotlib.pyplot as plt

# Define the target shape to match
target_shape = (5399, 6623)

# Open the existing interpolated rainfall GeoTIFF file
interpolated_rainfall_file = 'interpolated_rainfall.tif'
with rasterio.open(interpolated_rainfall_file) as src:
    # Read the rainfall data and ensure it's in float format for NaN handling
    rainfall_data = src.read(1).astype(float)

# Calculate the zoom factors based on the target shape
zoom_factors = (target_shape[0] / rainfall_data.shape[0], 
                target_shape[1] / rainfall_data.shape[1])

# Interpolate to match the target shape using linear interpolation
interpolated_rainfall = zoom(rainfall_data, zoom_factors, order=1)  # order=1 for linear interpolation

# Handle NaN values by leaving them as NaN (no need to fill)
# Create a masked array where NaNs are masked
masked_array = np.ma.masked_invalid(interpolated_rainfall)

# Display the interpolated rainfall data with NaNs in gray
plt.figure(figsize=(10, 10))

# Create a colormap and set NaN values to gray
cmap = plt.cm.viridis  # You can choose any colormap you prefer
cmap.set_bad(color='gray')  # Set color for NaN values

# Display the data using imshow
plt.imshow(masked_array, cmap=cmap, origin='upper')
plt.colorbar(label='Interpolated Rainfall')
plt.title('Interpolated Rainfall Data with NaNs in Gray')
plt.xlabel('Column Index')
plt.ylabel('Row Index')
plt.show()

# Save the new interpolated rainfall data to a new GeoTIFF file
output_file = 'interpolated_rainfall_resized.tif'
with rasterio.open(
    output_file,
    'w',
    driver='GTiff',
    height=interpolated_rainfall.shape[0],
    width=interpolated_rainfall.shape[1],
    count=1,
    dtype=interpolated_rainfall.dtype,
    crs=src.crs,
    transform=src.transform
) as dst:
    dst.write(interpolated_rainfall, 1)

print(f"Interpolated rainfall data saved to {output_file}")