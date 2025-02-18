import sys
from osgeo import gdal
from PyQt6.QtGui import QImage
import numpy as np

def load_raster(raster_path):
    print("Loading raster:", raster_path)
    dataset = gdal.Open(raster_path)
    if dataset is None:
        print("ERROR: Failed to load raster", file=sys.stderr)
        return None
    
    # Read first band
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()

    # Normalize data to 0-255 range (for visualization)
    array = (array - np.min(array)) / (np.max(array) - np.min(array)) * 255
    array = array.astype(np.uint8)

    # Convert to QImage (grayscale format)
    height, width = array.shape
    q_image = QImage(array.data, width, height, width, QImage.Format.Format_Grayscale8)

    return q_image

if __name__ == "__main__":
    raster_path = "C:/Users/Admin/Documents/GitHub/Flood/Testing/puneDem.tif"
    qimage = load_raster(raster_path)
    
    if qimage is not None:
        print("RASTER_LOADED")  # Signal to the main app that loading was successful
    else:
        print("ERROR_LOADING_RASTER", file=sys.stderr)
