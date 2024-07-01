from abc import abstractmethod

from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPen, QPainter, Qt, QPainterPath
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsDropShadowEffect, QGraphicsItem

from core.port.port import InputPort, OutputPort


class EdgeBase(QGraphicsPathItem):

    def __init__(self, source_pos=(0, 0), target_pos=(0, 0), color='#a1a1a1', scene=None, parent=None):
        super(EdgeBase, self).__init__(parent=parent)

        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self._scene = scene
        self._source_pos = source_pos
        self._target_pos = target_pos
        self._source_port = None
        self._target_port = None

        self._edge_color = QColor(color)
        self._default_pen = QPen(self._edge_color)
        self._default_pen.setWidthF(2)

        # 选中投影
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(20)
        self._shadow_color = Qt.yellow

        self.addToScene()

    def addToScene(self):
        self._scene.addItem(self)

    @abstractmethod
    def getSourcePos(self):
        return QPointF(self._source_pos[0], self._source_pos[1])

    @abstractmethod
    def getTargetPos(self):
        return QPointF(self._target_pos[0], self._target_pos[1])

    def setSourcePos(self, pos):
        self._source_pos = pos

    def setTargetPos(self, pos):
        self._target_pos = pos

    def updateVerticalEdgePath(self):
        source_pos = self.getSourcePos()
        target_pos = self.getTargetPos()

        path = QPainterPath(source_pos)

        y_height = source_pos.y() - target_pos.y()
        y_height = y_height + 0.01 if y_height == 0 else y_height
        x_width = abs(target_pos.x() - source_pos.x())

        tagnent = float(x_width) / y_height * 0.5
        tagnent *= y_height

        if y_height > 0:
            if y_height > 150:
                y_height = 150
            tagnent += y_height

        path.cubicTo(QPointF(source_pos.x(), source_pos.y() + tagnent),
                     QPointF(target_pos.x(), target_pos.y() - tagnent),
                     target_pos)

        self.setPath(path)

    # override qt function
    def paint(self, painter: QPainter, option, widget) -> None:
        self.updateVerticalEdgePath()

        painter.setPen(self._default_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

        if self.isSelected():
            self._shadow.setColor(self._shadow_color)
            self.setGraphicsEffect(self._shadow)
        else:
            self._shadow.setColor('#00000000')
            self.setGraphicsEffect(self._shadow)


class PortEdge(EdgeBase):
    def __init__(self, source_port: OutputPort, target_port: InputPort, scene=None, parent=None):
        super().__init__(source_pos=source_port.getCenterPos(), target_pos=target_port.getCenterPos(), scene=scene,
                         color=source_port._port_color, parent=parent)

        self._source_port: OutputPort = source_port
        self._target_port: InputPort = target_port

        self._source_port.addEdge(self)
        self._target_port.addEdge(self)

    def getSourcePos(self):
        (x, y) = self._source_port.getCenterPos()
        return QPointF(x, y)

    def getTargetPos(self):
        (x, y) = self._target_port.getCenterPos()
        return QPointF(x, y)

    def removeItself(self):
        if self in self._source_port._edges:
            self._source_port._edges.remove(self)
        if self in self._target_port._edges:
            self._target_port._edges.remove(self)
        self._source_port.update()
        self._target_port.update()
        if self in self._scene._edges:
            self._scene._edges.remove(self)
        if self.scene() == self._scene:
            self._scene.removeItem(self)


class DragEdge(EdgeBase):
    def __init__(self, source_pos, color='#a1a1a1', scene=None, drag_from_outputport=True, parent=None):
        super().__init__(source_pos=source_pos, target_pos=source_pos, color=color, scene=scene, parent=parent)

        self._drag_from_outputport = drag_from_outputport

    def setSourcePort(self, source_port: OutputPort = None):
        self._source_port = source_port

    def setTargetPort(self, target_port: InputPort = None):
        self._target_port = target_port

    def updatePos(self, pos=[0, 0]):
        if self._drag_from_outputport:
            self.setTargetPos(pos=pos)
        else:
            self.setSourcePos(pos=pos)
        self.update()

    def convToPortEdge(self):
        # 判断是否成对 1
        if not (isinstance(self._source_port, OutputPort) and isinstance(self._target_port, InputPort)):
            print("self._source_port & self._target_port dismatch")
            return None
        # 判断是否成对 2
        if not (self._source_port._port_dtype == self._target_port._port_dtype):
            print("self._source_port & self._target_port dismatch")
            return None
        # 判断是否是同一节点
        if self._source_port.getParentNode() == self._target_port.getParentNode():
            print('self._source_port.getParentNode() == self._target_port.getParentNode()')
            return None
        # 判断edge.target_port是否非空，如果非空，先删除
        if len(self._target_port._edges) > 0:
            for edge in self._target_port._edges.copy():
                edge.removeItself()
        edge = PortEdge(source_port=self._source_port, target_port=self._target_port, scene=self._scene)
        return edge

    def paint(self, painter: QPainter, option, widget) -> None:
        self.updateVerticalEdgePath()

        painter.setPen(self._default_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

        self._shadow.setColor(self._shadow_color)
        self.setGraphicsEffect(self._shadow)

    def __str__(self):
        return (f'DragEdge._source_port: {self._source_port} \n'
                f'DragEdge._target_port: {self._target_port} \n'
                f'DragEdge._source_pos: {self._source_pos} \n'
                f'DragEdge._target_pos: {self._target_pos}')
