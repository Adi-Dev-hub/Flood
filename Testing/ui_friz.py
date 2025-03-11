import sys
import numpy as np
from osgeo import gdal
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QSizePolicy
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QTimer, QEvent

def loadUi(ui_file, baseinstance=None):
    """Custom loadUi function for PySide6, similar to uic.loadUi in PyQt6."""
    loader = QUiLoader()
    file = QFile(ui_file)
    file.open(QFile.ReadOnly)
    ui = loader.load(file, baseinstance)
    file.close()
    
    if baseinstance:
        for attr_name in dir(ui):
            if not attr_name.startswith("__"):
                setattr(baseinstance, attr_name, getattr(ui, attr_name))
        baseinstance.setLayout(ui.layout())
    return ui

class RasterViewer(QMainWindow):
    def __init__(self, raster_path):
        super().__init__()

        # Load UI from the raster.ui file
        loadUi("C:/Users/Admin/Documents/GitHub/Flood/Testing/raster.ui", self)

        # Enable smooth rendering and set background
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.graphicsView.setBackgroundBrush(QColor(200, 200, 200))
        self.graphicsView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Install an event filter on the viewport to catch wheel events for zooming
        self.graphicsView.viewport().installEventFilter(self)

        # Load and display the raster
        self.load_raster(raster_path)

        # Use a timer to adjust the view after layout settles
        QTimer.singleShot(0, self.adjustView)

    def load_raster(self, raster_path):
        dataset = gdal.Open(raster_path)
        if not dataset:
            print("Failed to open raster file!")
            return

        # Read the first band as a float32 array
        band = dataset.GetRasterBand(1)
        raster_data = band.ReadAsArray().astype(np.float32)

        # Replace NoData values with NaN, if defined
        nodata_value = band.GetNoDataValue()
        if nodata_value is not None:
            raster_data[raster_data == nodata_value] = np.nan  

        # Normalize data to 0-255 for display
        min_val, max_val = np.nanmin(raster_data), np.nanmax(raster_data)
        if max_val > min_val:
            raster_data = np.clip(((raster_data - min_val) / (max_val - min_val) * 255), 0, 255)
        else:
            raster_data = np.zeros_like(raster_data)

        raster_data = np.nan_to_num(raster_data, nan=0).astype(np.uint8)
        raster_data = np.ascontiguousarray(raster_data)

        self.raster_data = raster_data  # store for later use in plotting

        # Use GetGeoTransform() to retrieve the affine transformation
        self.transform = dataset.GetGeoTransform()
        dataset = None  # Close the dataset

        # Create QImage from the raster data (using copy() to ensure proper memory handling)
        height, width = raster_data.shape
        qimage = QImage(raster_data.data, width, height, width, QImage.Format_Grayscale8).copy()

        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(qimage)

        # Create a QGraphicsScene and add the pixmap item
        self.scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.item)

        # Set the scene in the QGraphicsView
        self.graphicsView.setScene(self.scene)
        # Use the item's bounding rectangle as the scene rect
        self.graphicsView.setSceneRect(self.item.boundingRect())

        # Set the resize anchor so that scaling is based on the mouse position
        self.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        # Set the viewport update mode for smooth rendering
        self.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def adjustView(self):
        # Force the view to fit the raster image while keeping aspect ratio
        if hasattr(self, "item") and self.item is not None:
            self.graphicsView.fitInView(self.item, Qt.KeepAspectRatio)

    def eventFilter(self, obj, event):
        # Catch wheel events on the graphicsView's viewport to implement zooming.
        if obj == self.graphicsView.viewport() and event.type() == QEvent.Wheel:
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor
            if event.angleDelta().y() > 0:
                factor = zoomInFactor
            else:
                factor = zoomOutFactor
            self.graphicsView.scale(factor, factor)
            return True  # event handled
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        # On window resize, adjust the view to fit the raster
        self.adjustView()
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    raster_path = "C:/Users/Admin/Documents/GitHub/Flood/Testing/puneDem.tif"  # Change to your raster file path
    viewer = RasterViewer(raster_path)
    viewer.show()

    sys.exit(app.exec())
