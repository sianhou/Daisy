import sys

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QBrush, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem

from core.node.node import NodeBase
from dlpkg.op import Linear


class PEConfig:
    _width = 360
    _height = 480


class PEScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._view = None

        # set size
        self._width = PEConfig._width
        self._height = PEConfig._height
        self.setSceneRect(0, 0, self._width, self._height)

        # set color
        self.setBackgroundBrush(QBrush(QColor('#ffffff')))

    def setView(self, view):
        self._view = view


class PEView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = None

        # config display params
        self.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        print(self.rect())

    def setScene(self, scene):
        self._scene = scene
        super().setScene(scene)
        self.update()

    def resizeEvent(self, event):
        super(PEView, self).resizeEvent(event)
        new_rect = self.rect()
        print(self.mapToGlobal(new_rect.topLeft()))
        print(f"QGraphicsView rect changed: {new_rect}")


class PEItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._width = 300
        self._height = 300

        background_color = '#00151515'
        outline_color = '#ffffff'
        outline_selected_color = '#aaffee00'
        self._radius = 5

        self._background_brush = QBrush(QColor(background_color))
        self._default_pen = QPen(QColor(outline_color))
        self._default_pen.setWidthF(2)
        self._selected_pen = QPen(QColor(outline_selected_color))

    def setupParam(self, node: NodeBase):
        print(node)

    def paint(self, painter, option, widget):
        # 画背景颜色
        node_line = QPainterPath()
        node_line.addRoundedRect(0, 0, self._width, self._height, self._radius, self._radius)
        painter.setPen(self._default_pen)
        painter.setBrush(self._background_brush)
        painter.drawPath(node_line.simplified())

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._width, self._height)


class ParamsEditor(QWidget):
    def __init__(self, scene=None, view=None, parent=None):
        super().__init__(parent=parent)

        self.setGeometry(1200, 500, PEConfig._width, PEConfig._height)
        self.setWindowTitle("Params Editor For Daisy")

        self._view = PEView()
        self._scene = PEScene()
        self._view.setScene(self._scene)
        self._scene.setView(self._view)

        self._view.centerOn(0, 0)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self._view)
        self.layout.setContentsMargins(0, 0, 0, 0)

        test_node = Linear()
        op = PEItem()
        op.setupParam(test_node)

        self._scene.addItem(op)
        op.setPos(0, 0)

        self.show()

    def resizeEvent(self, event):
        super(ParamsEditor, self).resizeEvent(event)
        # new_rect = self.rect()
        # print(self.mapToGlobal(new_rect.topLeft()))
        # print(f"Widget rect changed: {new_rect}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pe = ParamsEditor()
    sys.exit(app.exec())
