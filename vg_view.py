# coding:utf-8
'''
QGraphicsView class
'''
from PySide6 import QtGui
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtWidgets import QGraphicsView

from vg_edge import NodeEdge, DraggingEdge, CuttingLine
from vg_node import GraphNode
from vg_node_port import NodePort


class VisualGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(VisualGraphicsView, self).__init__(parent)
        self._nodes = []
        self._edges = []

        self._scene = scene
        self.setScene(self._scene)
        self._scene.set_view(self)

        self.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 鼠标滑轮缩放比例
        self._zoom_clamp = [0.5, 5]
        self._zoom_factor = 1.05
        self._view_scale = 1.0
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # 框体选择
        self.setDragMode(QGraphicsView.RubberBandDrag)
        # 画布拖动
        self._drag_mode = False

        # 可拖动的边
        self._drag_edge = None
        self._drag_edge_mode = False

        # cutting line
        self._cutting_mode = False
        self._cutting_line = CuttingLine()
        self._scene.addItem(self._cutting_line)

    def add_graph_node(self, node: GraphNode, pos=[0, 0]):
        self._scene.addItem(node)
        node.set_scene(self._scene)
        node.setPos(pos[0], pos[1])
        self._nodes.append(node)

    def add_node_edge(self, source_node, target_node):
        edge = NodeEdge(source_node, target_node, scene=self._scene)
        self._edges.append(edge)

    def create_dragging_edge(self, port: NodePort):

        port_pos = port.get_port_pos()
        if port._port_type == NodePort.PORT_TYPE_EXEC_OUT or port._port_type == NodePort.PORT_TYPE_OUTPUT:
            drag_from_source = True
        else:
            drag_from_source = False

        if self._drag_edge is None:
            self._drag_edge = DraggingEdge(port_pos, port_pos, edge_color=port._port_color, scene=self._scene,
                                           drag_from_source=drag_from_source)
            self._drag_edge.set_first_port(port)
            self._scene.addItem(self._drag_edge)

    def delete_selected_items(self):
        # 获得当前选中的items
        for item in self._scene.selectedItems():
            if isinstance(item, GraphNode):
                item.remove_self()
            elif isinstance(item, NodeEdge):
                item.remove_self()

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_X:
            self.delete_selected_items()
        else:
            super().keyReleaseEvent(event)

    def leftButtonReleased(self, event: QMouseEvent):
        if self._drag_edge_mode:
            self._drag_edge_mode = False
            item = self.itemAt(event.pos())
            if isinstance(item, NodePort):
                # 创建一个NodeEdge
                self._drag_edge.set_second_port(item)
                edge = self._drag_edge.create_node_edge()
                if edge is not None:
                    self._edges.append(edge)
            # 删除 self._drag_edge
            self._scene.removeItem(self._drag_edge)
            self._drag_edge = None
        else:
            super().mouseReleaseEvent(event)

    def middleButtonPressed(self, event):
        if self.itemAt(event.pos()) is not None:
            return
        else:
            # 创建左键松开事件
            release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), Qt.LeftButton, Qt.NoButton,
                                        event.modifiers())
            super().mouseReleaseEvent(release_event)

            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._drag_mode = True
            # 创建左键点击事件
            click_event = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), Qt.LeftButton, Qt.NoButton,
                                      event.modifiers())
            super().mousePressEvent(click_event)

    def middleButtonReleased(self, event):
        # 创建左键松开事件
        release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), Qt.LeftButton, Qt.NoButton,
                                    event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self._drag_mode = False

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.reset_scale()
        else:
            return super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_edge_mode:
            self._drag_edge.update_position(self.mapToScene(event.pos()))
        else:
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.leftButtonPressed(event)
        elif event.button() == Qt.MiddleButton:
            self.middleButtonPressed(event)
        elif event.button() == Qt.RightButton:
            self.rightButtonPressed(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftButtonReleased(event)
        elif event.button() == Qt.MiddleButton:
            self.middleButtonReleased(event)
        elif event.button() == Qt.RightButton:
            self.rightButtonReleased(event)
        else:
            super().mouseReleaseEvent(event)

    def remove_node(self, node: GraphNode):
        if node in self._nodes:
            self._nodes.remove(node)

    def remove_edge(self, edge: NodeEdge):
        if edge in self._edges:
            self._edges.remove(edge)

    def reset_scale(self):
        self.resetTransform()
        self._view_scale = 1.0

    def leftButtonPressed(self, event: QMouseEvent):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)
        if isinstance(item, NodePort):
            # 设置drag edge mode
            self._drag_edge_mode = True
            self.create_dragging_edge(item)
        else:
            super().mousePressEvent(event)

    def rightButtonPressed(self, event):
        self.setDragMode(QGraphicsView.NoDrag)
        super().mousePressEvent(event)

    def rightButtonReleased(self, event):
        self.setDragMode(QGraphicsView.RubberBandDrag)
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        if not self._drag_mode:
            if event.angleDelta().y() > 0:
                zoom_factor = self._zoom_factor
            else:
                zoom_factor = 1.0 / self._zoom_factor

            self._view_scale *= zoom_factor
            print(self._view_scale)
            if self._view_scale < self._zoom_clamp[0] or self._view_scale > self._zoom_clamp[1]:
                zoom_factor = 1.0
                self._view_scale = self._last_scale

            self._last_scale = self._view_scale
            self.scale(self._view_scale, self._last_scale)
