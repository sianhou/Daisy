# coding:utf-8
'''
QGraphicsView class
'''
from PySide6.QtGui import QPainter, QMouseEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsItem
from PySide6.QtCore import Qt, QEvent

from vg_node import GraphNode


class VisualGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(VisualGraphicsView, self).__init__(parent)
        self._scene = scene
        self.setScene(self._scene)

        self.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 鼠标滑轮缩放比例
        self._zoom_clamp = [0.5, 5]
        self._zoom_factor = 1.05
        self._view_scale = 1.0
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # 画布拖动
        self._drag_mode = False

    def mousePressEvent(self, event):

        if event.button() == Qt.MiddleButton:
            self.middleButtonPressed(event)
        else:
            return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.reset_scale()
        else:
            return super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleButtonReleased(event)
        else:
            return super().mouseReleaseEvent(event)

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
        self.setDragMode(QGraphicsView.NoDrag)
        self._drag_mode = False
        # 创建左键松开事件
        release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), Qt.LeftButton, Qt.NoButton,
                                    event.modifiers())
        super().mouseReleaseEvent(release_event)

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

    def reset_scale(self):
        self.resetTransform()
        self._view_scale = 1.0

    def add_graph_node(self, node: GraphNode, pos=[0, 0]):
        self._scene.addItem(node)
        node.set_scene(self._scene)
        node.setPos(pos[0], pos[1])
