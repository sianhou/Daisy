from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor, QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsItem, QGraphicsProxyWidget

from core.parampin import ParamPinList


class ParamsEditorPanel(QGraphicsItem):
    def __init__(self):
        super().__init__()

        self._width = 300
        self._height = 200
        self._raduis = 20

        self._background_brush = QBrush(QColor('#aa151515'))
        self._default_pen = QPen(QColor('#a1a1a1'))

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

    def setupParamsPlane(self, params_list: ParamPinList):
        print(1)
        if len(params_list) > 0:
            for i, param in enumerate(params_list):
                param._proxy = QGraphicsProxyWidget(parent=self)
                param._proxy.setWidget(param._default_widget)
                param._proxy.setPos(10, 10 + i * 100)

        pass
