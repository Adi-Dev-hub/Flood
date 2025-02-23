import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QProcess

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

class FileInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load UI from FRIZ.ui
        loadUi("C:/Users/Admin/Documents/GitHub/Flood/GUI/FRIZ.ui", self)

        # Connect browse buttons to file selection functions
        self.toolButton.clicked.connect(lambda: self.select_file(self.lineEdit))
        self.toolButton_2.clicked.connect(lambda: self.select_file(self.lineEdit_2))
        self.toolButton_3.clicked.connect(lambda: self.select_file(self.lineEdit_3))

        # Connect the AHP calculation button to update the double spin boxes with computed weights
        self.pushButton_2.clicked.connect(self.calculate_ahp)

        # Connect the run button to execute the external script
        self.pushButton.clicked.connect(self.run_script)

    def select_file(self, line_edit):
        """Opens file dialog and sets the selected file path to QLineEdit."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        if file_path:
            line_edit.setText(file_path)

    def collect_ahp_values(self):
        """
        Collects pairwise comparison values from a QTableWidget named 'tableWidget'
        and computes the AHP weights and consistency ratio.
        Assumes the criteria order is: Elevation, Slope, Proximity, Rainfall.
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

        # Compute eigenvalues and eigenvectors
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
        """Calculates AHP weights from the table, updates the double spin boxes, and prints the consistency ratio."""
        ahp_weights, CR = self.collect_ahp_values()
        # Update double spin boxes with computed AHP weights
        self.doubleSpinBox.setValue(ahp_weights[0])
        self.doubleSpinBox_2.setValue(ahp_weights[1])
        self.doubleSpinBox_3.setValue(ahp_weights[2])
        self.doubleSpinBox_4.setValue(ahp_weights[3])
        print("AHP weights updated:")
        print("Elevation =", round(ahp_weights[0], 3),
              "Slope =", round(ahp_weights[1], 3),
              "Proximity =", round(ahp_weights[2], 3),
              "Rainfall =", round(ahp_weights[3], 3))
        print("Consistency Ratio (CR):", round(CR, 3))

    def run_script(self):
        """Executes an external Python script using QProcess and passes file paths and the final weights."""
        # Gather the current file path values
        Dem = self.lineEdit.text()
        Rainfall = self.lineEdit_2.text()
        Proximity = self.lineEdit_3.text()
        # Read the final weight values from the double spin boxes
        elevation_weight = str(self.doubleSpinBox.value())
        slope_weight     = str(self.doubleSpinBox_2.value())
        proximity_weight = str(self.doubleSpinBox_3.value())
        rainfall_weight  = str(self.doubleSpinBox_4.value())
        # Create a QProcess instance
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(
            lambda: print(self.process.readAllStandardOutput().data().decode())
        )
        self.process.readyReadStandardError.connect(
            lambda: print(self.process.readAllStandardError().data().decode())
        )
        # Path to the external script to run
        script_path = r"C:/Users/Admin/Documents/GitHub/Flood/Features/slopeelerainprox.py"
        # Start the external process using the current Python interpreter and pass the arguments
        self.process.start(sys.executable, [
            script_path, Dem, Rainfall, Proximity,
            elevation_weight, slope_weight, proximity_weight, rainfall_weight
        ])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileInputDialog()
    window.show()
    sys.exit(app.exec())
