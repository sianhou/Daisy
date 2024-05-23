# coding:utf-8
from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QFont, QPainter, QPainterPath, QPolygonF
from PySide6.QtWidgets import QGraphicsItem


class NodePort(QGraphicsItem):
    PORT_TYPE_EXEC_IN = 1001
    PORT_TYPE_EXEC_OUT = 1002
    PORT_TYPE_PARAM = 1003
    PORT_TYPE_OUTPUT = 1004

    def __init__(self, port_label='', port_class='str', port_color='#ffffff', port_type=PORT_TYPE_EXEC_IN, parent=None):
        super(NodePort, self).__init__(parent)

        self._port_label = port_label
        self._port_class = port_class
        self._port_color = port_color
        self._port_type = port_type

        # 定义PenheBrush
        self._pen_default = QPen(QColor(self._port_color))
        self._pen_default.setWidthF(1.5)
        self._brush_default = QBrush(QColor(self._port_color))
        self._font_size = 12
        self._port_font = QFont('Consolas', self._font_size)

        self._port_icon_size = 20
        self._port_label_size = len(self._port_label) * self._font_size
        self._port_width = self._port_icon_size + self._port_label_size

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._port_width, self._port_icon_size)

    # def paint(self, painter: QPainter, option, widget) -> None:
    #     super().paint(painter, option, widget)

    # 将本节点添加到parent node上
    def add_to_paraent_node(self, parent_node, scene):
        self.setParentItem(parent_node)
        self._parent_node = parent_node
        self._scene = scene


class EXECPort(NodePort):
    def __init__(self, port_label='', port_class='str', port_color='#ffffff', port_type=NodePort.PORT_TYPE_EXEC_IN,
                 parent=None):
        super().__init__(port_label, port_class, port_color, port_type, parent)

    def paint(self, painter: QPainter, option, widget) -> None:
        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(0, 0.2 * self._port_icon_size))
        poly.append(QPointF(0.25 * self._port_icon_size, 0.2 * self._port_icon_size))
        poly.append(QPointF(0.5 * self._port_icon_size, 0.5 * self._port_icon_size))
        poly.append(QPointF(0.25 * self._port_icon_size, 0.8 * self._port_icon_size))
        poly.append(QPointF(0, 0.8 * self._port_icon_size))

        port_outline.addPolygon(poly)
        painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(port_outline.simplified())


class EXECInPort(EXECPort):
    def __init__(self):
        super().__init__(port_type=NodePort.PORT_TYPE_EXEC_IN)


class EXECOutPort(EXECPort):
    def __init__(self):
        super().__init__(port_type=NodePort.PORT_TYPE_EXEC_OUT)


class ParamPort(NodePort):
    def __init__(self, port_label='', port_class='str', port_color='#ffffff', parent=None):
        super().__init__(port_label, port_class, port_color, NodePort.PORT_TYPE_PARAM, parent)

    def paint(self, painter: QPainter, option, widget) -> None:
        # icon o> 表示
        painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(0.25 * self._port_icon_size, 0.5 * self._port_icon_size),
                            0.25 * self._port_icon_size, 0.25 * self._port_icon_size)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_default)
        poly = QPolygonF()
        poly.append(QPointF(0.6 * self._port_icon_size, 0.35 * self._port_icon_size))
        poly.append(QPointF(0.7 * self._port_icon_size, 0.50 * self._port_icon_size))
        poly.append(QPointF(0.6 * self._port_icon_size, 0.65 * self._port_icon_size))
        painter.drawPolygon(poly)

        # port label
        painter.setPen(self._pen_default)
        painter.drawText(
            QRectF(self._port_icon_size, 0.1 * self._port_icon_size, self._port_label_size, self._port_icon_size),
            Qt.AlignmentFlag.AlignLeft, self._port_label)


class OutputPort(NodePort):
    def __init__(self, port_label='', port_class='str', port_color='#ffffff', parent=None):
        super().__init__(port_label, port_class, port_color, NodePort.PORT_TYPE_OUTPUT, parent)

    def paint(self, painter: QPainter, option, widget) -> None:
        # paint label
        painter.setPen(self._pen_default)
        painter.drawText(
            QRectF(0, 0.1 * self._port_icon_size, self._port_label_size, self._port_icon_size),
            Qt.AlignmentFlag.AlignRight, self._port_label)

        # icon o> 表示
        painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(self._port_label_size + 0.5 * self._port_icon_size,
                                    0.5 * self._port_icon_size), 0.25 * self._port_icon_size,
                            0.25 * self._port_icon_size)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_default)
        poly = QPolygonF()
        poly.append(QPointF(self._port_label_size + 0.85 * self._port_icon_size, 0.35 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.95 * self._port_icon_size, 0.50 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.85 * self._port_icon_size, 0.65 * self._port_icon_size))
        painter.drawPolygon(poly)
