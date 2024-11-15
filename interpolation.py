import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def interpolate_rainfall(rainfall_shapefile):
    # Load the rainfall shapefile
    rainfall_gdf = gpd.read_file(rainfall_shapefile)

    # Extract rainfall data and coordinates for interpolation
    coords = np.array([(point.x, point.y) for point in rainfall_gdf.geometry])
    rainfall_values = rainfall_gdf['rainfall'].values

    # Define the bounding box for interpolation
    minx, miny, maxx, maxy = rainfall_gdf.total_bounds
    grid_x, grid_y = np.mgrid[minx:maxx:6623j, miny:maxy:5399j]  # Set to desired shape 5399 x 6623

    # Interpolate rainfall data over the grid
    grid_z = griddata(coords, rainfall_values, (grid_x, grid_y), method='cubic')

    # Plotting the interpolated data
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("Interpolated Rainfall")
    plt.imshow(grid_z, extent=(minx, maxx, miny, maxy), origin='lower', cmap='Blues', alpha=0.6)
    plt.colorbar(label="Rainfall (mm)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

# Usage example
rainfall_shapefile = 'data/DRMS_station.shp'    # Replace with the path to your rainfall shapefile
interpolate_rainfall(rainfall_shapefile)
