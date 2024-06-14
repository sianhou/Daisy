# coding:utf-8
from abc import abstractmethod

from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QFont, QPainter, QPainterPath, QPolygonF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsProxyWidget, QLineEdit, QCheckBox

from core import dtype
from vg_config import EditorConfig


class NodePort(QGraphicsItem):
    PORT_TYPE_EXEC_IN = 1001
    PORT_TYPE_EXEC_OUT = 1002
    PORT_TYPE_PARAM = 1003
    PORT_TYPE_OUTPUT = 1004

    def __init__(self, port_label='', port_class='str', port_color='#ffffff', port_type=PORT_TYPE_EXEC_IN,
                 default_widget=None, connected_ports=None, edges=None, parent=None):
        super(NodePort, self).__init__(parent)

        self._port_label = port_label
        self._port_class = port_class
        self._port_color = port_color
        self._port_type = port_type

        self._edges = edges if edges is not None else []
        self._connected_ports = connected_ports if connected_ports is not None else []

        # 定义PenheBrush
        self._pen_default = QPen(QColor(self._port_color))
        self._pen_default.setWidthF(1.5)
        self._brush_default = QBrush(QColor(self._port_color))
        self._font_size = EditorConfig.editor_node_pin_label_font_size
        self._port_font = QFont(EditorConfig.editor_node_pin_label_font, self._font_size)

        self._port_icon_size = 20
        self._port_label_size = len(self._port_label) * self._font_size
        self._port_width = self._port_icon_size + self._port_label_size

        # widget
        # 只有param port才有
        # 只有default != None
        # 传进来的default_widget参数是一个类，这里声明实例
        self._default_widget = None
        if default_widget is not None:
            print(default_widget)
            self._default_widget = default_widget()
            if isinstance(self._default_widget, QLineEdit):
                self._default_widget.setMaxLength(20)
            # elif isinstance(self._default_widget, QCheckBox):
            #     self._default_widget.setChecked(True)

    def add_edge(self, edge, port):
        self.conditioned_remove_edge()
        self._parent_node.add_connected_node(port._parent_node, edge)
        self._edges.append(edge)
        self._connected_ports.append(port)

    # 将本节点添加到parent node上
    def add_to_parent_node(self, parent_node, scene):

        self.setParentItem(parent_node)
        self._parent_node = parent_node
        self._scene = scene

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._port_width, self._port_icon_size)

    def conditioned_remove_edge(self):
        # 如果port_type == PORT_TYPE_EXEC_IN or PORT_TYPE_PARAM, 删除已有edge
        if self._port_type == NodePort.PORT_TYPE_EXEC_IN or self._port_type == NodePort.PORT_TYPE_PARAM:
            if len(self._edges) > 0:
                for edge in self._edges:
                    # 因为self._port_type == NodePort.PORT_TYPE_EXEC_IN or self._port_type == NodePort.PORT_TYPE_PARAM
                    # 所以当前port一定是一个target_port
                    # edge需要从source_port,source_port._parent_node中删除
                    # edge需要从target_port,target_port._parent_node中删除
                    edge.remove_self()

            # edge = self._edges.pop()
            # self._scene._edges.remove(edge)
            # self._

    def get_port_pos(self) -> QPointF:
        # 获得本身在scene的位置
        self._port_pos = self.scenePos()
        return QPointF(self._port_pos.x() + 0.25 * self._port_icon_size,
                       self._port_pos.y() + 0.5 * self._port_icon_size)

    def is_connected(self):
        return len(self._edges) > 0

    def remove_edge(self, edge):
        if not edge in self._edges:
            return
        self._edges.remove(edge)
        if edge._source_port == self:
            self._connected_ports.remove(edge._target_port)
            self._parent_node.remove_connected_node(edge._target_port._parent_node, edge)
        else:
            self._connected_ports.remove(edge._source_port)
            self._parent_node.remove_connected_node(edge._source_port._parent_node, edge)


class EXECPort(NodePort):
    def __init__(self, port_label='', port_class='str', port_color='#ffffff', port_type=NodePort.PORT_TYPE_EXEC_IN,
                 parent=None):
        super().__init__(port_label, port_class, port_color, port_type, parent)


