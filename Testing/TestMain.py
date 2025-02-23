import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6 import uic
from PyQt6.QtCore import QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:/Users/Admin/Documents/GitHub/Flood/Testing/ImageView.ui", self)

        # Connect menu action to trigger raster loading
        self.actionShow.triggered.connect(self.load_raster)

        # QProcess for running GDAL externally
        self.process = QProcess()
        self.process.readyReadStandardError.connect(self.on_process_error)

    def load_raster(self):
        """Opens a file dialog to select a raster and then executes load_raster.py."""
        raster_path, _ = QFileDialog.getOpenFileName(self, "Select Raster File", "", "Raster Files (*.tif *.tiff)")
        
        # raster_path = "C:/Users/Admin/Documents/GitHub/Flood/Testing/puneDem.tif"  # Example raster file
        
        print(f"Executing load_raster.py with: {raster_path}")
        self.process.start("python", ["C:/Users/Admin/Documents/GitHub/Flood/Testing/load_raster.py", raster_path])

    def on_process_error(self):
        """Handles errors from the QProcess."""
        error = self.process.readAllStandardError().data().decode().strip()
        if error:
            print(f"Error: {error}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
