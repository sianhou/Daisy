from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class MouseRightBtnWidget(QTreeWidget):
    def __init__(self, data, scene, view, parent=None):
        super().__init__(parent)
        self._data = data
        self._view = view
        self._scene = scene

        self._pos = (0, 0)

        self.resize(200, 300)
        self.setColumnCount(1)
        self.setHeaderHidden(True)

        self.setup()

    def setup(self):
        self.clear()
        items = []
        for pkg_name in self._data.keys():
            print(pkg_name)
            item = QTreeWidgetItem([pkg_name])
            for node_name in self._data[pkg_name].keys():
                node_item = QTreeWidgetItem([node_name])
                # print(self._data[pkg_name][node_name])
                node_item.setData(0, Qt.UserRole, self._data[pkg_name][node_name])
                item.addChild(node_item)
            items.append(item)

        self.insertTopLevelItems(0, items)

    def hide(self):
        self.setVisible(False)

    def show(self):
        self.setVisible(True)
