from PySide6.QtCore import QRectF, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent

from core import dtype
from env.config import EditorConfig


class PortBase(QGraphicsItem):
    def __init__(self, port_color='#a1a1a1', port_dtype: dtype.DtypeBase = dtype.Int, port_radius=7, parent=None):
        super(PortBase, self).__init__(parent)
        self._port_color = port_color
        self._port_dtype = port_dtype
        self._port_radius = port_radius
        self._port_size = 2 * port_radius
        self._default_pen = QPen(QColor(self._port_color))
        self._default_pen.setWidthF(2)
        self._default_brush = QBrush(QColor(EditorConfig.background_color))
        self._parent_node = None
        self._edges = []

    def getParentNode(self):
        return self._parent_node

    def addToParentNode(self, node):
        self._parent_node = node
        self.setParentItem(node)

    # override QT function
    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._port_size, self._port_size)

    def paint(self, painter: QPainter, option, widget) -> None:
        if len(self._edges) == 0:
            painter.setPen(self._default_pen)
            painter.setBrush(self._default_brush)
            painter.drawEllipse(QPointF(self._port_radius, self._port_radius),
                                self._port_radius, self._port_radius)
        else:
            painter.setPen(self._default_pen)
            painter.setBrush(QBrush(QColor(self._port_color)))
            painter.drawEllipse(QPointF(self._port_radius, self._port_radius),
                                self._port_radius, self._port_radius)

    def addEdge(self, edge):
        self._edges.append(edge)

    def getPos(self):
        self._port_pos = (self.scenePos().x(), self.scenePos().y())
        return self._port_pos

    def getCenterPos(self):
        self._port_pos = (self.scenePos().x() + self._port_radius, self.scenePos().y() + self._port_radius)
        return self._port_pos

    # override qt function
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        # Check Item Scene Association: Before ungrabbing the mouse,
        # ensure the item is still part of a scene.
        if self.scene() is not None:
            self.ungrabMouse()
        super().mouseReleaseEvent(event)


class InputPort(PortBase):
    def __init__(self, port_dtype: dtype.DtypeBase = dtype.Float, parent=None):
        super(InputPort, self).__init__(port_color=port_dtype.dtype_color, port_dtype=port_dtype, parent=parent)


class OutputPort(PortBase):
    def __init__(self, port_dtype: dtype.DtypeBase = dtype.Float, parent=None):
        super(OutputPort, self).__init__(port_color=port_dtype.dtype_color, port_dtype=port_dtype, parent=parent)
