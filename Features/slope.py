import sys
import numpy as np
from osgeo import gdal
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

def classify_slope(slope_data):
    slope_risk = np.full_like(slope_data, np.nan, dtype=float)
    slope_risk[(~np.isnan(slope_data)) & (slope_data < 30)] = 3  # High flood risk
    slope_risk[(~np.isnan(slope_data)) & (slope_data >= 30) & (slope_data <= 50)] = 2  # Moderate
    slope_risk[(~np.isnan(slope_data)) & (slope_data > 50)] = 1  # Low
    return slope_risk

def save_raster(output_path, array, geo, proj, nodata_val=np.nan):
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = array.shape
    out_raster = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
    out_raster.SetGeoTransform(geo)
    out_raster.SetProjection(proj)
    out_band = out_raster.GetRasterBand(1)
    out_band.WriteArray(array)
    out_band.SetNoDataValue(nodata_val)
    out_raster.FlushCache()

def display_raster(array, title="Raster"):
    plt.imshow(array, cmap='terrain', interpolation='bilinear')
    plt.title(title)
    plt.colorbar(label="Risk Level (1=Low, 2=Moderate, 3=High)")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python slope.py <input_dem>  <output_path> <nodata_value>")
        sys.exit(1)

    dem_path = sys.argv[1]
    output_path = sys.argv[2]
    nodata_value = float(sys.argv[3])

    try:
        print("Loading DEM...")
        dataset = gdal.Open(dem_path)
        if dataset is None:
            raise FileNotFoundError(f"DEM not found: {dem_path}")

        band = dataset.GetRasterBand(1)
        dem = band.ReadAsArray().astype(float)

        # Apply NoData mask
        dem[dem == nodata_value] = np.nan

        print("Applying Gaussian smoothing...")
        smoothed = gaussian_filter(dem, sigma=1)

        print("Calculating slope...")
        x_grad, y_grad = np.gradient(smoothed)
        slope = np.arctan(np.sqrt(x_grad**2 + y_grad**2)) * (180 / np.pi)
        slope[np.isnan(dem)] = np.nan  # re-mask

        print("Classifying slope into risk levels...")
        slope_risk = classify_slope(slope)

        if output_path is  not"temp_slope.tif":
            print("Saving slope risk raster...")
            save_raster(output_path, slope_risk, dataset.GetGeoTransform(), dataset.GetProjection(), nodata_val=nodata_value)

        print("Displaying slope risk map...")
        display_raster(slope_risk, title="Slope Risk Map")

        print("Process completed successfully.")
    except Exception as e:
        print(f"Error encountered: {e}")
        sys.exit(1)
