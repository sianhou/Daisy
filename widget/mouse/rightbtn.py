from PySide6.QtWidgets import QTreeWidget


class NodeListWidget(QTreeWidget):
    def __init__(self, data, scene, view, parent=None):
        super().__init__(parent)
        self._data = data
        self._view = view
        self._scene = scene

        self._pos = (0, 0)

        self.resize(200, 300)
        self.setColumnCount(1)
        self.setHeaderHidden(True)

    def hide(self):
        self.setVisible(False)
