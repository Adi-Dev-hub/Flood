import sys
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal


def clip_rainfall_to_dem(dem_path, rainfall_path):
    print(f"Opening DEM file: {dem_path}")
    dem_ds = gdal.Open(dem_path)
    if dem_ds is None:
        raise FileNotFoundError(f"DEM file not found: {dem_path}")

    dem_raster_data = dem_ds.ReadAsArray().astype(float)
    dem_nodata = dem_ds.GetRasterBand(1).GetNoDataValue()
    print(f"DEM NoData value: {dem_nodata}")
    if dem_nodata is not None:
        dem_raster_data[dem_raster_data == dem_nodata] = np.nan

    print(f"Opening Rainfall file: {rainfall_path}")
    rainfall_ds = gdal.Open(rainfall_path)
    if rainfall_ds is None:
        raise FileNotFoundError(f"Rainfall file not found: {rainfall_path}")

    rainfall_raster_data = rainfall_ds.ReadAsArray().astype(float)
    if dem_raster_data.shape != rainfall_raster_data.shape:
        raise ValueError("DEM and Rainfall rasters must have the same dimensions.")

    print("Clipping rainfall data using DEM's valid region...")
    rainfall_clipped = np.where(np.isnan(dem_raster_data), np.nan, rainfall_raster_data)

    geotransform = dem_ds.GetGeoTransform()
    projection = dem_ds.GetProjection()

    dem_ds = None
    rainfall_ds = None

    print("Clipping complete.")
    return rainfall_clipped, geotransform, projection


def save_raster(output_path, array, geotransform, projection, nodata_val=-1):
    print(f"Saving raster to: {output_path}")
    driver = gdal.GetDriverByName("GTiff")
    rows, cols = array.shape
    out_ds = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
    if out_ds is None:
        raise RuntimeError(f"Failed to create output raster: {output_path}")

    out_ds.SetGeoTransform(geotransform)
    out_ds.SetProjection(projection)

    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(array)
    out_band.SetNoDataValue(nodata_val)
    out_band.FlushCache()
    out_ds = None

    print("Raster saved successfully.")
    return output_path


def display_raster(array, title="Raster Data"):
    plt.figure(figsize=(10, 8))
    plt.imshow(array, cmap="viridis", interpolation="nearest")
    plt.colorbar(label="Intensity")
    plt.title(title)
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python clipping.py <input_raster> <extent_raster> <nodata_value> <output_raster>")
        sys.exit(1)

    input_raster_path = sys.argv[1]
    extent_raster_path = sys.argv[2]
    nodata_value = float(sys.argv[3])
    output_raster_path = sys.argv[4]

    try:
        print("Starting clipping process...")
        clipped_array, geo, proj = clip_rainfall_to_dem(extent_raster_path, input_raster_path)

        # Replace NaNs with the user-defined NoData value
        clipped_array_filled = np.where(np.isnan(clipped_array), nodata_value, clipped_array)

        save_raster(output_raster_path, clipped_array_filled, geo, proj, nodata_val=nodata_value)

        print("Displaying clipped raster...")
        display_raster(clipped_array, title="Clipped Raster Data")

        print("Process completed successfully.")
    except Exception as e:
        print(f"Error encountered: {e}")
        sys.exit(1)
