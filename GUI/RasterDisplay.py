# main.py
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PySide6.QtGui import QImage, QPixmap, QIcon
from RasterDisplay_ui import Ui_Dialog

class RasterDisplayApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Initialize UI components"""
        self.populate_colormaps()
    
    def connect_signals(self):
        """Connect UI signals to slots"""
        self.ui.toolButton.clicked.connect(self.open_file_dialog)
        self.ui.pushButton.clicked.connect(self.execute_script)
    
    def populate_colormaps(self):
        """Populate combobox with colormaps and color previews"""
        self.ui.comboBox.clear()
        
        # Generate preview icons for all matplotlib colormaps
        width, height = 100, 20  # Preview image dimensions
        
        for cmap_name in sorted(plt.colormaps()):
            try:
                # Create color gradient preview
                cmap = plt.get_cmap(cmap_name)
                gradient = np.linspace(0, 1, width)
                
                # Get RGBA values (shape: [width, 4])
                rgba = cmap(gradient)
                
                # Convert to 8-bit values and create 2D array
                rgba_8bit = (rgba * 255).astype(np.uint8)
                preview_array = np.tile(rgba_8bit, (height, 1, 1))
                
                # Create QImage from numpy array
                image = QImage(
                    preview_array.data,
                    width,
                    height,
                    QImage.Format_RGBA8888
                )
                
                # Create QIcon and add to combobox
                self.ui.comboBox.addItem(QIcon(QPixmap.fromImage(image)), cmap_name)
                
            except Exception as e:
                print(f"Skipping colormap {cmap_name}: {str(e)}")
    
    def open_file_dialog(self):
        """Handle file selection"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Raster File",
            "",
            "GeoTIFF Files (*.tif *.tiff);;All Files (*)"
        )
        if file_path:
            self.ui.lineEdit.setText(file_path)
    
    def execute_script(self):
        """Execute external script with parameters"""
        file_path = self.ui.lineEdit.text()
        colormap = self.ui.comboBox.currentText()
        
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please select a raster file first!")
            return
        
        try:
            script_path = r"C:\Users\Admin\Documents\GitHub\Flood\GUI\tifdis.py"
            subprocess.run([
                sys.executable,
                script_path,
                "--file", file_path,
                "--cmap", colormap
            ], check=True)
            
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Script failed: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RasterDisplayApp()
    window.show()
    sys.exit(app.exec())