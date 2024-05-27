# coding:utf-8
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

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

        self.show()

    def debug_add_node(self, pos=[0, 0]):

        params = []
        params.append(ParamPort('width', 'float', '#99ff22'))
        params.append(ParamPort('height', 'float', '#99ff22'))

        outputs = []
        outputs.append(OutputPort('area', 'float', '#99ff22'))

        # 创建一个port
        node = GraphNode(title="Area", param_ports=params, output_ports=outputs, is_pure=False)

        self.view.add_graph_node(node, pos)

        params2 = []
        params2.append(ParamPort('width', 'float', '#99ff22'))
        params2.append(ParamPort('height', 'float', '#99ff22'))

        outputs2 = []
        outputs2.append(OutputPort('area', 'float', '#99ff22'))

        # 创建一个port
        node2 = GraphNode(title="Area2", param_ports=params2, output_ports=outputs2, is_pure=False)

        self.view.add_graph_node(node2, [pos[0] + 200, pos[1] + 200])

        # self.view.add_node_edge(outputs[0], params2[0])

    def right_click_add_node(self, mouse_pos):
        self.debug_add_node([mouse_pos.x(), mouse_pos.y()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.right_click_add_node(self.view.mapToScene(event.pos()))
        else:
            super().mousePressEvent(event)
