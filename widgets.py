from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class NodeListWidget(QTreeWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        self._data = data

        self.resize(200, 300)
        self.setColumnCount(1)
        self.setHeaderHidden(True)

        self.setupTree()

    def setupTree(self, filter=None):
        self.clear()
        items = []
        for pkg_name in self._data.keys():
            item = QTreeWidgetItem([pkg_name])
            for node_name in self._data[pkg_name].keys():
                node_item = QTreeWidgetItem([node_name])
                item.addChild(node_item)
            items.append(item)

        self.insertTopLevelItems(0, items)
