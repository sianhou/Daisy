# coding: utf-8
from abc import abstractmethod

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsDropShadowEffect

from vg_config import EditorConfig
from vg_node_port import NodePort, EXECInPort, EXECOutPort


class GraphNode(QGraphicsItem):
    def __init__(self, title="", param_ports=None, output_ports=None, is_pure=True, scene=None, node_position=None,
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
        self._port_space = 10
        self._node_width_min = 2 * self._node_radius
        self._node_height_min = 40  # TODO(HOUSIAN): using self._title_height and self._node_radius to calculate a proper value

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
        self._title_font_size = EditorConfig.editor_node_title_font_size
        self._title_font = QFont(EditorConfig.editor_node_title_font, self._title_font_size)
        self._title_color = Qt.white
        self._title_padding = 5
        self._brush_title_back = QBrush(QColor('#aa00002f'))
        self.init_title()

        # exec Port
        self._port_padding = 7
        self._port_exec_index = 0

        # param ports &output ports
        self._port_index = 0

        if not is_pure:
            self._node_height_min = 20 + 2 * self._node_radius

        # param ports
        self._param_ports = param_ports
        self._output_ports = output_ports

        self.init_node_height_and_width()
        self.init_ports()

        # if not is_pure:
        #     self.init_exec_ports()

        # 选中投影
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)
        self._shadow_color = QColor('#22eeee00')

    def add_connected_node(self, node, edge):
        self._connected_nodes.append(node)
        self._edges.append(edge)

    def add_exec_in_port(self, port: NodePort, index=0):
        port.add_to_parent_node(self, self._scene)
        x = self._port_padding
        y = self._title_height + index * (self._port_padding + port._port_icon_size) + self._port_padding
        port.setPos(x, y)

    def add_exec_out_port(self, port: NodePort, index=0):
        port.add_to_parent_node(self, self._scene)
        x = self._node_width - port._port_width - self._port_padding
        y = self._title_height + index * (self._port_padding + port._port_icon_size) + self._port_padding
        port.setPos(x, y)

    def add_output_port(self, port: NodePort, index=0):
        port.add_to_parent_node(self, self._scene)
        x = self._node_width - port._port_width - self._port_padding
        y = self._title_height + index * (self._port_padding + port._port_icon_size) + self._port_padding
        port.setPos(x, y)

    def add_param_port(self, port: NodePort, index=0):
        port.add_to_parent_node(self, self._scene)
        x = self._port_padding
        y = self._title_height + index * (self._port_padding + port._port_icon_size) + self._port_padding
        port.setPos(x, y)

    def add_port(self, port: NodePort, index=0):
        if port._port_type == NodePort.PORT_TYPE_EXEC_IN:
            self.add_exec_in_port(port, index)
        elif port._port_type == NodePort.PORT_TYPE_EXEC_OUT:
            self.add_exec_out_port(port, index)
        elif port._port_type == NodePort.PORT_TYPE_PARAM:
            self.add_param_port(port, index)
        elif port._port_type == NodePort.PORT_TYPE_OUTPUT:
            self.add_output_port(port, index)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._node_width, self._node_height)

    # def init_exec_ports(self):
    #     execin = EXECInPort()
    #     execout = EXECOutPort()
    #     self.add_port(execin)
    #     self.add_port(execout)

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
                self.add_port(port, index=i)

    def init_param_ports(self):
        if self._param_ports != None:
            for i, port in enumerate(self._param_ports):
                self.add_port(port, index=i)

    def init_ports(self):
        # 参数
        self.init_param_ports()
        # 输出
        self.init_output_ports()

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

        # 选中投影设置， 最先画是为了放在最底层
        if not self.isSelected():
            self._shadow.setColor('#00000000')
            self.setGraphicsEffect(self._shadow)
        else:
            # 选中投影设置
            self._shadow.setColor(self._shadow_color)
            self.setGraphicsEffect(self._shadow)

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

    def remove_connected_node(self, node, edge):
        self._connected_nodes.remove(node)
        if edge in self._edges:
            self._edges.remove(edge)

    # 删除自己
    def remove_self(self):
        # 删除edge
        for edge in self._edges.copy():
            edge.remove_self()
        # 删除node
        self._scene.removeItem(self)
        self._scene._view.remove_node(self)

    def set_scene(self, scene):
        self._scene = scene


class Node(GraphNode):

    def __init__(self):
        self.node_title = ''
        self.node_description = ''

        self.input_pins = None
        self.output_pins = None

        self.setup_node()

        self.is_validate()

        in_ports = [pin.port for pin in self.input_pins]
        out_ports = [pin.port for pin in self.output_pins]
        super().__init__(title=self.node_title, param_ports=in_ports, output_ports=out_ports, is_pure=True)

        self._input_data_ready = False
        self._output_data_ready = False

    def is_validate(self):
        if self.node_title == '' or self.node_title is None:
            print('Node title could note be Empty or None.')
            return False

        if len(self.input_pins) == 0 or self.input_pins is None:
            print('Node input pins could note be Empty or None.')
            return False

        if self.output_pins is None:
            self.output_pins = []

        return True

    @abstractmethod
    def run_node(self):
        pass

    @abstractmethod
    def setup_node(self):
        pass
