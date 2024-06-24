from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor, QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsItem

from core.paramitem import ParamItemList, ParamItem


class ParamCard(QGraphicsItem):
    def __init__(self, params_list: ParamItemList, parent=None):
        super().__init__(parent=parent)

        self._width = ParamItem._param_padding
        self._height = ParamItem._param_padding
        self._raduis = 10

        self._background_brush = QBrush(QColor('#aa151515'))
        self._default_pen = QPen(QColor('#a1a1a1'))

        if len(params_list) > 0:
            for i, param in enumerate(params_list):
                temp_width = param._width + 2 * param._param_padding
                self._width = temp_width if temp_width > self._width else self._width
                param.setParentItem(self)
                param.setPos(param._param_padding, self._height)
                self._height += param._height + param._param_padding

        self.setZValue(10)

    def paint(self, painter, option, widget):
        # 画背景颜色
        node_line = QPainterPath()
        node_line.addRoundedRect(0, 0, self._width, self._height, self._raduis, self._raduis)
        painter.setPen(self._default_pen)
        painter.setBrush(self._background_brush)
        painter.drawPath(node_line.simplified())

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._width, self._height)

    def addToParaentNode(self, node):
        self._parent_node = node
        self.setParentItem(node)
