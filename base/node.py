from abc import abstractmethod

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

    def setScene(self, scene):
        self._scene = scene

    def snapToNearestGrid(self, pos=(0, 0)):
        (x, y) = pos
        x = round(x / EditorSceneConfig.grid_size) * EditorSceneConfig.grid_size
        y = round(y / EditorSceneConfig.grid_size) * EditorSceneConfig.grid_size
        return (x, y)

    def updateInputEdge(self):
        if len(self._input_ports) > 0:
            for input_port in self._input_ports:
                if len(input_port._edges) > 0:
                    for edge in input_port._edges:
                        edge.update()

    def updateOutputEdge(self):
        if len(self._output_ports) > 0:
            for output_port in self._output_ports:
                if len(output_port._edges) > 0:
                    for edge in output_port._edges:
                        edge.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            x, y = value.x(), value.y()
            (x, y) = self.snapToNearestGrid(pos=(value.x(), value.y()))
            self.setPos(x, y)

            # update edge in inputports
            self.updateInputEdge()

            # update edge in outputports
            self.updateOutputEdge()

        return super().itemChange(change, value)
