from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor, QPainterPath, QPen, Qt, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem


class NodeBase(QGraphicsItem):
    def __init__(self, parent=None):
        super(NodeBase, self).__init__(parent)

        self.setFlags(
            QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)

        self._scene = None

    def setScene(self, scene):
        self._scene = scene


class DeepNetworkNode(NodeBase):
    def __init__(self, parent=None):
        super(DeepNetworkNode, self).__init__(parent)
        self.setup()

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
