from PySide6.QtCore import QPointF
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class MouseRightBtnWidget(QTreeWidget):
    def __init__(self, data, scene, view, parent=None):
        super().__init__(parent)
        self._data = data
        self._view = view
        self._scene = scene

        self._pos = QPointF(0, 0)

        self.resize(200, 300)
        self.setColumnCount(1)
        self.setHeaderHidden(True)

        self.setup()

        self.itemDoubleClicked.connect(self.clickTreeItemTwice)

    def setup(self):
        self.clear()
        items = []
        for pkg_name in self._data.keys():
            item = QTreeWidgetItem([pkg_name])
            for node_name in self._data[pkg_name].keys():
                node_item = QTreeWidgetItem([node_name])
                node_item.setData(0, Qt.UserRole, self._data[pkg_name][node_name])
                item.addChild(node_item)
            items.append(item)
        self.insertTopLevelItems(0, items)

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)

    def clickTreeItemTwice(self, item, column):
        print("clickTreeItemTwice")
        if isinstance(item, QTreeWidgetItem):
            print("QTreeWidgetItem")
            cls = item.data(column, Qt.UserRole)
            if cls is not None:
                self._view.addNodeWithClass(cls, [self._pos.x(), self._pos.y()])
                self.hide()
