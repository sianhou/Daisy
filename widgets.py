from PySide6.QtGui import Qt, QCursor
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import QEvent, QPointF


class NodeListWidget(QTreeWidget):
    def __init__(self, data, scene, view, parent=None):
        super().__init__(parent)

        self._data = data
        self._view = view
        self._scene = scene

        self._pos = QPointF(0, 0)

        self.resize(200, 300)
        self.setColumnCount(1)
        self.setHeaderHidden(True)

        self.setupTree()

        self.itemDoubleClicked.connect(self.clickTreeItemTwice)

    def setupTree(self, filter=None):
        self.clear()
        items = []
        for pkg_name in self._data.keys():
            item = QTreeWidgetItem([pkg_name])
            for node_name in self._data[pkg_name].keys():
                node_item = QTreeWidgetItem([node_name])
                # print(self._data[pkg_name][node_name])
                node_item.setData(0, Qt.UserRole, self._data[pkg_name][node_name])
                item.addChild(node_item)
            items.append(item)

        self.insertTopLevelItems(0, items)

    # node_selected in vg_view
    def clickTreeItemTwice(self, item, column):
        if isinstance(item, QTreeWidgetItem):
            cls = item.data(column, Qt.UserRole)
            if cls is not None:
                self._view.addGraphNode(cls, self._pos)
                self.hide()
                # print(item.data(0, Qt.UserRole))

    def hide(self):
        self.setVisible(False)
