import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QProcess
from mainwindow_ui import Ui_MainWindow  # Generated from your .ui file

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Set up the UI from the converted code

        # Initialize QProcess variables
        self.processFRZI = None
        self.processOsm = None
        self.processInterpolation = None

        # Connect actions to respective methods
        try:
            self.actionFRZI.triggered.connect(self.run_friz)
            self.actionFRZ_IA.triggered.connect(self.run_osm)
            self.actionInterpolation.triggered.connect(self.run_interpolation)
            self.actionOpen.triggered.connect(self.run_tifdis)
            self.actionClipping_Raster.triggered.connect(self.run_clipping)
            self.actionSlope.triggered.connect(self.run_slope)
        except AttributeError:
            print("One or more actions not found in the UI!")
    def run_slope(self):
        """Run the external Slope.py script using QProcess."""
        self.processSlope = self.run_script("C:/Users/Admin/Documents/GitHub/Flood/GUI/Slope.py")        
    def run_clipping(self):
        """Run the external Clipping.py script using QProcess."""
        self.processClipping = self.run_script("C:/Users/Admin/Documents/GitHub/Flood/GUI/Clipping.py")
    def run_tifdis(self):
        """Run the external Tifdis.py script using QProcess."""
        self.processTifdis = self.run_script("C:/Users/Admin/Documents/GitHub/Flood/GUI/RasterDisplay.py")

    def run_friz(self):
        """Run the external FRIZ.py script using QProcess."""
        self.processFRZI = self.run_script("C:/Users/Admin/Documents/GitHub/Flood/GUI/FRIZ.py")

    def run_osm(self):
        """Run the external Osm.py script using QProcess."""
        self.processOsm = self.run_script("C:/Users/Admin/Documents/GitHub/Flood/GUI/Osm.py")

    def run_interpolation(self):
        """Run the external Interpolation.py script using QProcess."""
        self.processInterpolation = self.run_script("C:/Users/Admin/Documents/GitHub/Flood/GUI/Interpolation.py")

    def run_script(self, script_path):
        """Helper function to run an external script with QProcess."""
        process = QProcess(self)
        process.readyReadStandardOutput.connect(
            lambda: print(process.readAllStandardOutput().data().decode())
        )
        process.readyReadStandardError.connect(
            lambda: print(process.readAllStandardError().data().decode())
        )
        process.start(sys.executable, [script_path])
        return process

    def closeEvent(self, event):
        """Ensure all external processes are terminated before closing."""
        for process in [self.processFRZI, self.processOsm, self.processInterpolation]:
            if process is not None and process.state() != QProcess.NotRunning:
                process.kill()
                process.waitForFinished(1000)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load QSS stylesheet
    try:
        with open("C:/Users/Admin/Documents/GitHub/Flood/GUI/style.qss", "r") as f:
            qss = f.read()
            app.setStyleSheet(qss)
    except FileNotFoundError:
        print("Warning: style.qss not found. Skipping stylesheet.")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
