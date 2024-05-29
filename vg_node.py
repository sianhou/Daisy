# coding: utf-8
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem

from vg_node_port import NodePort, EXECInPort, EXECOutPort


class GraphNode(QGraphicsItem):
    def __init__(self, title="", param_ports=None, output_ports=None, is_pure=False, scene=None, node_position=None,
                 connected_nodes=None, edges=None, parent=None):
        super(GraphNode, self).__init__(parent)

        self._scene = scene

        self._node_position = node_position
        self._connected_nodes = connected_nodes if connected_nodes is not None else []
        self._edges = edges if edges is not None else []

        # 定义node大小
        self._node_width = 100
        self._node_height = 100
        self._node_radius = 10
        self._port_space = 50
        self._node_width_min = 2 * self._node_radius
        self._node_height_min = 40 + 2 * self._node_radius  # TODO(HOUSIAN): using self._title_height and self._node_radius to calculate a proper value

        # 定义node边框
        self._pen_default = QPen(QColor('#151515'))
        self._pen_selected = QPen(QColor('#aaffee00'))
        # node背景
        self._brush_background = QBrush(QColor('#aa151515'))

        self.setFlags(
            QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)

        # 节点的title
        self._title = title
        # title的高度
        self._title_height = 35
        self._title_font_size = 13
        self._title_font = QFont("Arial", self._title_font_size)
        self._title_color = Qt.white
        self._title_padding = 3
        self._brush_title_back = QBrush(QColor('#aa00002f'))
        self.init_title()

        # exec Port
        self._port_padding = 6
        self._port_exec_index = 0

        # param ports &output ports
        self._port_index = 0
        self._param_ports = param_ports
        self._output_ports = output_ports
        if is_pure:
            self._node_height_min = 20 + 2 * self._node_radius
        else:
            self._port_index += 1
        self.init_node_height_and_width()
        self.init_param_ports()
        self.init_output_ports()
        if not is_pure:
            self.init_exec_ports()

    def add_connected_node(self, node, edge):
        self._connected_nodes.append(node)
        self._edges.append(edge)

    def remove_connected_node(self, node, edge):
        self._connected_nodes.remove(node)
        self._edges.remove(edge)

    def add_exec_in_port(self, port: NodePort):
        port.add_to_paraent_node(self, self._scene)
        port.setPos(self._port_padding, self._title_height)

    def add_exec_out_port(self, port: NodePort):
        port.add_to_paraent_node(self, self._scene)
        port.setPos(self._node_width + 0.5 * port._port_icon_size - port._port_width - self._port_padding,
                    self._title_height)

    def add_output_port(self, port: NodePort, index=0):
        port.add_to_paraent_node(self, self._scene)
        port.setPos(self._node_width - port._port_width - self._port_padding,
                    self._title_height + index * (self._port_padding + port._port_icon_size))

    def add_param_port(self, port: NodePort, index=0):
        port.add_to_paraent_node(self, self._scene)
        port.setPos(self._port_padding,
                    self._title_height + index * (self._port_padding + port._port_icon_size))

    def add_port(self, port: NodePort, index=0):
        if port._port_type == NodePort.PORT_TYPE_EXEC_IN:
            self.add_exec_in_port(port)
        elif port._port_type == NodePort.PORT_TYPE_EXEC_OUT:
            self.add_exec_out_port(port)
        elif port._port_type == NodePort.PORT_TYPE_PARAM:
            self.add_param_port(port, index)
        elif port._port_type == NodePort.PORT_TYPE_OUTPUT:
            self.add_output_port(port, index)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)

    def init_exec_ports(self):
        execin = EXECInPort()
        execout = EXECOutPort()
        self.add_port(execin)
        self.add_port(execout)

    def init_node_height_and_width(self):
        # param_ports
        height = len(self._param_ports) * (
                self._param_ports[0]._port_icon_size + self._port_padding) + self._node_height_min

        if self._node_height < height:
            self._node_height = height

        self._max_param_port = 0
        if self._param_ports != None:
            for _, port in enumerate(self._param_ports):
                if self._max_param_port < port._port_width:
                    self._max_param_port = port._port_width

        # output_ports
        height = len(self._output_ports) * (
                self._output_ports[0]._port_icon_size + self._port_padding) + self._node_height_min

        if self._node_height < height:
            self._node_height = height

        self._max_output_port = 0
        if self._output_ports != None:
            for _, port in enumerate(self._output_ports):
                if self._max_output_port < port._port_width:
                    self._max_output_port = port._port_width
        # width
        if self._node_width < self._max_param_port + self._max_output_port + self._port_space:
            self._node_width = self._max_param_port + self._max_output_port + self._port_space

    def init_output_ports(self):
        if self._output_ports != None:
            for i, port in enumerate(self._output_ports):
                self.add_port(port, index=i + self._port_index)

    def init_param_ports(self):
        if self._param_ports != None:
            for i, port in enumerate(self._param_ports):
                self.add_port(port, index=i + self._port_index)

    def init_title(self):
        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._title_padding, self._title_padding)
        width = self._title_font_size * len(self._title) + self._node_width_min

        if self._node_width < width:
            self._node_width = width

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if len(self._edges) > 0:
                for edge in self._edges:
                    edge.update()

        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        # 画背景颜色
        node_line = QPainterPath()
        node_line.addRoundedRect(0, 0, self._node_width, self._node_height, self._node_radius, self._node_radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(node_line.simplified())

        # 画title背景
        title_outline = QPainterPath()
        title_outline.setFillRule(Qt.WindingFill)
        title_outline.addRoundedRect(0, 0, self._node_width, self._title_height, self._node_radius, self._node_radius)
        title_outline.addRect(0, self._title_height - self._node_radius, self._node_radius, self._node_radius)
        title_outline.addRect(self._node_width - self._node_radius, self._title_height - self._node_radius,
                              self._node_radius, self._node_radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title_back)
        painter.drawPath(title_outline.simplified())

        if not self.isSelected():
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(node_line)
        else:
            painter.setPen(self._pen_selected)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(node_line)

    # 删除自己
    def remove_self(self):
        # 删除edge
        for edge in self._edges:
            edge.remove_self()
        # 删除node
        self._scene.removeItem(self)
        self._scene._view.remove_node(self)

    def set_scene(self, scene):
        self._scene = scene
