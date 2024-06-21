from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QPen, QColor, QFont, QPainterPath, Qt
from PySide6.QtWidgets import QGraphicsTextItem

from core.node.node import NodeBase
from core.port import OutputPort, InputPort


class MiniNode(NodeBase):
    def __init__(self, parent=None):
        super(MiniNode, self).__init__(parent)
        self.setup()

    def addInputPort(self, port: InputPort, pos=[0, 0]):
        port.addToParentNode(self)
        port.setPos(pos[0], pos[1])
        self._input_ports.append(port)

    def addInputPortList(self, port_list: [InputPort] = None):
        if len(port_list) != 0:
            total_width = (len(port_list) - 1) * (self._port_space + port_list[0]._port_size)
            x = self.getShape()[0] / 2 - total_width / 2 - port_list[0]._port_radius
            y = 0 - port_list[0]._port_radius
            for i, port in enumerate(port_list):
                self.addInputPort(port=port, pos=[x + i * (self._port_space + port_list[0]._port_size), y])
        else:
            # TODO(housian): debug
            pass

    def addOutputPort(self, port: OutputPort, pos=[0, 0]):
        port.addToParentNode(self)
        self._output_ports.append(port)
        port.setPos(pos[0], pos[1])

    def addOutputPortList(self, port_list: [OutputPort] = None):
        if len(port_list) != 0:
            total_width = (len(port_list) - 1) * (self._port_space + port_list[0]._port_size)
            x = self.getShape()[0] / 2 - total_width / 2 - port_list[0]._port_radius
            y = self.getShape()[1] - port_list[0]._port_radius
            for i, port in enumerate(port_list):
                self.addOutputPort(port=port, pos=[x + i * (self._port_space + port_list[0]._port_size), y])
        else:
            # TODO(housian): debug
            pass

    def getShape(self):
        return (self._node_width, self._node_height)

    def getPos(self):
        return (self.x, self.y)

    def getInputPort(self):
        return self._input_ports

    def getOutputPort(self):
        return self._output_ports

    def setup(self, width=200, height=40, radius=4, background_color='#aa151515', outline_color='#a1a1a1',
              outline_selected_color='#aaffee00', icon_padding=5, icon_color='#88df00'):
        # body
        self._node_width = width
        self._node_height = height
        self._node_radius = radius
        self._background_brush = QBrush(QColor(background_color))
        self._default_pen = QPen(QColor(outline_color))
        self._default_pen.setWidthF(2)
        self._selected_pen = QPen(QColor(outline_selected_color))

        # icon
        self._icon_padding = icon_padding
        temp_size = self._node_width if self._node_width < self._node_height else self._node_height
        self._icon_size = temp_size - 2 * self._icon_padding
        self._icon_radius = radius * self._icon_size / temp_size
        self._icon_background_brush = QBrush(QColor(icon_color))
        self.update()

    def setTitle(self, title="", font='Arial', font_size=10, color='#eeeeee', background_color='#aa4e90fe',
                 padding=5):
        self._title = title
        self._title_font = QFont(font, font_size)
        self._title_font_size = font_size
        self._title_color = QColor(color)
        self._title_padding = padding
        self._title_background_brush = QBrush(QColor(background_color))

        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._icon_size + self._icon_padding + self._title_padding,
                                self._icon_padding)
        self.update()

    # override QT function
    def paint(self, painter, option, widget):
        # 画背景颜色
        node_line = QPainterPath()
        node_line.addRoundedRect(0, 0, self._node_width, self._node_height, self._node_radius, self._node_radius)
        painter.setPen(self._default_pen)
        painter.setBrush(self._background_brush)
        painter.drawPath(node_line.simplified())

        # plot icon
        icon_line = QPainterPath()
        icon_line.setFillRule(Qt.WindingFill)
        icon_line.addRoundedRect(self._icon_padding, self._icon_padding, self._icon_size, self._icon_size,
                                 self._icon_radius, self._icon_radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._icon_background_brush)
        painter.drawPath(icon_line.simplified())

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)
