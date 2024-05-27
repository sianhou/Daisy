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

        self.setZValue(0.5)

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
        self._source_port.add_edge(self, self._target_port)
        self._target_port.add_edge(self, self._source_port)

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

        x_width = abs(target_pos.x() - source_pos.x()) + 1
        y_height = abs(target_pos.y() - source_pos.y())

        tagnent = float(y_height) / float(x_width) * 0.5
        tagnent = tagnent if tagnent < 1 else 1

        tagnent *= x_width

        path.cubicTo(QPointF(source_pos.x() + tagnent, source_pos.y()),
                     QPointF(target_pos.x() - tagnent, target_pos.y()),
                     target_pos)

        self.setPath(path)


class DraggingEdge(QGraphicsPathItem):
    def __init__(self, source_pos, target_pos, scene=None, edge_color='#ffffff', drag_from_source=True, parent=None):
        super().__init__(parent)

        self._source_pos = source_pos
        self._target_pos = target_pos
        self._edge_color = edge_color
        self._scene = scene
        self._drag_from_source = drag_from_source

        self._pen_default = QPen(QColor(self._edge_color))
        self._pen_default.setWidthF(2)

        self._source_port = None
        self._target_port = None

        self.setZValue(-1)

        # 选中投影
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)
        self._shadow_color = Qt.yellow
        self.setFlags(QGraphicsItem.ItemIsSelectable)

    def paint(self, painter: QPainter, option, widget) -> None:
        self.update_edge_path()

        painter.setPen(self._pen_default)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

        self._shadow.setColor(self._shadow_color)
        self.setGraphicsEffect(self._shadow)

    def update_edge_path(self):
        source_pos = self._source_pos
        target_pos = self._target_pos

        path = QPainterPath(source_pos)

        x_width = abs(target_pos.x() - source_pos.x()) + 1
        y_height = abs(target_pos.y() - source_pos.y())

        tagnent = float(y_height) / float(x_width) * 0.5
        tagnent = tagnent if tagnent < 1 else 1

        tagnent *= x_width

        path.cubicTo(QPointF(source_pos.x() + tagnent, source_pos.y()),
                     QPointF(target_pos.x() - tagnent, target_pos.y()),
                     target_pos)

        self.setPath(path)

    def set_first_port(self, port: NodePort):
        if self._drag_from_source:
            self._source_port = port
        else:
            self._target_port = port

    def set_second_port(self, port: NodePort):
        if not self._drag_from_source:
            self._source_port = port
        else:
            self._target_port = port

    def update_position(self, position):
        if self._drag_from_source:
            self._target_pos = position
        else:
            self._source_pos = position
        self.update()

    def create_node_edge(self):
        if self.is_connectable():
            NodeEdge(self._source_port, self._target_port, self._scene, self._edge_color)

    def is_connectable(self):
        # 判断是否可以链接
        if self.is_pair():
            return True
        return False

    def is_pair(self):
        if self._source_port._port_type == NodePort.PORT_TYPE_EXEC_OUT and self._target_port._port_type == NodePort.PORT_TYPE_EXEC_IN:
            return True
        elif self._source_port._port_type == NodePort.PORT_TYPE_OUTPUT and self._target_port._port_type == NodePort.PORT_TYPE_PARAM:
            return True
        else:
            return False
