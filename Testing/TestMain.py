import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QBrush, QColor
from PyQt6.QtCore import Qt, QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:/Users/Admin/Documents/GitHub/Flood/Testing/ImageView.ui", self)

        # Set up QGraphicsScene
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.scene.setBackgroundBrush(QBrush(QColor(220, 220, 220)))  # Light gray background

        # Connect menu action to trigger raster loading
        self.actionShow.triggered.connect(self.load_raster)

        # QProcess for running GDAL externally
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_process_output)
        self.process.readyReadStandardError.connect(self.on_process_error)

    def load_raster(self):
        """Runs the external GDAL script using QProcess."""
        self.process.start("python", ["C:/Users/Admin/Documents/GitHub/Flood/Testing/load_raster.py"])

    def on_process_output(self):
        """Handles the output from the QProcess (expected: image path)."""
        output = self.process.readAllStandardOutput().data().decode().strip()
        if output:
            print(f"Raster processed: {output}")
            self.display_image(output)

    def on_process_error(self):
        """Handles errors from the QProcess."""
        error = self.process.readAllStandardError().data().decode().strip()
        if error:
            print(f"Error: {error}")

    def display_image(self, image_path):
        """Displays the processed image in QGraphicsView."""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Failed to load processed image")
            return

        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        print("Image displayed successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
