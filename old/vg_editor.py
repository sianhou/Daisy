# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout

from env import Env
from node.port import ParamPort, OutputPort
from vg_node import GraphNode
from vg_scene import VisualGraphScene
from vg_view import VisualGraphicsView


class VisualGraphEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        Env.registerNode()
        self.setup_editor()

    def debug_add_custom_node(self, pos):
        # node = BranchNode()
        node = Env.getRegisteredNode()[0]()
        self.view.addNode(node, [pos[0], pos[1]])

        node = Env.getRegisteredNode()[1]()
        self.view.addNode(node, [pos[0] + 100, pos[1] + 100])

    def debug_add_node(self, pos=[0, 0]):

        params = []
        params.append(ParamPort('width', 'float', '#99ff22'))
        params.append(ParamPort('height', 'float', '#99ff22'))
        params.append(ParamPort('count', 'int', '#00ffee'))

        outputs = []
        outputs.append(OutputPort('area', 'float', '#99ff22'))
        outputs.append(OutputPort('num', 'int', '#00ffee'))

        # 创建一个port
        node2 = GraphNode(title="Area", param_ports=params, output_ports=outputs, is_pure=False)

        self.view.addNode(node2, [pos[0], pos[1]])

        # self.view.add_node_edge(outputs[0], params2[0])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.right_click_add_node(self.view.mapToScene(event.pos()))
        else:
            super().mousePressEvent(event)

    def right_click_add_node(self, mouse_pos):
        # self.debug_add_node([mouse_pos.x(), mouse_pos.y()])
        self.debug_add_custom_node([mouse_pos.x(), mouse_pos.y()])

    def setup_editor(self):
        self.setGeometry(100, 100, 1440, 720)
        self.setWindowTitle("Visual Graph Editor")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 初始化scene
        self._scene = VisualGraphScene()
        self.view = VisualGraphicsView(self._scene, self)
        self.layout.addWidget(self.view)

        self.show()
