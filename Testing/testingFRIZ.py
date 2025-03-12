import sys
import numpy as np
from osgeo import gdal
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from PySide6.QtGui import QImage, QPixmap,QPainter,QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile,Qt

def loadUi(ui_file, baseinstance=None):
    """Custom loadUi function for PySide6, similar to uic.loadUi in PyQt6."""
    loader = QUiLoader()
    ui = loader.load(QFile(ui_file))
    
    if baseinstance:
        for attr_name in dir(ui):
            if not attr_name.startswith("__"):
                setattr(baseinstance, attr_name, getattr(ui, attr_name))
        baseinstance.setLayout(ui.layout())

    return ui

class RasterViewer(QMainWindow):
    def __init__(self, raster_path):
        super().__init__()

        # Load UI
        loadUi("C:/Users/Admin/Documents/GitHub/Flood/Testing/raster.ui", self)

        # Enable anti-aliasing (makes it smoother)
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.graphicsView.setBackgroundBrush(QColor(200, 200, 200))  # Light gray background

        # Load and display raster
        self.load_raster(raster_path)

    def load_raster(self, raster_path):
        dataset = gdal.Open(raster_path)
        if not dataset:
            print("Failed to open raster file!")
            return

        band = dataset.GetRasterBand(1)
        raster_data = band.ReadAsArray().astype(np.float32)

        nodata_value = band.GetNoDataValue()
        if nodata_value is not None:
            raster_data[raster_data == nodata_value] = np.nan  

        min_val, max_val = np.nanmin(raster_data), np.nanmax(raster_data)
        if max_val > min_val:
            raster_data = np.clip(((raster_data - min_val) / (max_val - min_val) * 255), 0, 255)
        else:
            raster_data = np.zeros_like(raster_data)

        raster_data = np.nan_to_num(raster_data, nan=0).astype(np.uint8)
        raster_data = np.ascontiguousarray(raster_data)

        height, width = raster_data.shape
        qimage = QImage(raster_data.data, width, height, width, QImage.Format_Grayscale8).copy()

        pixmap = QPixmap.fromImage(qimage)
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)

        self.graphicsView.setScene(scene)
        self.graphicsView.setSceneRect(scene.itemsBoundingRect())  

        # ✅ Make sure `fitInView()` works by forcing an update
        self.graphicsView.fitInView(item, Qt.KeepAspectRatio)
        self.graphicsView.update()  # Refresh view to apply changes

        # ✅ Ensure it resizes dynamically
        self.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        # ✅ Set a background color (optional)
        self.graphicsView.setBackgroundBrush(QColor(200, 200, 200))  # Light gray
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    raster_path = "C:/Users/Admin/Documents/GitHub/Flood/Testing/puneDem.tif"  # Change to your raster file
    viewer = RasterViewer(raster_path)
    viewer.show()

    sys.exit(app.exec())
