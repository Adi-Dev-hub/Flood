import sys
import numpy as np
import rasterio
import rasterio.features
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# Get DEM and shapefile paths from command-line arguments
dem_file_path = sys.argv[1] if len(sys.argv) > 1 else 'data/puneDem.tif'  # Default to Pune DEM if no input
shp_file_path = sys.argv[2] if len(sys.argv) > 2 else None  # Optional shapefile path

try:
    # 1. Load the DEM
    with rasterio.open(dem_file_path) as dem:
        dem_data = dem.read(1).astype(float)  # Convert to float for NaN handling
        transform = dem.transform
        dem_crs = dem.crs

    # 2. If a shapefile is provided, mask the DEM data using the shapefile
    if shp_file_path:
        # Load the shapefile
        shapefile = gpd.read_file(shp_file_path)
        
        if shapefile.empty:
            raise ValueError("Shapefile contains no geometries!")

        # Reproject the shapefile to match the DEM CRS
        if shapefile.crs.to_epsg() != dem_crs.to_epsg():
            shapefile = shapefile.to_crs(epsg=dem_crs.to_epsg())

        # Create a mask for the shapefile region
        mask = rasterio.features.geometry_mask(
            [geom for geom in shapefile.geometry],
            transform=transform,
            invert=True,
            out_shape=dem_data.shape
        )

        # Apply the mask to the DEM data (set areas outside the shapefile region to NaN)
        dem_data[~mask] = np.nan

    # 3. Mask for negative values in the DEM
    negative_mask = dem_data < 0
    dem_data[negative_mask] = np.nan

    # Optional: Apply Gaussian filter for smoothing
    smoothed_data = gaussian_filter(dem_data, sigma=1)

    # 4. Calculate the Slope
    x_gradient, y_gradient = np.gradient(smoothed_data)
    slope = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2)) * (180 / np.pi)
    slope[negative_mask] = np.nan

    # Define slope risk categories
    def classify_slope(slope_data):
        slope_risk = np.zeros_like(slope_data, dtype=int)
        slope_risk[(slope_data < 30)] = 3  # High flood risk (flat areas)
        slope_risk[(slope_data >= 30) & (slope_data <= 50)] = 2  # Moderate flood risk
        slope_risk[(slope_data > 50)] = 1  # Low flood risk (steep areas)
        slope_risk[np.isnan(slope_data)] = 4  # NaN as No Data
        return slope_risk

    slope_risk_map = classify_slope(slope)

    # 5. Visualize the Slope Map
    fig, ax = plt.subplots(figsize=(10, 6))
    slope_cmap = plt.get_cmap('terrain').copy()
    slope_cmap.set_bad(color='gray')  # Handle NaN areas with gray color
    img = ax.imshow(slope, cmap=slope_cmap, interpolation='bilinear', origin='upper')
    ax.set_title(f"Slope Map ({dem_file_path.split('/')[-1]})")
    ax.axis('off')
    plt.colorbar(img, ax=ax, label='Slope (degrees)')
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error: {e}")
