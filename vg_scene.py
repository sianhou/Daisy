# coding:utf-8
import math

from PySide6.QtCore import QLine
from PySide6.QtGui import QBrush, QColor, QPen, QPainter
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

from vg_config import EditorConfig


class VisualGraphScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(VisualGraphScene, self).__init__(parent)

        self.setBackgroundBrush(QBrush(QColor(EditorConfig.editor_scene_background_color)))

        self._width = EditorConfig.editor_scene_width
        self._height = EditorConfig.editor_scene_height
        self.setSceneRect(-self._width / 2, -self._height / 2, self._width, self._height)

        # 画网格
        self._grid_size = EditorConfig.editor_scene_grid_size
        self._chunk_size = EditorConfig.editor_scene_grid_chunk

        self._normal_line_pen = QPen(QColor(EditorConfig.editor_scene_grid_normal_line_color))
        self._normal_line_pen.setWidthF(EditorConfig.editor_scene_grid_normal_line_width)

        self._dark_line_pen = QPen(QColor(EditorConfig.editor_scene_grid_dark_line_color))
        self._dark_line_pen.setWidthF(EditorConfig.editor_scene_grid_dark_line_width)

        self._view = None

    def cal_grid_lines(self, rect):
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

    def drawBackground(self, painter: QPainter, rect) -> None:

        super().drawBackground(painter, rect)

        lines, dark_lines = self.cal_grid_lines(rect)

        # 画普通线
        painter.setPen(self._normal_line_pen)
        painter.drawLines(lines)

        # 画粗线
        painter.setPen(self._dark_line_pen)
        painter.drawLines(dark_lines)

    def set_view(self, view: QGraphicsView) -> None:
        self._view = view
