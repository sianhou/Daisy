from PySide6.QtGui import Qt, QPainter
from PySide6.QtWidgets import QGraphicsView

from base.edge import PortEdge, DragEdge
# from base.edge import EdgeBase, DraggingEdge
from base.node import NodeBase
from base.port import PortBase, InputPort, OutputPort


class EditorView(QGraphicsView):
    def __init__(self, parent=None):
        super(EditorView, self).__init__(parent)
        self._scene = None
        self._edges = []
        self._drag_edge = None
        self._drag_edge_mode = False

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

    def createDragEdge(self, port: PortBase):
        if isinstance(port, OutputPort):
            drag_from_outputport = True
        elif isinstance(port, InputPort):
            drag_from_outputport = False

        print(f'drag_from_outputport = {drag_from_outputport}')

        if self._drag_edge is None:
            self._drag_edge = DragEdge(source_pos=port.getCenterPos(), color=port._port_color, scene=self._scene,
                                       drag_from_outputport=drag_from_outputport)
            if drag_from_outputport:
                self._drag_edge.setSourcePort(source_port=port)
            else:
                self._drag_edge.setTargetPort(target_port=port)

        print(self._drag_edge)

    def prsMouseLeftBtn(self, event):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)
        if isinstance(item, PortBase):
            print(item)
            self._drag_edge_mode = True
            self.createDragEdge(item)
        else:
            super().mousePressEvent(event)

    # override qt function
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.prsMouseLeftBtn(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_edge_mode:
            pos = self.mapToScene(event.pos())
            self._drag_edge.updatePos(pos=[pos.x(), pos.y()])
        else:
            super().mouseMoveEvent(event)
