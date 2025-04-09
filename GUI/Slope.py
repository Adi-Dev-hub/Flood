import sys
import subprocess
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from slope_ui import Ui_Dialog  # Your generated class


class SlopeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect buttons to their respective methods
        self.ui.toolButton.clicked.connect(self.select_input)
        self.ui.toolButton_2.clicked.connect(self.select_output)
        self.ui.pushButton.clicked.connect(self.run_slope_script)

    def select_input(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select DEM Input Raster", "", "TIFF files (*.tif *.tiff)")
        if file_path:
            self.ui.lineEdit.setText(file_path)

    def select_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Slope Output", "", "TIFF files (*.tif *.tiff)")
        if file_path:
            self.ui.lineEdit_2.setText(file_path)

    def run_slope_script(self):
        input_path = self.ui.lineEdit.text().strip()
        output_path = self.ui.lineEdit_2.text().strip()
        nodata_value = self.ui.lineEdit_3.text().strip()

        if not input_path or not output_path:
            QMessageBox.warning(self, "Missing Input", "Please provide both input and output raster paths.")
            return

        # If nodata_value is empty, pass a default like "None"
        nodata_value = nodata_value if nodata_value else "-1"

        cmd = ["python", "C:/Users/Admin/Documents/GitHub/Flood/Features/slope.py", input_path, output_path, nodata_value]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                self.ui.textBrowser.append("✅ Script ran successfully!\n")
                self.ui.textBrowser.append(result.stdout)
            else:
                self.ui.textBrowser.append("❌ Script failed!\n")
                self.ui.textBrowser.append(result.stderr)
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", f"An error occurred while running the script:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SlopeDialog()
    window.setWindowTitle("Slope Calculation")
    window.show()
    sys.exit(app.exec())
