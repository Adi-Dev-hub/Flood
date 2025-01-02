import rasterio
import numpy as np
import matplotlib.pyplot as plt

def display_lulc_info(lulc_path):
    # Open the LULC file
    with rasterio.open(lulc_path) as src:
        print("=== LULC File Metadata ===")
        print(f"Driver: {src.driver}")
        print(f"Width, Height: {src.width} x {src.height}")
        print(f"Number of Bands: {src.count}")
        print(f"Coordinate Reference System (CRS): {src.crs}")
        print(f"Bounds: {src.bounds}")
        
        # Read the first band
        lulc_data = src.read(1)
        transform = src.transform
        
    # Display unique class values
    unique_classes = np.unique(lulc_data)
    print("\nUnique LULC Classes:")
    for value in unique_classes:
        print(f"Class Value: {value}")
    
    # Display a basic visualization
    plt.figure(figsize=(10, 8))
    plt.imshow(lulc_data, cmap='tab20', interpolation='none')
    plt.colorbar(label="LULC Classes")
    plt.title("LULC Map")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.show()

# Path to your LULC file
lulc_file = "path_to_your_lulc_map.tif"

# Call the function
display_lulc_info(lulc_file)