class EXECInPort(EXECPort):
    def __init__(self, port_label=''):
        super().__init__(port_label=port_label, port_type=NodePort.PORT_TYPE_EXEC_IN)

    def paint(self, painter: QPainter, option, widget) -> None:
        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(0, 0.2 * self._port_icon_size))
        poly.append(QPointF(0.25 * self._port_icon_size, 0.2 * self._port_icon_size))
        poly.append(QPointF(0.5 * self._port_icon_size, 0.5 * self._port_icon_size))
        poly.append(QPointF(0.25 * self._port_icon_size, 0.8 * self._port_icon_size))
        poly.append(QPointF(0, 0.8 * self._port_icon_size))
        port_outline.addPolygon(poly)

        if not self.is_connected():
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(port_outline.simplified())
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._brush_default)
            painter.drawPath(port_outline.simplified())

        # port label
        painter.setPen(self._pen_default)
        painter.setFont(self._port_font)
        painter.drawText(
            QRectF(0.8 * self._port_icon_size, 0, self._port_label_size, self._port_icon_size),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._port_label)


class EXECOutPort(EXECPort):
    def __init__(self, port_label=''):
        super().__init__(port_label=port_label, port_type=NodePort.PORT_TYPE_EXEC_OUT)

    def paint(self, painter: QPainter, option, widget) -> None:
        # paint label
        painter.setPen(self._pen_default)
        painter.setFont(self._port_font)
        painter.drawText(
            QRectF(0, 0, self._port_label_size, self._port_icon_size),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._port_label)

        # paint icon
        port_outline = QPainterPath()
        poly = QPolygonF()
        poly.append(QPointF(self._port_label_size + 0.5 * self._port_icon_size + 0, 0.2 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.5 * self._port_icon_size + 0.25 * self._port_icon_size,
                            0.2 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.5 * self._port_icon_size + 0.5 * self._port_icon_size,
                            0.5 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.5 * self._port_icon_size + 0.25 * self._port_icon_size,
                            0.8 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.5 * self._port_icon_size + 0, 0.8 * self._port_icon_size))
        port_outline.addPolygon(poly)

        if not self.is_connected():
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(port_outline.simplified())
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._brush_default)
            painter.drawPath(port_outline.simplified())

    def get_port_pos(self) -> QPointF:
        # 获得本身在scene的位置
        self._port_pos = self.scenePos()
        return QPointF(
            self._port_pos.x() + self._port_label_size + 0.75 * self._port_icon_size,
            self._port_pos.y() + 0.5 * self._port_icon_size)


class ParamPort(NodePort):
    def __init__(self, port_label='', port_class='str', port_color='#ffffff', default_widget=None, parent=None):
        super().__init__(port_label, port_class, port_color, NodePort.PORT_TYPE_PARAM,
                         default_widget=default_widget, parent=parent)
        self.setupWidget()

    def get_port_pos(self) -> QPointF:
        # 获得本身在scene的位置
        self._port_pos = self.scenePos()
        return QPointF(self._port_pos.x() + 0.25 * self._port_icon_size,
                       self._port_pos.y() + 0.5 * self._port_icon_size)

    def paint(self, painter: QPainter, option, widget) -> None:
        # icon o> 表示

        if not self.is_connected():
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(0.25 * self._port_icon_size, 0.5 * self._port_icon_size),
                                0.25 * self._port_icon_size, 0.25 * self._port_icon_size)
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._brush_default)
            painter.drawEllipse(QPointF(0.25 * self._port_icon_size, 0.5 * self._port_icon_size),
                                0.25 * self._port_icon_size, 0.25 * self._port_icon_size)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_default)
        poly = QPolygonF()
        poly.append(QPointF(0.6 * self._port_icon_size, 0.35 * self._port_icon_size))
        poly.append(QPointF(0.7 * self._port_icon_size, 0.50 * self._port_icon_size))
        poly.append(QPointF(0.6 * self._port_icon_size, 0.65 * self._port_icon_size))
        painter.drawPolygon(poly)

        # port label
        painter.setPen(self._pen_default)
        painter.setFont(self._port_font)
        painter.drawText(
            QRectF(self._port_icon_size, 0, self._port_label_size, self._port_icon_size),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._port_label)

    def setupWidget(self):
        # 画widget
        if self._default_widget is not None:
            proxy = QGraphicsProxyWidget(parent=self)
            proxy.setWidget(self._default_widget)
            proxy.setPos(self._port_icon_size + self._port_label_size, 0)


