import math

from PySide6.QtCore import QLine
from PySide6.QtGui import QBrush, QColor, QPen, QPainter
from PySide6.QtWidgets import QGraphicsScene

from env import config


class EditorScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initScene()

    def calGridLines(self, rect):
        lines = []
        dark_lines = []

        left, right, top, bottom = math.floor(rect.left()), math.floor(rect.right()), math.floor(
            rect.top()), math.floor(rect.bottom())

        first_left = left - (left % self._grid_size)
        first_top = top - (top % self._grid_size)

        # 画横线
        for v in range(first_top, bottom, self._grid_size):
            line = QLine(left, v, right, v)
            if v % (self._grid_size * self._grid_size) == 0:
                dark_lines.append(line)
            else:
                lines.append(line)

        for h in range(first_left, right, self._grid_size):
            line = QLine(h, top, h, bottom)
            if h % (self._grid_size * self._grid_size) == 0:
                dark_lines.append(line)
            else:
                lines.append(line)

        return lines, dark_lines

    # override QT function
    def drawBackground(self, painter: QPainter, rect) -> None:

        super().drawBackground(painter, rect)

        lines, dark_lines = self.calGridLines(rect)

        # 画普通线
        painter.setPen(self._normal_line_pen)
        painter.drawLines(lines)

        # 画粗线
        painter.setPen(self._dark_line_pen)
        painter.drawLines(dark_lines)

    def initScene(self):
        # 初始化view
        self._view = None

        # initialize size
        self._width = config.EditorScene.width
        self._height = config.EditorScene.height
        self.setSceneRect(-self._width / 2, -self._height / 2, self._width, self._height)

        # initialize background brush
        self.setBackgroundBrush(QBrush(QColor(config.EditorScene.background_color)))

        # initialize grid
        self._grid_size = config.EditorScene.grid_size
        self._chunk_size = config.EditorScene.grid_chunk

        self._normal_line_pen = QPen(QColor(config.EditorScene.grid_normal_line_color))
        self._normal_line_pen.setWidthF(config.EditorScene.grid_normal_line_width)

        self._dark_line_pen = QPen(QColor(config.EditorScene.grid_dark_line_color))
        self._dark_line_pen.setWidthF(config.EditorScene.grid_dark_line_width)

    def setView(self, view):
        self._view = view
