import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load the raster data
with rasterio.open('data/ps2.tif') as src:
    # Read the first band (assuming it contains LULC data)
    band1 = src.read(1)
    
    # Step 2: Extract the color palette (colormap)
    colormap = src.colormap(1)  # Get colormap for the first band

# Create a color map from the colormap dictionary
# This will create a list of colors corresponding to index values
colors = np.zeros((256, 4), dtype=np.float32)  # Assuming up to 256 classes with RGBA
for index, color in colormap.items():
    # Normalize RGB values if they are in range [0, 255]
    if len(color) == 4:  # RGBA
        colors[index] = [c / 255.0 for c in color]  # Normalize to [0, 1]
    else:  # RGB
        colors[index] = [c / 255.0 for c in color] + [1.0]  # Add alpha channel as fully opaque

# Step 3: Display the map using Matplotlib
plt.figure(figsize=(10, 10))
# Use `imshow` without specifying a colormap; it will use indexed colors
plt.imshow(band1, cmap=plt.cm.colors.ListedColormap(colors))
plt.colorbar(ticks=range(len(colormap)), label='LULC Classes')
plt.title('LULC Map')
plt.axis('off')  # Hide axes
plt.show()
