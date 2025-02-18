import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Function to create an inundation map
def create_inundation_map(dem_path, output_path, water_level=2.0):
    """
    Create an inundation map from a DEM file.

    Parameters:
    dem_path (str): Path to the DEM file (GeoTIFF format).
    output_path (str): Path to save the output inundation map (GeoTIFF).
    water_level (float): Water level to compare against the DEM (in meters).
    """
    # Open the DEM file
    with rasterio.open(dem_path) as dem:
        dem_data = dem.read(1)  # Read the first band (elevation values)
        profile = dem.profile   # Get the metadata profile

        # Create a binary inundation mask where elevation <= water level
        inundation_mask = (dem_data <= water_level).astype(np.uint8)

        # Update the metadata profile for the output
        profile.update(dtype=rasterio.uint8, count=1)

        # Save the inundation mask as a new GeoTIFF
        with rasterio.open(output_path, 'w', **profile) as output:
            output.write(inundation_mask, 1)

    # Plot the DEM and the inundation mask for visualization
    plt.figure(figsize=(12, 6))
    
    # Plot DEM
    plt.subplot(1, 2, 1)
    plt.title("DEM")
    plt.imshow(dem_data, cmap='terrain', extent=[dem.bounds.left, dem.bounds.right, dem.bounds.bottom, dem.bounds.top])
    plt.colorbar(label="Elevation (m)")
    
    # Plot Inundation Map
    plt.subplot(1, 2, 2)
    plt.title("Inundation Map (Water Level: {}m)".format(water_level))
    plt.imshow(inundation_mask, cmap='Blues', extent=[dem.bounds.left, dem.bounds.right, dem.bounds.bottom, dem.bounds.top])
    plt.colorbar(label="Inundation (1 = Inundated, 0 = Not Inundated)")
    
    plt.tight_layout()
    plt.show()

# Example usage
dem_file = "path/to/your/dem.tif"  # Replace with the path to your DEM file
output_file = "path/to/save/inundation_map.tif"  # Replace with the path to save the output map
create_inundation_map(dem_file, output_file, water_level=2.0)
