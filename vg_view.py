# coding:utf-8
'''
QGraphicsView class
'''

from PySide6 import QtGui
from PySide6.QtCore import QEvent
from PySide6.QtGui import QPainter, QMouseEvent, Qt
from PySide6.QtWidgets import QApplication, QGraphicsProxyWidget
from PySide6.QtWidgets import QGraphicsView

from MouseBtnWidget import NodeListWidget
from env import Env
from node.op.control import BeginNode
from node.port import NodePort
from vg_edge import NodeEdge, DraggingEdge, CuttingLine
from vg_node import GraphNode


class VisualGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(VisualGraphicsView, self).__init__(parent)
        self._nodes = []
        self._edges = []
        self._begin_node = None
        self._has_begin_node = False

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

        # Node List Widget
        self.setupNodeListWidget()

    def addNode(self, node: GraphNode, pos=[0, 0]):

        if isinstance(node, BeginNode):
            if self._has_begin_node:
                # TODO(housian): using logging
                print('View -- Add Graph Debug: BeginNode already exists.')
                return
            else:
                self._begin_node = node
                self._has_begin_node = True

        self._scene.addItem(node)
        node.set_scene(self._scene)
        node.setPos(pos[0], pos[1])
        self._nodes.append(node)

    def addNodeWithClass(self, cls, pos):
        node = cls()
        self.addNode(node, pos)
        # self._scene.addItem(node)
        # node.set_scene(self._scene)
        # node.setPos(pos.x(), pos.y())
        # self._nodes.append(node)

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
        # TODO(housian), 如果不在remove_self()后面增加item.update()，会在显示上残留最后一个node
        for item in self._scene.selectedItems():
            if isinstance(item, GraphNode):
                if isinstance(item, BeginNode):
                    self._has_begin_node = False
                    self._begin_node = None
                item.remove_self()
                item.update()
            elif isinstance(item, NodeEdge):
                item.remove_self()
                item.update()

    def hideNodeListWidget(self):
        self._node_list_widget.setVisible(False)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_X:
            self.delete_selected_items()
        elif event.key() == Qt.Key_R and event.modifiers() == Qt.ControlModifier:
            self.runGraph()

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
        elif self._cutting_mode:
            self._cutting_line.update_points(self.mapToScene(event.pos()))
        else:
            super().mouseMoveEvent(event)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.pressMouseLeftButton(event)
        elif event.button() == Qt.MiddleButton:
            self.middleButtonPressed(event)
        elif event.button() == Qt.RightButton:
            self.pressMouseRightButton(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftButtonReleased(event)
        elif event.button() == Qt.MiddleButton:
            self.middleButtonReleased(event)
        elif event.button() == Qt.RightButton:
            self.releaseMouseRightButton(event)
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

    def pressMouseLeftButton(self, event: QMouseEvent):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)

        # TODO(housian): 这里希望的作用是在用鼠标左键点击非右键菜单item时，右键自动隐藏
        # 但是目前的方案似乎有些问题，就是当有多个QGraphicsProxyWidget，依然会有问题
        # 未来是否可以用鼠标右键的点击位置进行判断，当鼠标不在NodeListWidget的范围内就进行隐藏
        if not isinstance(item, QGraphicsProxyWidget):
            self.hideNodeListWidget()

        if isinstance(item, NodePort):
            # 设置drag edge mode
            self._drag_edge_mode = True
            self.create_dragging_edge(item)

        # elif item is None:
        #     self.hideNodeListWidget()
        #     super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def pressMouseRightButton(self, event):

        item = self.itemAt(event.pos())

        # 当前位置item为空
        if item is None:
            # 并且按住了键盘的ctrl键
            if (event.modifiers() == Qt.ControlModifier):
                self._cutting_mode = True
                # 此处setOverrideCursor是强制设置鼠标为某种模式，用于表示特定的信息
                # 直到下一次设置setOverrideCursor或restoreOverrideCursor为止
                QApplication.setOverrideCursor(Qt.CrossCursor)
            else:
                # 右键显示self._node_list_widget
                self.showNodeListWidget(self.mapToScene(event.pos()))
        else:
            self.setDragMode(QGraphicsView.NoDrag)
        super().mousePressEvent(event)

    def releaseMouseRightButton(self, event):
        # 获得和cuttingline相交的边并删除
        self._cutting_line.remove_intersect_edges(self._edges)

        # clean cutting line
        self._cutting_mode = False
        self._cutting_line._line_points = []
        self._cutting_line.update()
        QApplication.restoreOverrideCursor()

        self.setDragMode(QGraphicsView.RubberBandDrag)
        super().mousePressEvent(event)

    def setupNodeListWidget(self):
        # 获取data
        data = Env.getNodeListJson()
        self._node_list_widget = NodeListWidget(data, self._scene, self)
        self._scene.addWidget(self._node_list_widget)
        self._node_list_widget.setGeometry(0, 0, 200, 300)
        self.hideNodeListWidget()

    def showNodeListWidget(self, pos):
        self._node_list_widget.setGeometry(pos.x(), pos.y(), 200, 300)
        self._node_list_widget._pos = pos
        self._node_list_widget.show()

    def wheelEvent(self, event):
        if not self._drag_mode:
            if event.angleDelta().y() > 0:
                zoom_factor = self._zoom_factor
            else:
                zoom_factor = 1.0 / self._zoom_factor

            self._view_scale *= zoom_factor
            if self._view_scale < self._zoom_clamp[0] or self._view_scale > self._zoom_clamp[1]:
                zoom_factor = 1.0
                self._view_scale = self._last_scale

            self._last_scale = self._view_scale
            self.scale(self._view_scale, self._last_scale)

    def runGraph(self):
        # TODO(housian): using pythong.logging in the future
        print("============== run graph  ==============")

        # step1 在node里面找到beginnode
        # 如果没有begin node，提示添加begin node
        if not self._has_begin_node:
            print('View -- Graph needs a begin nodes.')
            return

        # step2 找到begin node，并开始执行
        self._begin_node.run()
