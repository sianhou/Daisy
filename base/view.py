from PySide6.QtGui import Qt, QPainter, QMouseEvent
from PySide6.QtWidgets import QGraphicsView

from base.edge import EdgeBase, DraggingEdge
from base.node import NodeBase
from base.port import PortBase, InputPort


class EditorView(QGraphicsView):
    def __init__(self, parent=None):
        super(EditorView, self).__init__(parent)
        self._scene = None
        self._edges = []
        self._dragging_edge_mode = False
        self._dragging_edge = None

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

    def pressMouseLeftButton(self, event: QMouseEvent):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)

        if isinstance(item, PortBase):
            # 设置drag edge mode
            self._dragging_edge_mode = True
            self.createDraggingEdge(item)
        else:
            super().mousePressEvent(event)

    def createDraggingEdge(self, port: PortBase):
        port_pos = port.getPos()
        if isinstance(port, InputPort):
            drag_from_source = True
        else:
            drag_from_source = False

        if self._dragging_edge is None:
            self._dragging_edge = DraggingEdge(port_pos, port_pos, edge_color=port._port_color, scene=self._scene,
                                               drag_from_source=drag_from_source)
            self._dragging_edge.setFirstPort(port)
            self._scene.addItem(self._dragging_edge)

    # override QT function
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressMouseLeftButton(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._dragging_edge_mode:
            pos = self.mapToScene(event.pos())
            self._dragging_edge.updatePos((pos.x(), pos.y()))
        # elif self._cutting_mode:
        # self._cutting_line.update_points(self.mapToScene(event.pos()))
        #    pass
        else:
            super().mouseMoveEvent(event)
