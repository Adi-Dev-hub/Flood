import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog,QColorDialog
from PySide6.QtCore import Qt, QProcess
from FRIZ_ui import Ui_Dialog  # Your converted UI file
from PySide6.QtGui import QColor

class FileInputDialog(QDialog, Ui_Dialog):
    def select_color_and_update_line_edit(self, line_edit):
    # Open a color dialog and get the selected color
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()  # This returns the hex string (e.g., "#FF0000")
            line_edit.setText(hex_color)
            return hex_color
        return None
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Initialize UI

        # Connect file browse buttons to file selection functions
        self.toolButton.clicked.connect(lambda: self.select_file(self.lineEdit))
        self.toolButton_2.clicked.connect(lambda: self.select_file(self.lineEdit_2))
        self.toolButton_3.clicked.connect(lambda: self.select_file(self.lineEdit_3))

        # Assume you want these default hex values: 
        self.lineEdit_4.setText("#FF0000")
        self.lineEdit_5.setText("#FFA500")
        self.lineEdit_6.setText("#FFFF00" )

        # Connect color selection buttons to color selection functions
        self.toolButton_4.clicked.connect(lambda: self.select_color_and_update_line_edit(self.lineEdit_4))
        self.toolButton_5.clicked.connect(lambda: self.select_color_and_update_line_edit(self.lineEdit_5))
        self.toolButton_6.clicked.connect(lambda: self.select_color_and_update_line_edit(self.lineEdit_6))

        # Connect the AHP calculation button to update the weight boxes
        self.pushButton_2.clicked.connect(self.calculate_ahp)
        
        # Connect the Run button to execute the external script
        self.pushButton.clicked.connect(self.run_script)
        
        self.process = None

    def select_file(self, line_edit):
        """Opens a file dialog and sets the selected file path into the given QLineEdit."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        if file_path:
            line_edit.setText(file_path)

    def collect_ahp_values(self):
        """
        Collects pairwise comparison values from the tableWidget and computes the AHP weights.
        Assumes the criteria order is: Elevation, Slope, Proximity, Rainfall.
        Returns a tuple (ahp_weights, CR) where ahp_weights is a numpy array and CR is the consistency ratio.
        """
        n = self.tableWidget.rowCount()
        A = np.zeros((n, n), dtype=float)
        for i in range(n):
            for j in range(n):
                item = self.tableWidget.item(i, j)
                if item is not None and item.text():
                    try:
                        A[i, j] = float(item.text())
                    except ValueError:
                        A[i, j] = 1.0
                else:
                    A[i, j] = 1.0

        eigenvalues, eigenvectors = np.linalg.eig(A)
        max_index = np.argmax(eigenvalues.real)
        principal_eigenvector = eigenvectors[:, max_index].real
        ahp_weights = principal_eigenvector / np.sum(principal_eigenvector)

        # Calculate consistency ratio (CR)
        lambda_max = eigenvalues[max_index].real
        CI = (lambda_max - n) / (n - 1) if n > 1 else 0.0
        RI_dict = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12,
                   6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_dict.get(n, 1.49)
        CR = CI / RI if RI != 0 else 0.0

        return ahp_weights, CR

    def calculate_ahp(self):
        """Calculates AHP weights from the tableWidget and updates the double spin boxes."""
        ahp_weights, CR = self.collect_ahp_values()
        self.doubleSpinBox_weigh_1.setValue(ahp_weights[0])
        self.doubleSpinBox_weigh_2.setValue(ahp_weights[1])
        self.doubleSpinBox_weigh_3.setValue(ahp_weights[2])
        self.doubleSpinBox_weigh_4.setValue(ahp_weights[3])
        print("AHP weights updated:")
        print("Elevation =", round(ahp_weights[0], 3),
              "Slope =", round(ahp_weights[1], 3),
              "Proximity =", round(ahp_weights[2], 3),
              "Rainfall =", round(ahp_weights[3], 3))
        print("Consistency Ratio (CR):", round(CR, 3))

    def run_script(self):
        """
        Gathers all the necessary values from the UI:
          - File paths from QLineEdits (DEM, Rainfall, Proximity)
          - AHP weights from the corresponding double spin boxes
          - Middle range values from the lower/upper limit spin boxes in groupBox_4
        Then starts the external script (slopeelerainprox.py) via QProcess,
        passing all these values as command-line arguments.
        """
        # File paths
        Dem = self.lineEdit.text()
        Rainfall = self.lineEdit_2.text()
        Proximity = self.lineEdit_3.text()
        # AHP weight values
        elevation_weight = str(self.doubleSpinBox_weigh_1.value())
        slope_weight = str(self.doubleSpinBox_weigh_2.value())
        proximity_weight = str(self.doubleSpinBox_weigh_3.value())
        rainfall_weight = str(self.doubleSpinBox_weigh_4.value())
        # Middle range values (from groupBox_4)
        middle_lower_elev = str(self.doubleSpinBox_low_1.value())
        middle_upper_elev = str(self.doubleSpinBox_upp_1.value())
        middle_lower_slope = str(self.doubleSpinBox_low_2.value())
        middle_upper_slope = str(self.doubleSpinBox_upp_2.value())
        middle_lower_rain = str(self.doubleSpinBox_low_3.value())
        middle_upper_rain = str(self.doubleSpinBox_upp_3.value())
        middle_lower_prox = str(self.doubleSpinBox_low_4.value())
        middle_upper_prox = str(self.doubleSpinBox_upp_4.value())

        # Color of classes
        High = self.lineEdit_4.text()
        Medium = self.lineEdit_5.text()
        Low = self.lineEdit_6.text()
        # Create and configure QProcess
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(
            lambda: print(self.process.readAllStandardOutput().data().decode())
        )
        self.process.readyReadStandardError.connect(
            lambda: print(self.process.readAllStandardError().data().decode())
        )
        script_path = r"C:/Users/Admin/Documents/GitHub/Flood/Features/slopeelerainprox.py"
        # Build the argument list. Adjust the order as required by your external script.
        args = [
            script_path,
            Dem, Rainfall, Proximity,
            elevation_weight, slope_weight, proximity_weight, rainfall_weight,
            middle_lower_elev, middle_upper_elev,
            middle_lower_slope, middle_upper_slope,
            middle_lower_rain, middle_upper_rain,
            middle_lower_prox, middle_upper_prox,
            High, Medium, Low
        ]
        self.process.start(sys.executable, args)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Try to load the style.qss file
    try:
        with open("C:/Users/Admin/Documents/GitHub/Flood/GUI/style.qss", "r") as f:
            qss = f.read()
            app.setStyleSheet(qss)
    except Exception as e:
        print("Warning: style.qss not found or could not be loaded.", e)
        
    window = FileInputDialog()
    window.show()
    sys.exit(app.exec())
