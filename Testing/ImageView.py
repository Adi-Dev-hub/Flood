import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QWheelEvent, QBrush, QColor
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:/Users/Admin/Documents/GitHub/Flood/Testing/ImageView.ui", self)
        
        # Set up the QGraphicsScene
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.scene.setBackgroundBrush(QBrush(QColor(220, 220, 220)))  # Light gray background
        
        # Enable panning by setting the drag mode to ScrollHandDrag
        self.graphicsView.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
        # Connect a menu action to display the image
        self.actionShow.triggered.connect(self.display_image)
        
        # Set a static image path for testing
        self.image_path = "C:/Users/Admin/Documents/GitHub/Flood/Testing/myself.jpg"

    def display_image(self):
        """Load and display the image when the 'Show' action is triggered."""
        pixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            print("Failed to load image from:", self.image_path)
            return
        
        self.scene.clear()  # Clear any existing items
        self.scene.addPixmap(pixmap)
        
        # Initially fit the image within the view, keeping aspect ratio.
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        print("Image displayed successfully!")

    def wheelEvent(self, event: QWheelEvent):
        """Override the wheel event to implement zooming."""
        zoom_in_factor = 1.2
        zoom_out_factor = 1 / zoom_in_factor
        
        factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
        self.graphicsView.scale(factor, factor)
        event.accept()
        print("Wheel event: zoom factor applied:", factor)

    def resizeEvent(self, event):
        """Ensure the GraphicsView resizes with the window and print its new size."""
        super().resizeEvent(event)
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        
        # Debug message to show the GraphicsView size on resizing
        size = self.graphicsView.size()
        print(f"GraphicsView resized: Width={size.width()}, Height={size.height()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
