import rasterio
import numpy as np

# Load the raster file
raster_path = 'data/data.0.tif'

with rasterio.open(raster_path) as src:
    # Read the raster data
    raster_data = src.read(1)
    # Get metadata
    meta = src.meta
    width, height = meta['width'], meta['height']
    transform = src.transform

# Analyze the raster
def check_raster_anomalies(data, width, height):
    anomalies = []
    # Check for extra lines or columns
    if data.shape != (height, width):
        anomalies.append(f"Unexpected shape: Found {data.shape}, expected {(height, width)}.")
    
    # Check for non-standard values (e.g., NaN, negative, or extreme values)
    if np.isnan(data).any():
        anomalies.append("Contains NaN values.")
    if (data < 0).any():
        anomalies.append("Contains negative values.")
    if (data > 1e6).any():  # Example threshold, adjust based on your data
        anomalies.append("Contains abnormally large values.")
    
    # Check for uniformity at the edges
    left_edge = data[:, 0]
    right_edge = data[:, -1]
    if not np.all(left_edge == right_edge):  # Adjust logic if needed
        anomalies.append("Potential issues at the right edge.")

    return anomalies

# Run anomaly check
anomalies = check_raster_anomalies(raster_data, width, height)

# Display results
if anomalies:
    print("Anomalies found:")
    for anomaly in anomalies:
        print(f"- {anomaly}")
else:
    print("No anomalies found. The raster appears normal.")
