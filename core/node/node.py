import uuid
from abc import abstractmethod

from PySide6.QtWidgets import QGraphicsItem

from core.port import InputPort, OutputPort
from env.config import EditorConfig


class NodeBase(QGraphicsItem):

    def __init__(self, parent=None):
        super(NodeBase, self).__init__(parent)

        self.setFlags(
            QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemSendsGeometryChanges)

        self._port_space = 15
        self._scene = None
        self._input_ports: [InputPort] = []
        self._output_ports: [OutputPort] = []

        self._node_width = 100
        self._node_height = 40
        self._node_radius = 7

        self._unique_id = uuid.uuid4()

    @abstractmethod
    def addInputPort(self, port: InputPort, pos=None):
        pass

    @abstractmethod
    def addInputPortList(self, port_list: [InputPort] = None):
        pass

    @abstractmethod
    def addOutputPort(self, port: OutputPort, pos=None):
        pass

    @abstractmethod
    def addOutputPortList(self, port_list: [OutputPort] = None):
        pass

    @abstractmethod
    def getPos(self):
        return self.x(), self.y()

    @abstractmethod
    def getShape(self):
        return self._node_width, self._node_height

    def getInputPort(self):
        return self._input_ports

    def getOutputPort(self):
        return self._output_ports

    def setScene(self, scene):
        self._scene = scene

    def snapToNearestGrid(self, pos=(0, 0)):
        (x, y) = pos
        x = round(x / EditorConfig.grid_size) * EditorConfig.grid_size
        y = round(y / EditorConfig.grid_size) * EditorConfig.grid_size
        return x, y

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

    def removeItself(self):
        # 删除所有的边
        for port in self._input_ports:
            for edge in port._edges:
                edge.removeItself()

        for port in self._output_ports:
            for edge in port._edges:
                edge.removeItself()

        self._scene._view._nodes.remove(self)
        self._scene.removeItem(self)
