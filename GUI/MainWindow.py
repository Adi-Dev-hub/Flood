from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QGraphicsPathItem, QFileDialog
from PyQt6.QtGui import QPixmap, QImage, QPainterPath, QPen
from PyQt6.QtCore import Qt,QThread, pyqtSignal
from osgeo import gdal,ogr
import numpy as np
import sys
from PyQt6 import uic  
# import tifdis as td

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("MainWindow initialized!")  # Debug message
        uic.loadUi("C:/Users/Admin/Documents/GitHub/Flood/GUI/MainWindow.ui", self)  

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        # self.raster_file_path = None  # Store the selected raster file path

        # Connect menu actions
        self.actionOpen_Raster.triggered.connect(self.display_raster)
        self.actionOpen_Shape.triggered.connect(self.load_shapefile)
        
        # Connect show button
        # self.pushButton.clicked.connect(self.display_raster)
    def load_raster(self,file_path):
        print("load_raster() function called! hello")  # Debug message
        """Load a raster file using GDAL."""
        dataset = gdal.Open(file_path)
        if dataset is None:
            raise FileNotFoundError(f"Failed to open raster at path: {file_path}")
        #  Read the DEM raster data as an array
        raster = dataset.ReadAsArray()

        # Convert to float to allow assignment of NaN (as NaN can't be assigned to an integer array)
        raster = raster.astype(float)

        # Set negative values as NoData (NaN)
        raster[raster < 0] = np.nan  # Treat negative values as NoData

        # Close the DEM dataset
        dataset = None

        print("Raster loaded successfully!")  # Debug message
        return raster

    def display_raster(self):
        """Load and display the raster after selecting it."""
        print("display_raster() function called!")  # Debug message
        print("load_raster() function called! hii")  # Debug message
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Raster", "", "Raster Files (*.tif *.tiff *.png *.jpg)")
        
        if not file_path:
            print("No file selected.")  # Debug message
            return
        print(f"Selected file: {file_path}")  # Debug message
        raster_data = self.load_raster(file_path)  # Store file path
      
        # dataset = gdal.Open(self.raster_file_path, gdal.GA_ReadOnly)
        if raster_data is None:
            print("Failed to open raster for display.")
            return

               # raster_data = band.ReadAsArray()
        rows, cols = raster_data.shape

        # Normalize pixel values to 0-255 for display
        raster_data = ((raster_data - raster_data.min()) / (raster_data.max() - raster_data.min()) * 255).astype(np.uint8)

        # Create QImage from raster data
        image = QImage(raster_data.data, cols, rows, cols, QImage.Format_Grayscale8)

        # Convert QImage to QPixmap and display in QGraphicsView
        pixmap = QPixmap.fromImage(image)
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        print("Raster displayed successfully!")

    def load_shapefile(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Shapefile", "", "Shapefiles (*.shp)")
            if not file_path:
                print("No shapefile selected.")
                return

            print(f"Loading shapefile: {file_path}")
            driver = ogr.GetDriverByName("ESRI Shapefile")
            dataset = driver.Open(file_path, 0)
            if dataset is None:
                print("Failed to open shapefile.")
                return

            layer = dataset.GetLayer()
            if layer is None:
                print("Failed to get layer.")
                return

            self.scene.clear()

            for feature in layer:
                geom = feature.GetGeometryRef()
                path = QPainterPath()

                if geom is None:
                    print("Geometry is None, skipping feature.")
                    continue

                if geom.GetGeometryType() in [ogr.wkbLineString, ogr.wkbMultiLineString]:
                    for i in range(geom.GetPointCount()):
                        x, y, _ = geom.GetPoint(i)
                        if i == 0:
                            path.moveTo(x, -y)  
                        else:
                            path.lineTo(x, -y)
                    shape_item = QGraphicsPathItem(path)
                    shape_item.setPen(QPen(Qt.red, 2))
                    self.scene.addItem(shape_item)

                elif geom.GetGeometryType() == ogr.wkbPolygon:
                    for ring in range(geom.GetGeometryCount()):
                        sub_geom = geom.GetGeometryRef(ring)
                        for i in range(sub_geom.GetPointCount()):
                            x, y, _ = sub_geom.GetPoint(i)
                            if i == 0:
                                path.moveTo(x, -y)
                            else:
                                path.lineTo(x, -y)
                    shape_item = QGraphicsPathItem(path)
                    shape_item.setPen(QPen(Qt.blue, 2))
                    self.scene.addItem(shape_item)

            print("Shapefile loaded successfully!")

        except Exception as e:
            print(f"Error in load_shapefile: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        # Load the QSS file
        with open("C:/Users/Admin/Documents/GitHub/Flood/GUI/style.qss", "r") as f:
            qss = f.read()
            app.setStyleSheet(qss)
    except FileNotFoundError:
        print("Warning: GUI/style.qss not found. Skipping stylesheet.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
