#interpolation predition
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def predict_flood_risk_with_nan(interpolated_rainfall_file, low_risk_threshold, medium_risk_threshold, high_risk_threshold):
    # Open the interpolated rainfall file (GeoTIFF)
    with rasterio.open(interpolated_rainfall_file) as src:
        rainfall_data = src.read(1).astype(float)  # Ensure float type for NaN handling
        transform = src.transform

    # Debugging step: transform negative rainfall values to zero
    rainfall_data[rainfall_data < 0] = 0

    # # Identify and set NaN values
    # rainfall_data[rainfall_data == 0] = np.nan  # Assuming 0 is considered invalid/NaN

    # Define flood risk levels based on thresholds
    flood_risk = np.zeros(rainfall_data.shape, dtype=np.uint8)
    flood_risk[rainfall_data >= high_risk_threshold] = 3  # High risk
    flood_risk[(rainfall_data >= medium_risk_threshold) & (rainfall_data < high_risk_threshold)] = 2  # Medium risk
    flood_risk[(rainfall_data >= low_risk_threshold) & (rainfall_data < medium_risk_threshold)] = 1  # Low risk
    flood_risk[np.isnan(rainfall_data)] = 4  # Set NaN values as 4 for custom coloring

    # Define colors with NaN (category 4) as gray
    cmap = ListedColormap(['lightblue', 'yellow', 'orange', 'red', 'gray'])
    risk_labels = ['No Risk', 'Low Risk', 'Medium Risk', 'High Risk', 'No Data']

    # Plot flood risk with NaNs in gray
    plt.figure(figsize=(10, 10))
    plt.imshow(flood_risk, cmap=cmap, origin='upper', extent=(src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top))
    cbar = plt.colorbar(ticks=[0, 1, 2, 3, 4], label="Flood Risk Level")
    cbar.ax.set_yticklabels(risk_labels)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Flood Risk Prediction with NaN in Gray")
    plt.show()

# Usage example
interpolated_rainfall_file = 'interpolated_rainfall_resized.tif'
predict_flood_risk_with_nan(interpolated_rainfall_file, low_risk_threshold=10, medium_risk_threshold=20, high_risk_threshold=24)
