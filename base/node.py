from abc import abstractmethod

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsItem

from base.port import InputPort, OutputPort
from env.config import EditorSceneConfig


class NodeBase(QGraphicsItem):
    def __init__(self, parent=None):
        super(NodeBase, self).__init__(parent)

        self.setFlags(
            QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemSendsGeometryChanges)

        self._port_space = 15
        self._scene = None
        self._input_ports: [InputPort] = []
        self._output_ports: [OutputPort] = []

    @abstractmethod
    def addInputPort(self, port: InputPort, pos=[0, 0]):
        pass

    @abstractmethod
    def addInputPortList(self, port_list: [InputPort] = None):
        pass

    @abstractmethod
    def addOutputPort(self, port: OutputPort, pos=[0, 0]):
        pass

    @abstractmethod
    def addOutputPortList(self, port_list: [OutputPort] = None):
        pass

    @abstractmethod
    def getPos(self):
        pass

    @abstractmethod
    def getShape(self):
        pass

    def snapToNearestGrid(self):
        x, y = self.x(), self.y()
        x = round(x / EditorSceneConfig.grid_size) * EditorSceneConfig.grid_size
        y = round(y / EditorSceneConfig.grid_size) * EditorSceneConfig.grid_size
        self.setPos(QPointF(x, y))

    def setScene(self, scene):
        self._scene = scene

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.snapToNearestGrid()
        return super().itemChange(change, value)
