from PySide6.QtGui import Qt, QPainter
from PySide6.QtWidgets import QGraphicsView

from base.edge import PortEdge
# from base.edge import EdgeBase, DraggingEdge
from base.node import NodeBase
from base.port import PortBase, InputPort, OutputPort


class EditorView(QGraphicsView):
    def __init__(self, parent=None):
        super(EditorView, self).__init__(parent)
        self._scene = None
        self._edges = []
        self._dragging_edge = None
        self._dragging_edge_mode = False

        # config display params
        self.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # 不显示垂直和横向滚轮
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def addEdge(self, source_port: InputPort, target_port: OutputPort):
        # edge = EdgeBase(source_pos=source_port.getCenterPos(), target_pos=target_port.getCenterPos(),
        #                 color=source_port._port_color, scene=self._scene)
        edge = PortEdge(source_port=source_port, target_port=target_port, scene=self._scene)
        # edge = EdgeBase(source_port, target_port, scene=self._scene)
        self._edges.append(edge)
        pass

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

    def createDraggingEdge(self, port: PortBase):
        if isinstance(port, InputPort):
            drag_from_source = True
        elif isinstance(port, OutputPort):
            drag_from_source = False

        if self._dragging_edge is None:
            pass
            # self._dragging_edge = DraggingEdge(port)

        pass

    def prsMouseLeftBtn(self, event):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)
        if isinstance(item, PortBase):
            print(item)
            self._dragging_edge_mode = True
            self.createDraggingEdge(item)
        else:
            super().mousePressEvent(event)

    # override qt function
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.prsMouseLeftBtn(event)
        else:
            super().mousePressEvent(event)
