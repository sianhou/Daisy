from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout

from core.scene import EditorScene
from core.view import EditorView
from dlpkg.op import Linear
from dlpkg.opscan import OpListHandle


class NodeEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        OpListHandle.scan()
        self.setup()

    def setup(self):
        self.setGeometry(100, 100, 2000, 1200)
        self.setWindowTitle("Daisy - a simple node editor")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._view = EditorView()
        self._scene = EditorScene()
        self._view.setScene(self._scene)
        self._scene.setView(self._view)
        self._view.setupMouseRightBtnWidget()
        self._view.addDebugBtn()
        self.layout.addWidget(self._view)

        self.show()

        # self.addDebugNode()

    def addDebugNode(self):
        # node0 = MiniNode()
        # node0.setTitle("Test node0")
        #
        # input0 = InputPort()
        # input1 = InputPort()
        # input2 = InputPort()
        # node0.addInputPortList([input0, input1, input2])
        #
        # output0 = OutputPort()
        # output1 = OutputPort()
        # output2 = OutputPort()
        # output3 = OutputPort()
        # node0.addOutputPortList([output0, output1, output2, output3])
        #
        # node1 = MiniNode()
        # node1.setTitle("Test node1")
        #
        # input0 = InputPort()
        # input1 = InputPort()
        # input2 = InputPort()
        # node1.addInputPortList([input0, input1, input2])
        #
        # output0 = OutputPort()
        # output1 = OutputPort()
        # output2 = OutputPort()
        # output3 = OutputPort()
        # node1.addOutputPortList([output0, output1, output2, output3])
        node0 = Linear()
        node1 = Linear()
        self._view.addNode(node0)
        self._view.addNode(node1, pos=[200, 200])
        # self._view.addEdge(node0._output_ports[0], node1._input_ports[0])
