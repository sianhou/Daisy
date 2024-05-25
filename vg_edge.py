# coding:utf-8
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, QColor, QPainter, QPainterPath, Qt
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsDropShadowEffect, QGraphicsItem

from vg_node_port import NodePort


class NodeEdge(QGraphicsPathItem):

    def __init__(self, source_port: NodePort, target_port: NodePort, scene=None, edge_color='#ffffff', parent=None):
        super().__init__(parent)

        self._source_port = source_port
        self._target_port = target_port
        self._scene = scene

        self._edge_color = self._source_port._port_color
        self._pen_default = QPen(QColor(self._edge_color))
        self._pen_default.setWidthF(2)

        self.setZValue(-1)

        # 选中投影
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)
        self._shadow_color = Qt.yellow
        self.setFlags(QGraphicsItem.ItemIsSelectable)

        self.add_to_scene()

    def add_to_scene(self):
        self._scene.addItem(self)
        # 添加到相关的节点的port

    def paint(self, painter: QPainter, option, widget) -> None:
        self.update_edge_path()

        painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

        if self.isSelected():
            self._shadow.setColor(self._shadow_color)
            self.setGraphicsEffect(self._shadow)
        else:
            self._shadow.setColor('#00000000')
            self.setGraphicsEffect(self._shadow)

    # 更新路径
    def update_edge_path(self):
        source_pos = self._source_port.get_port_pos()
        target_pos = self._target_port.get_port_pos()

        path = QPainterPath(source_pos)

        x_width = abs(target_pos.x() - source_pos.x())
        y_height = abs(target_pos.y() - source_pos.y())

        tagnent = float(y_height) / float(x_width) * 0.5
        tagnent = tagnent if tagnent < 1 else 1

        tagnent *= x_width

        path.cubicTo(QPointF(source_pos.x() + tagnent, source_pos.y()),
                     QPointF(target_pos.x() - tagnent, target_pos.y()),
                     target_pos)

        self.setPath(path)
