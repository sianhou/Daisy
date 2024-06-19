from PySide6.QtGui import Qt, QPainter
from PySide6.QtWidgets import QGraphicsView

from base.edge import EdgeBase
from base.node import NodeBase


class EditorView(QGraphicsView):
    def __init__(self, parent=None):
        super(EditorView, self).__init__(parent)
        self._scene = None
        self._edges = []

        # config display params
        self.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # 不显示垂直和横向滚轮
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def addEdge(self, source_port, target_port):
        edge = EdgeBase(source_port, target_port, scene=self._scene)
        self._edges.append(edge)

    def addNode(self, node: NodeBase = None, pos=[0, 0]):
        if node is not None:
            self._scene.addItem(node)
            node.setPos(pos[0], pos[1])
            node.setScene(self._scene)

            # self._nodes.append(node)

    def setScene(self, scene):
        self._scene = scene
        super().setScene(scene)
        self.update()
