import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 1. Load the LULC Map
lulc_file_path = 'data/PuneLuLc.tif'
with rasterio.open(lulc_file_path) as lulc_src:
    lulc_data = lulc_src.read(1)  # Read the LULC raster data
    lulc_transform = lulc_src.transform

# 2. Define LULC Risk Categories
# Replace these categories based on your LULC map legend
# {LULC category: flood risk level}
lulc_risk_mapping = {
    1: 1,  # Water Body: Low Risk
    2: 3,  # Urban: High Risk
    3: 2,  # Agriculture: Moderate Risk
    4: 1,  # Forest: Low Risk
    5: 2,  # Barren Land: Moderate Risk
}

# 3. Create Flood Risk Map Based on LULC
lulc_flood_risk = np.zeros_like(lulc_data, dtype=np.uint8)

# Assign flood risk levels to LULC categories
for lulc_category, risk_level in lulc_risk_mapping.items():
    lulc_flood_risk[lulc_data == lulc_category] = risk_level

# Handle No Data values (e.g., -1 or a specific nodata value in your raster)
nodata_value = -1  # Adjust based on your dataset
lulc_flood_risk[lulc_data == nodata_value] = 4  # Assign 'No Data' risk level

# 4. Visualize LULC Flood Risk Map
fig, ax = plt.subplots(figsize=(10, 8))

# Define a colormap for flood risk
lulc_cmap = ListedColormap(['lightblue', 'yellow', 'orange', 'red', 'gray'])
risk_labels = ['Low Risk', 'Moderate Risk', 'High Risk', 'No Data']

# Plot the flood risk map
img = ax.imshow(lulc_flood_risk, cmap=lulc_cmap, origin='upper')
ax.set_title('Flood Risk Based on LULC')
ax.axis('off')

# Add a colorbar
cbar = plt.colorbar(img, ax=ax, ticks=[1, 2, 3, 4], shrink=0.8)
cbar.ax.set_yticklabels(risk_labels)
cbar.set_label('Flood Risk Level')

plt.show()
