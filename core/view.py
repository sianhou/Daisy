from PySide6.QtGui import Qt, QPainter
from PySide6.QtWidgets import QGraphicsView, QPushButton, QGraphicsProxyWidget

from core.edge import PortEdge, DragEdge
from core.node.dln import DLN
# from base.edge import EdgeBase, DraggingEdge
from core.node.node import NodeBase
from core.port.port import PortBase, InputPort, OutputPort
from core.widget import MouseRightBtnWidget
from dlpkg.opscan import OpListHandle


class EditorView(QGraphicsView):
    def __init__(self, parent=None):
        super(EditorView, self).__init__(parent)
        self._scene = None
        self._nodes = []
        self._edges = []
        self._drag_edge = None
        self._drag_edge_mode = False

        # config display params
        self.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # 不显示垂直和横向滚轮
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def addNodeWithClass(self, cls, pos):
        node = cls()
        self.addNode(node, pos)

    def removeEdge(self, edge: PortEdge):
        if edge in self._edges:
            self._edges.remove(edge)
            edge._source_port._edges.remove(edge)
            edge._target_port._edges.remove(edge)

    def addEdge(self, source_port: OutputPort, target_port: InputPort):
        edge = PortEdge(source_port=source_port, target_port=target_port, scene=self._scene)
        self._edges.append(edge)

    def addPortEdge(self, edge: PortEdge):

        self._edges.append(edge)

    def addNode(self, node: NodeBase = None, pos=(0, 0)):
        if node is not None:
            self._scene.addItem(node)
            self._nodes.append(node)
            node.setPos(pos[0], pos[1])
            node.setScene(self._scene)

    def setScene(self, scene):
        self._scene = scene
        super().setScene(scene)
        self.update()

    def createDragEdge(self, port: PortBase):
        drag_from_outputport = True
        if isinstance(port, OutputPort):
            drag_from_outputport = True
        elif isinstance(port, InputPort):
            drag_from_outputport = False

        if self._drag_edge is None:
            self._drag_edge = DragEdge(source_pos=port.getCenterPos(), color=port._port_color, scene=self._scene,
                                       drag_from_outputport=drag_from_outputport)
            if drag_from_outputport:
                self._drag_edge.setSourcePort(source_port=port)
            else:
                self._drag_edge.setTargetPort(target_port=port)

    def pressMouseLeftBtn(self, event):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)

        # TODO(housian): 这里希望的作用是在用鼠标左键点击非右键菜单item时，右键自动隐藏
        # 但是目前的方案似乎有些问题，就是当有多个QGraphicsProxyWidget，依然会有问题
        # 未来是否可以用鼠标右键的点击位置进行判断，当鼠标不在NodeListWidget的范围内就进行隐藏
        if not isinstance(item, QGraphicsProxyWidget):
            self._mouse_right_btn_widget.hide()

        if item is None:
            if len(self._nodes) > 0:
                for node in self._nodes:
                    node._paramcard.hide()
        if isinstance(item, PortBase):
            self._drag_edge_mode = True
            self.createDragEdge(item)
        else:
            super().mousePressEvent(event)

    def pressMouseRightBtn(self, event):
        item = self.itemAt(event.pos())
        # 当前位置item为空
        if item is None:
            pos = self.mapToScene(event.pos())
            w, h = self._mouse_right_btn_widget.rect().width(), self._mouse_right_btn_widget.rect().height()
            self._mouse_right_btn_widget.setGeometry(pos.x(), pos.y(), w, h)
            self._mouse_right_btn_widget._pos = pos
            self._mouse_right_btn_widget.show()
        super().mousePressEvent(event)

    def releaseMouseLeftBtn(self, event):
        if self._drag_edge_mode:
            self._drag_edge_mode = False
            item = self.itemAt(event.pos())
            if isinstance(item, PortBase):
                if self._drag_edge._drag_from_outputport:
                    self._drag_edge.setTargetPort(item)
                else:
                    self._drag_edge.setSourcePort(item)
                edge = self._drag_edge.convToPortEdge()
                if edge is not None:
                    self.addPortEdge(edge)
            self._scene.removeItem(self._drag_edge)
            self._drag_edge = None
        else:
            super().mouseReleaseEvent(event)

    # override qt function
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressMouseLeftBtn(event)
        elif event.button() == Qt.RightButton:
            self.pressMouseRightBtn(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.releaseMouseLeftBtn(event)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_edge_mode:
            pos = self.mapToScene(event.pos())
            self._drag_edge.updatePos(pos=(pos.x(), pos.y()))
        else:
            super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_X:
            self.deleteSelectedItems()
        else:
            super().keyReleaseEvent(event)

    def deleteSelectedItems(self):
        # TODO(housian), 如果不在remove_self()后面增加item.update()，会在显示上残留最后一个node
        for item in self._scene.selectedItems():
            if isinstance(item, PortEdge):
                item.removeItself()
                item.update()
            elif isinstance(item, NodeBase):
                item.removeItself()
                item.update()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressMouseLeftBtnTwice(event)
        else:
            return super().mouseDoubleClickEvent(event)

    def pressMouseLeftBtnTwice(self, event):
        mouse_pos = event.pos()
        item = self.itemAt(mouse_pos)
        if isinstance(item, DLN):
            item._paramcard.show()
        else:
            super().mouseDoubleClickEvent(event)

    def setupMouseRightBtnWidget(self):
        data = OpListHandle.getRegisteredOpsJson()
        self._mouse_right_btn_widget = MouseRightBtnWidget(data=data, scene=self._scene, view=self)
        self._scene.addWidget(self._mouse_right_btn_widget)
        self._mouse_right_btn_widget.setGeometry(0, 0, 200, 300)
        self._mouse_right_btn_widget.hide()

    def addDebugBtn(self):
        self._debug_btn = QPushButton('Debug')
        self._debug_btn_proxy = QGraphicsProxyWidget()
        self._debug_btn_proxy.setWidget(self._debug_btn)
        self._scene.addItem(self._debug_btn_proxy)
        self._debug_btn_proxy.setPos(300, 300)

        self._debug_btn.clicked.connect(self.debugFunc)

    def debugFunc(self):
        for node in self._nodes:
            node.updateParams()

            print(f'debug: {node._unique_id}')

            for param in node._params:
                print(param._title, ' = ', param._value)
