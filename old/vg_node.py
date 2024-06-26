# coding: utf-8
from abc import abstractmethod
from typing import List

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsDropShadowEffect

from node.port import NodePort
from vg_config import NodeConfig, EditorConfig


class GraphNode(QGraphicsItem):
    def __init__(self, title="", param_ports=None, output_ports=None, is_pure=True, scene=None, node_position=None,
                 connected_nodes=None, edges=None, parent=None):
        super(GraphNode, self).__init__(parent)

        self._scene = scene

        self._node_position = node_position
        self._connected_nodes = connected_nodes if connected_nodes is not None else []
        self._edges = edges if edges is not None else []

        self.setFlags(
            QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)

        self.setNode()
        self.setupOutline()
        self.setupTitle(title=title)

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

        self.updateWidthHeight()
        self.init_ports()

        # if not is_pure:
        #     self.init_exec_ports()

        # 选中投影
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)
        self._shadow_color = QColor('#aaeeee00')

        # self.setZValue(0)

    def setNode(self, width=100, height=35, min_height=40, min_width=8, port_space=60, radius=4,
                background_color='#aa151515'):
        self._node_width = width
        self._node_height = height
        self._node_radius = radius
        self._node_port_space = port_space
        self._node_width_min = min_width
        self._node_height_min = min_height  # TODO(HOUSIAN): using self._title_height and self._node_radius to calculate a proper value
        self._brush_background = QBrush(QColor(background_color))

    def setupOutline(self, color='#4e90fe', color_selected='#aaffee00'):
        self._pen_default = QPen(QColor(color))
        self._pen_selected = QPen(QColor(color_selected))

    def setupTitle(self, title="", height=35, font='Arial', font_size=16, color='#eeeeee', background_color='#aa4e90fe',
                   padding=5):
        self._title = title
        self._title_height = height
        self._title_font = QFont(font, font_size)
        self._title_font_size = font_size
        self._title_color = QColor(color)
        self._title_padding = padding
        self._title_background_brush = QBrush(QColor(background_color))

        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._title_font)
        self._title_item.setDefaultTextColor(self._title_color)
        self._title_item.setPos(self._title_padding, self._title_padding)
        _width = self._title_font_size * len(self._title)
        if self._node_width < _width:
            self._node_width = _width

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

    def updateWidthHeight(self):
        # param_ports
        height = len(self._param_ports) * (
                NodeConfig.port_icon_size + self._port_padding) + self._node_height_min

        if self._node_height < height:
            self._node_height = height

        self._max_param_port = 0
        if self._param_ports != None:
            for _, port in enumerate(self._param_ports):
                if self._max_param_port < port._port_width:
                    self._max_param_port = port._port_width

        # output_ports
        height = len(self._output_ports) * (
                NodeConfig.port_icon_size + self._port_padding) + self._node_height_min

        if self._node_height < height:
            self._node_height = height

        self._max_output_port = 0
        if self._output_ports != None:
            for _, port in enumerate(self._output_ports):
                if self._max_output_port < port._port_width:
                    self._max_output_port = port._port_width
        # width
        if self._node_width < self._max_param_port + self._max_output_port + self._node_port_space:
            self._node_width = self._max_param_port + self._max_output_port + self._node_port_space

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
        painter.setBrush(self._title_background_brush)
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
    package_name = ''
    node_title = ''
    node_description = ''

    input_pins = None
    output_pins = None

    def __init__(self):

        # self.setup()

        self.is_validate()

        self.in_ports: List[NodePort] = [pin.init_port() for pin in self.input_pins]
        self.out_ports: List[NodePort] = [pin.init_port() for pin in self.output_pins]
        super().__init__(title=self.node_title, param_ports=self.in_ports, output_ports=self.out_ports, is_pure=True)

        self.setNode()
        color = NodeConfig.node_title_back_color.get(self.package_name, '#4e90fe')
        self.setupOutline(color=color)

        background_color = NodeConfig.node_title_back_color.get(self.package_name, '#4e90fe')
        self.setupTitle(title=self.node_title, height=35, font=EditorConfig.editor_node_title_font,
                        font_size=EditorConfig.editor_node_title_font_size, color='#eeeeee',
                        background_color=background_color, padding=5)
        self.updateWidthHeight()
        self._input_data_ready = False
        self._output_data_ready = False

    def exec(self, index):
        pass

    # 通过index获取一个pin的值如果pin的值为空，需要通过递归获取关联port的值
    def input(self, index):
        # 判断当前pin是否是可以获取数据的
        if not self.input_pins[index]._pin_type == 'data':
            # TODO(housian): logging
            print('Node: ', self.node_title, ', index: ', index, ' is not data port.')
            return None

        port = self.in_ports[index]
        port_value = port.getDefaultValue()

        if port_value is None:
            pass

        return port_value
        # if port._ha
        # if pin.has_set_value:
        #     return pin.getValue()

        # 一种带有widget 且widget可见

        # pin_value = pin.getPort().getDefaultValue()
        # if pin_value is not None:
        #     if pin._pin_class == dtype.Int:
        #         pin.setValue(int(pin_value))
        #     elif pin._pin_class == dtype.Float:
        #         pin.setValue(float(pin_value))
        #     elif pin._pin_class == dtype.Bool:
        #         pin.setValue(bool(pin_value))
        #     elif pin._pin_class == dtype.String:
        #         pin.setValue(pin_value)
        #     else:
        #         # TODO(housian)
        #         pass
        #     pin._has_set_value = True
        # else:
        #     # TODO(housian)
        #     pass
        # 一种不带有widget

    def is_validate(self):
        if self.node_title == '' or self.node_title is None:
            print('Node title could note be Empty or None.')
            return False

        if self.input_pins is None:
            print('Node input pins could note be Empty or None.')
            return False

        if self.output_pins is None:
            self.output_pins = []

        return True

    # 通过index设置一个pin的输出值，到下一个相连节点的port
    def output(self, index, value):
        if not self.output_pins[index]._pin_type == 'data':
            # TODO(housian): logging
            print('Node: ', self.node_title, ', index: ', index, ' is not data port.')
            return None

        port = self.out_ports[index]
        port.setValue(value)
        # pin.setValue(value)

    @abstractmethod
    def runSelf(self):
        pass

    def runNext(self):
        for pin in self.output_pins:
            if pin._pin_type == 'exec':
                pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    def run_output(self, index):

        # 判断当前pin是否是可以执行的
        if not self.output_pins[index]._pin_type == 'exec':
            # TODO(housian): logging
            print('Node: ', self.node_title, ', index: ', index, ' is not exec port.')
            return

        port = self.out_ports[index]
        # 如果当前pin是可以自行的，获得当前pin对应的node
        ports = port.getConnectedPorts()
        for port in ports:
            parent_node = port.getParentNode()
            parent_node.run()
