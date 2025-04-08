import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QDialog, QFileDialog, QMessageBox
)
from Clipping_ui import Ui_Dialog  # This is your auto-generated UI class


class ClippingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect Run button
        self.ui.pushButton.clicked.connect(self.run_clipping_script)

        # Connect Tool Buttons
        self.ui.toolButton.clicked.connect(self.select_input_raster)
        self.ui.toolButton_2.clicked.connect(self.select_extent_raster)
        self.ui.toolButton_3.clicked.connect(self.select_output_raster)

    def select_input_raster(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input Raster", "", "Raster Files (*.tif *.tiff *.img);;All Files (*)"
        )
        if file_path:
            self.ui.lineEdit.setText(file_path)

    def select_extent_raster(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Extent Raster", "", "Raster Files (*.tif *.tiff *.img);;All Files (*)"
        )
        if file_path:
            self.ui.lineEdit_2.setText(file_path)

    def select_output_raster(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Output Raster Path", "", "TIFF Files (*.tif);;All Files (*)"
        )
        if file_path:
            self.ui.lineEdit_4.setText(file_path)

    def run_clipping_script(self):
        # input_raster = self.ui.lineEdit.text().strip()
        # extent_raster = self.ui.lineEdit_2.text().strip()
        # nodata_value = self.ui.lineEdit_3.text().strip()
        # output_raster = self.ui.lineEdit_4.text().strip()
        input_raster = "data/Cproximity.tif"
        extent_raster = "data/puneDem.tif"
        nodata_value = "-1"
        output_raster = "data/clipped_proximity.tif"

        if not input_raster or not extent_raster or not nodata_value or not output_raster:
            QMessageBox.warning(self, "Missing Input", "Please fill in all fields.")
            return

        script_path = r"C:\Users\Admin\Documents\GitHub\Flood\Features\clipping.py"

        try:
            result = subprocess.run(
                ["python", script_path, input_raster, extent_raster, nodata_value, output_raster],
                capture_output=True,
                text=True,
                check=True
            )
            self.ui.textBrowser.setPlainText(result.stdout)
            QMessageBox.information(self, "Success", "Clipping completed successfully.")
        except subprocess.CalledProcessError as e:
            self.ui.textBrowser.setPlainText(e.stderr)
            QMessageBox.critical(self, "Error", f"Script failed:\n{e.stderr}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Script Not Found", f"Could not find script at:\n{script_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ClippingDialog()
    dialog.setWindowTitle("FRZIT - Clipping Tool")
    dialog.show()
    sys.exit(app.exec())
