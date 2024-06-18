from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGraphicsView


class EditorView(QGraphicsView):
    def __init__(self, parent=None):
        super(EditorView, self).__init__(parent)
        self._scene = None

        # 不显示垂直和横向滚轮
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setScene(self, scene):
        self._scene = scene
        super().setScene(scene)
        self.update()
