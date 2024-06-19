from PySide6.QtCore import QRectF, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import QGraphicsItem

from env.config import EditorScene


class PortBase(QGraphicsItem):
    def __init__(self, port_color='#a1a1a1', port_size=7, parent=None):
        super(PortBase, self).__init__(parent)
        self._port_color = port_color
        self._port_size = port_size
        self._default_pen = QPen(QColor(self._port_color))
        self._default_pen.setWidthF(2)
        self._default_brush = QBrush(QColor(EditorScene.background_color))

    def addToParentNode(self, node):
        self._parent_node = node
        self.setParentItem(node)

    # override QT function
    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._port_size, self._port_size)

    def paint(self, painter: QPainter, option, widget) -> None:
        painter.setPen(self._default_pen)
        painter.setBrush(self._default_brush)
        painter.drawEllipse(QPointF(0, 0),
                            self._port_size, self._port_size)


class InputPort(PortBase):
    def __init__(self, parent=None):
        super(InputPort, self).__init__(parent=parent)


class OutputPort(PortBase):
    def __init__(self, parent=None):
        super(OutputPort, self).__init__(parent=parent)
