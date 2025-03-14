from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog)
from PySide6.QtCore import QCoreApplication
import subprocess
from Interpolation_ui import Ui_Dialog  # Assuming your UI file is compiled as Interpolation_ui.py

class InterpolationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect tool buttons to open file dialogs
        self.ui.toolButton.clicked.connect(lambda: self.load_file(self.ui.lineEdit, "Shapefiles (*.shp);;All Files (*)"))
        self.ui.toolButton_2.clicked.connect(lambda: self.load_file(self.ui.lineEdit_2, "Raster Files (*.tif *.tiff);;All Files (*)"))
        
        # Connect run button to execute script
        self.ui.pushButton.clicked.connect(self.run_script)

    def load_file(self, line_edit, file_filter):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_path:
            line_edit.setText(file_path)

    def run_script(self):
        self.ui.lineEdit.setText("data/DRMS_station.shp")
        self.ui.lineEdit_2.setText("data/puneDem.tif")
        self.ui.lineEdit_3.setText("-1")
        rainfall_path = self.ui.lineEdit.text()
        extent_raster_path = self.ui.lineEdit_2.text()
        no_data_value = self.ui.lineEdit_3.text()
        smoothened = self.ui.checkBox.isChecked()
        
        if not rainfall_path or not extent_raster_path:
            print("Please select required files.")
            return

        print(f"Running script with parameters:\n Rainfall: {rainfall_path}\n Extent Raster: {extent_raster_path}\n No Data Value: {no_data_value}\n Smoothened: {smoothened}")
        
        # Execute the interpolation script
        script_path = "C:/Users/Admin/Documents/GitHub/Flood/Features/interpolation.py"
        try:
            subprocess.run(["python", script_path, rainfall_path, extent_raster_path, no_data_value, str(smoothened)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = InterpolationDialog()
    window.show()
    app.exec()