class OutputPort(NodePort):
    def __init__(self, port_label='', port_class='str', port_color='#ffffff', parent=None):
        super().__init__(port_label, port_class, port_color, NodePort.PORT_TYPE_OUTPUT, parent)

    def get_port_pos(self) -> QPointF:
        self._port_pos = self.scenePos()
        return QPointF(self._port_pos.x() + self._port_label_size + 0.5 * self._port_icon_size,
                       self._port_pos.y() + 0.5 * self._port_icon_size)

    def paint(self, painter: QPainter, option, widget) -> None:
        # paint label
        painter.setPen(self._pen_default)
        painter.setFont(self._port_font)
        painter.drawText(
            QRectF(0, 0, self._port_label_size, self._port_icon_size),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._port_label)

        # icon o> 表示
        if not self.is_connected():
            painter.setPen(self._pen_default)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(self._port_label_size + 0.5 * self._port_icon_size,
                                        0.5 * self._port_icon_size), 0.25 * self._port_icon_size,
                                0.25 * self._port_icon_size)
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self._brush_default)
            painter.drawEllipse(QPointF(self._port_label_size + 0.5 * self._port_icon_size,
                                        0.5 * self._port_icon_size), 0.25 * self._port_icon_size,
                                0.25 * self._port_icon_size)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_default)
        poly = QPolygonF()
        poly.append(QPointF(self._port_label_size + 0.85 * self._port_icon_size, 0.35 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.95 * self._port_icon_size, 0.50 * self._port_icon_size))
        poly.append(QPointF(self._port_label_size + 0.85 * self._port_icon_size, 0.65 * self._port_icon_size))
        painter.drawPolygon(poly)


class Pin:
    def __init__(self, pin_name='', pin_class='', pin_type='data', use_default_widget=True, pin_widget=None):
        self._pin_name = pin_name
        self._pin_type = pin_type
        self._pin_class = pin_class
        if self._pin_type == 'data':
            # 获取默认的color和widget
            self._pin_color = dtype.color_map[self._pin_class]
            if use_default_widget:
                self._pin_widget = dtype.default_widget[self._pin_class]
            else:
                self._pin_widget = pin_widget

        self.current_session = -1
        self.has_set_value = False

        # init value, 初始化为None或相应class的默认值
        # TODO(housian) 以后要创建一个字典
        self.value = None

        # 不能在这里进行初始化，这里的变量在register都会被调用，会出现在application之前初始化widget的错误
        # 实际的初始化变量在双击鼠标时调用node（）进行初始化
        # self.init_port()

    def getValue(self):
        return self.value

    @abstractmethod
    def init_port(self):
        pass

    def setSession(self, session):
        self.current_session = session
        self.has_set_value = False

    def setValue(self, value):
        self.value = value
        self.has_set_value = True


class NodeInput(Pin):
    def init_port(self):
        if self._pin_type == 'data':
            self.port = ParamPort(port_label=self._pin_name, port_class=self._pin_class, port_color=self._pin_color,
                                  default_widget=self._pin_widget)
        elif self._pin_type == 'exec':
            self.port = EXECInPort(port_label=self._pin_name)
        else:
            self.port = None
            print("No such kinds of pin type")
        return self.port


class NodeOutput(Pin):
    def init_port(self):
        if self._pin_type == 'data':
            self.port = OutputPort(port_label=self._pin_name, port_class=self._pin_class, port_color=self._pin_color)
        elif self._pin_type == 'exec':
            self.port = EXECOutPort(port_label=self._pin_name)
        else:
            self.port = None
            print("No such kinds of pin type")
        return self.port
