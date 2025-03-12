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
        dem_raster_data[dem_raster_data == dem_nodata] = np.nan  # Convert NoData values to NaN
    
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

def save_raster(output_path, array, reference_ds, save_raster=True, format="GTiff"):
    if not save_raster:
        print("Saving skipped as save_raster is False.")
        return None
    
    print(f"Saving raster to: {output_path}")
    driver = gdal.GetDriverByName(format)
    cols, rows = array.shape[1], array.shape[0]
    out_ds = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
    if out_ds is None:
        raise RuntimeError(f"Failed to create output raster: {output_path}")
    
    out_ds.SetGeoTransform(reference_ds.GetGeoTransform())
    out_ds.SetProjection(reference_ds.GetProjection())
    
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(array)
    out_band.SetNoDataValue(-1)  # Assign NoData value explicitly for missing data
    out_band.FlushCache()
    out_ds = None
    
    print("Raster saved successfully.")
    return output_path

if __name__ == "__main__":
    dem_file_path = "data/puneDem.tif"
    rainfall_file_path = "data/Cproximity.tif"
    output_path = "data/clipped_proximity.tif"
    
    try:
        print("Starting clipping process...")
        clipped_rainfall, geotransform, projection = clip_rainfall_to_dem(dem_file_path, rainfall_file_path)
        print("Saving clipped raster...")
        save_raster(output_path, clipped_rainfall, gdal.Open(dem_file_path))
        print("Process completed successfully.")
    except Exception as e:
        print(f"Error encountered: {e}")
