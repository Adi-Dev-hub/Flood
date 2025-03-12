import sys
import numpy as np
from osgeo import gdal
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QSizePolicy
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QPointF

# Custom QGraphicsView subclass to mimic QGIS behavior.
class MapCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def wheelEvent(self, event):
        zoomFactor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(zoomFactor, zoomFactor)

# Main window that loads and displays raster data.
class MainWindow(QMainWindow):
    def __init__(self, raster_path):
        super().__init__()
        self.setWindowTitle("QGIS-Style Raster Viewer")
        self.canvas = MapCanvas(self)
        self.setCentralWidget(self.canvas)
        self.showMaximized()

        self.load_raster(raster_path)

    def load_raster(self, raster_path):
        dataset = gdal.Open(raster_path)
        if not dataset:
            print("Failed to open raster file!")
            return

        band = dataset.GetRasterBand(1)
        raster_data = band.ReadAsArray().astype(np.float32)

        # Handle NoData values
        nodata_value = band.GetNoDataValue()
        if nodata_value is not None:
            raster_data[raster_data == nodata_value] = np.nan

        # Normalize data for display
        min_val, max_val = np.nanmin(raster_data), np.nanmax(raster_data)
        if max_val > min_val:
            raster_data = np.clip(((raster_data - min_val) / (max_val - min_val) * 255), 0, 255)
        else:
            raster_data = np.zeros_like(raster_data)

        raster_data = np.nan_to_num(raster_data, nan=0).astype(np.uint8)
        raster_data = np.ascontiguousarray(raster_data)

        # Get raster geotransform (for correct positioning)
        geo_transform = dataset.GetGeoTransform()
        top_left_x = geo_transform[0]  # X coordinate of top-left corner
        top_left_y = geo_transform[3]  # Y coordinate of top-left corner
        pixel_width = geo_transform[1]  # Pixel size in X direction
        pixel_height = -geo_transform[5]  # Pixel size in Y direction (negative)

        dataset = None  # Close the dataset

        # Create QImage from the raster data
        height, width = raster_data.shape
        qimage = QImage(raster_data.data, width, height, width, QImage.Format_Grayscale8).copy()
        pixmap = QPixmap.fromImage(qimage)

        # Create scene and add the raster with correct positioning
        scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem(pixmap)
        scene.addItem(self.item)

        # Convert pixel coordinates to real-world coordinates
        self.item.setScale(pixel_width)  # Scale by real-world pixel size
        self.item.setPos(QPointF(top_left_x, top_left_y - (height * pixel_height)))  # Adjust for top-left origin

        self.canvas.setScene(scene)
        self.canvas.setSceneRect(scene.itemsBoundingRect())  # Adjust scene boundaries
        self.canvas.fitInView(self.item, Qt.KeepAspectRatio)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Change this to your raster file path
    raster_path = "C:/Users/Admin/Documents/GitHub/Flood/Testing/puneDem.tif"
    window = MainWindow(raster_path)
    window.show()
    
    sys.exit(app.exec())
