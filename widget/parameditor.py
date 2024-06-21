import sys

from PySide6.QtGui import QColor, QBrush, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QGraphicsScene, QGraphicsView


class PEScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._view = None

        # set size
        self._width = 360
        self._height = 720
        self.setSceneRect(0, 0, self._width, self._height)

        # set color
        self.setBackgroundBrush(QBrush(QColor('#000000')))

    def setView(self, view):
        self._view = view


class PEView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = None

        # config display params
        self.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def setScene(self, scene):
        self._scene = scene


class ParamsEditor(QWidget):
    def __init__(self, scene=None, view=None, parent=None):
        super().__init__(parent=parent)

        self.setGeometry(100, 100, 360, 360)
        self.setWindowTitle("Params Editor For Daisy")

        self._view = PEView()
        self._scene = PEScene()
        self._view.setScene(self._scene)
        self._scene.setView(self._view)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._view)
        self.layout.setContentsMargins(5, 5, 5, 5)

        # self._module_name = "Linear"
        #
        # self._module_qlable = QLabel(self._module_name)
        # self.layout.addWidget(self._module_qlable)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pe = ParamsEditor()
    sys.exit(app.exec())
