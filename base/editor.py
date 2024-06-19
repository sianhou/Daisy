from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout

from base.node import DeepNetworkNode
from base.scene import EditorScene
from base.view import EditorView


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup()

    def setup(self):
        self.setGeometry(100, 100, 1440, 720)
        self.setWindowTitle("Daisy - a simple node editor")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._view = EditorView()
        self._scene = EditorScene()
        self._view.setScene(self._scene)
        self._scene.setView(self._view)
        self.layout.addWidget(self._view)

        self.show()

        self.addDebugNode()

    def addDebugNode(self):
        node = DeepNetworkNode()
        node.setTitle("Test title")
        self._view.addNode(node)
