# coding:utf-8

from PySide6.QtWidgets import QWidget, QVBoxLayout

from vg_node import GraphNode
from vg_view import VisualGraphicsView
from vg_scene import VisualGraphScene

from vg_node_port import EXECInPort, EXECOutPort, ParamPort, OutputPort


class VisualGraphEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()

    def setup_editor(self):
        self.setGeometry(100, 100, 1440, 720)
        self.setWindowTitle("Visual Graph Editor")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 初始化scene
        self.scene = VisualGraphScene()
        self.view = VisualGraphicsView(self.scene, self)
        self.layout.addWidget(self.view)

        self.debug_add_node()

        self.show()

    def debug_add_node(self):
        port = EXECInPort()
        port2 = EXECOutPort()
        port_param = ParamPort('width', 'float', '#99ff22')
        port_output = OutputPort('area', 'float', '#99ff22')

        # 创建一个port
        node = GraphNode(title="Area")
        node.add_port(port)
        node.add_port(port2)
        node.add_port(port_param)
        node.add_port(port_output)
        self.view.add_graph_node(node, [100, 100])
