# coding:utf-8
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, QColor, QPainter, QPainterPath, Qt, QPolygonF
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsDropShadowEffect, QGraphicsItem

from node.port import NodePort


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
        self._source_port.update()
        self._target_port.update()

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

    def remove_self(self):
        self._scene.removeItem(self)
        self._scene._view.remove_edge(self)
        self._source_port.remove_edge(self)
        self._target_port.remove_edge(self)
        self._source_port.update()
        self._target_port.update()

    # 更新路径
    def update_edge_path(self):
        source_pos = self._source_port.get_port_pos()
        target_pos = self._target_port.get_port_pos()

        path = QPainterPath(source_pos)

        x_width = source_pos.x() - target_pos.x()
        x_width = x_width + 0.01 if x_width == 0 else x_width
        y_height = abs(target_pos.y() - source_pos.y())

        tagnent = float(y_height) / x_width * 0.5
        tagnent *= x_width

        if x_width > 0:
            if x_width > 150:
                x_width = 150
            tagnent += x_width

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

    def is_connectable(self):
        # 判断是否可以链接
        if self.is_pair() and not self.is_same_node() and self.is_same_class():
            return True
        return False

    def is_pair(self):
        if self._source_port._port_type == NodePort.PORT_TYPE_EXEC_OUT and self._target_port._port_type == NodePort.PORT_TYPE_EXEC_IN:
            return True
        elif self._source_port._port_type == NodePort.PORT_TYPE_OUTPUT and self._target_port._port_type == NodePort.PORT_TYPE_PARAM:
            return True
        else:
            return False

    def is_same_node(self):
        if self._source_port._parent_node == self._target_port._parent_node:
            return True
        return False

    def is_same_class(self):
        if self._source_port._port_class == self._target_port._port_class:
            return True
        return False

    def create_node_edge(self):
        if self.is_connectable():
            edge = NodeEdge(self._source_port, self._target_port, self._scene, self._edge_color)
            return edge
        return None

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

    def update_edge_path(self):
        source_pos = self._source_pos
        target_pos = self._target_pos

        path = QPainterPath(source_pos)

        x_width = source_pos.x() - target_pos.x()
        x_width = x_width + 0.01 if x_width == 0 else x_width
        y_height = abs(target_pos.y() - source_pos.y())

        tagnent = float(y_height) / x_width * 0.5

        tagnent *= x_width

        if x_width > 0:
            if x_width > 150:
                x_width = 150
            tagnent += x_width

        path.cubicTo(QPointF(source_pos.x() + tagnent, source_pos.y()),
                     QPointF(target_pos.x() - tagnent, target_pos.y()),
                     target_pos)

        self.setPath(path)

    def update_position(self, position):
        if self._drag_from_source:
            self._target_pos = position
        else:
            self._source_pos = position
        self.update()


class CuttingLine(QGraphicsPathItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._line_points = []
        self._pen = QPen(Qt.red)
        self._pen.setWidthF(1.5)
        self._pen.setDashPattern([3, 3])

    def paint(self, painter: QPainter, option, widget) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self._line_points)
        painter.drawPolyline(poly)

    def update_points(self, point):
        self._line_points.append(point)
        self.update()

    def remove_intersect_edges(self, edges):
        for edge in edges.copy():
            path = QPainterPath()
            path.addPolygon(QPolygonF(self._line_points))

            if edge.collidesWithPath(path):
                edge.remove_self()
