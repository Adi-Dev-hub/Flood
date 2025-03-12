import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QProcess
from mainwindow_ui import Ui_MainWindow  # Generated from your .ui file

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Set up the UI from the converted code

        # Initialize QProcess variable
        self.frizProcess = None

        # Connect the FRZI action to run_friz() method.
        # The generated UI code should have created self.actionFRZI.
        try:
            self.actionFRZI.triggered.connect(self.run_friz)
        except AttributeError:
            print("actionFRZI not found in the UI!")

    def run_friz(self):
        """Run the external FRIZ.py script using QProcess."""
        self.frizProcess = QProcess(self)
        self.frizProcess.readyReadStandardOutput.connect(
            lambda: print(self.frizProcess.readAllStandardOutput().data().decode())
        )
        self.frizProcess.readyReadStandardError.connect(
            lambda: print(self.frizProcess.readAllStandardError().data().decode())
        )
        script_path = r"C:/Users/Admin/Documents/GitHub/Flood/GUI/FRIZ.py"
        self.frizProcess.start(sys.executable, [script_path])

    def closeEvent(self, event):
        """Ensure the external process is terminated before closing."""
        if self.frizProcess is not None and self.frizProcess.state() != QProcess.NotRunning:
            self.frizProcess.kill()
            self.frizProcess.waitForFinished(1000)
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
