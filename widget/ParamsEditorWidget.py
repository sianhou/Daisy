from PySide6.QtCore import QRectF
from PySide6.QtGui import Qt, QPainterPath
from PySide6.QtWidgets import QWidget, QGraphicsItem


class ParamsEditor(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._width = 300
        self._height = 200
        self._raduis = 20

    def paint(self, painter, option, widget):
        # 画背景颜色
        node_line = QPainterPath()
        node_line.addRoundedRect(0, 0, self._width, self._height, self._raduis, self._raduis)
        painter.setPen(self._default_pen)
        painter.setBrush(self._background_brush)
        painter.drawPath(node_line.simplified())

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)


class ParamsEditorWidget(QWidget):
    def __init__(self, parent=None):
        super(ParamsEditorWidget, self).__init__(parent=parent)
        self.pos = (0, 0)
        self.resize(300, 200)
        # 设置永远在最顶层显示
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
