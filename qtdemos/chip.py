import sys

from PySide6.QtCore import QRectF, QRect, QLineF, QPoint, QSize
from PySide6.QtGui import Qt, QColor, QPainterPath, QBrush, QPen, QFont, QImage, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import QGraphicsScene, QSplitter, QHBoxLayout, QWidget, QGraphicsView, QApplication, \
    QGraphicsItem, QStyle, QFrame, QToolButton, QSlider, QGridLayout, QVBoxLayout


class Chip(QGraphicsItem):
    def __init__(self, color: QColor, x: int, y: int, parent=None):
        super(Chip, self).__init__(parent)

        self.x = x
        self.y = y
        self.color = color
        self.stuff = []
        
        self.setZValue((x + y) % 2)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(0, 0, 110, 70)

    def shape(self):
        path = QPainterPath()
        path.addRect(14, 14, 82, 42)
        return path

    def paint(self, painter, option, widget):
        fill_color = self.color.darker(150) if self.isSelected() else self.color
        if option.state & QStyle.State_MouseOver:
            fill_color = fill_color.lighter(125)

        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        if lod < 0.2:
            if lod < 0.125:
                painter.fillRect(QRectF(0, 0, 110, 70), fill_color)
                return

            b = painter.brush()
            painter.setBrush(fill_color)
            painter.drawRect(13, 13, 97, 57)
            painter.setBrush(b)
            return

        old_pen = painter.pen()
        pen = old_pen
        width = int(0)
        if option.state & QStyle.State_Selected:
            width += 2
        pen.setWidth(width)
        b = painter.brush()
        painter.setBrush(QBrush(fill_color.darker(120 if option.state & QStyle.State_Sunken else 100)))
        painter.drawRect(QRect(14, 14, 79, 39))
        painter.setBrush(b)

        if lod >= 1:
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawLine(15, 54, 94, 54)
            painter.drawLine(94, 53, 94, 15)
            painter.setPen(QPen(Qt.black, 0))

        if lod >= 2:
            font = QFont("Times", 10)
            font.setStyleStrategy(QFont.ForceOutline)
            painter.setFont(font)
            painter.save()
            painter.scale(0.1, 0.1)
            painter.drawText(170, 180, f"Model: VSC-2000 (Very Small Chip) at {self.x}x{self.y}")
            painter.drawText(170, 200, "Serial number: DLWR-WEER-123L-ZZ33-SDSJ")
            painter.drawText(170, 220, "Manufacturer: Chip Manufacturer")
            painter.restore()

        # draw lines
        lines = []
        if lod >= 0.5:
            inc = 1 if lod > 0.5 else 2
            for i in range(0, 11, inc):
                lines.append(QLineF(18 + 7 * i, 13, 18 + 7 * i, 5))
                lines.append(QLineF(18 + 7 * i, 54, 18 + 7 * i, 62))
            for i in range(0, 7, inc):
                lines.append(QLineF(5, 18 + i * 5, 13, 18 + i * 5))
                lines.append(QLineF(94, 18 + i * 5, 102, 18 + i * 5))

        if lod >= 0.4:
            lines.extend([QLineF(25, 35, 35, 35),
                          QLineF(35, 30, 35, 40),
                          QLineF(35, 30, 45, 35),
                          QLineF(35, 40, 45, 35),
                          QLineF(45, 30, 45, 40),
                          QLineF(45, 35, 55, 35)])

        painter.drawLines(lines)

        # draw red ink
        if len(self.stuff) > 1:
            p = painter.pen()
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            path = QPainterPath()
            path.moveTo(self.stuff[0])
            for _, p in enumerate(self.stuff[1:]):
                path.lineTo(p)
            painter.drawPath(path)
            painter.setPen(p)


class View(QFrame):
    def __init__(self, name="", parent=None):
        super(View, self).__init__(parent)

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.view = QGraphicsView(self)
        self.view.setRenderHint(QPainter.Antialiasing, False)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.view.setOptimizationFlag(QGraphicsView.DontSavePainterState)
        self.view.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        size = self.style().pixelMetric(QStyle.PM_ToolBarIconSize)
        icon_size = QSize(size, size)

        self.zoom_in_icon = QToolButton()
        self.zoom_in_icon.setAutoRepeat(True)
        self.zoom_in_icon.setAutoRepeatInterval(33)
        self.zoom_in_icon.setAutoRepeatDelay(0)
        self.zoom_in_icon.setIcon(QPixmap("./zoomin.png"))
        self.zoom_in_icon.setIconSize(icon_size)

        self.zoom_out_icon = QToolButton()
        self.zoom_out_icon.setAutoRepeat(True)
        self.zoom_out_icon.setAutoRepeatInterval(33)
        self.zoom_out_icon.setAutoRepeatDelay(0)
        self.zoom_out_icon.setIcon(QPixmap("./zoomout.png"))
        self.zoom_out_icon.setIconSize(icon_size)

        self.zoom_slider = QSlider()
        self.zoom_slider.setMinimum(0)
        self.zoom_slider.setMaximum(500)
        self.zoom_slider.setValue(250)
        self.zoom_slider.setTickPosition(QSlider.TicksRight)

        self.zoom_slider_layout = QVBoxLayout()
        self.zoom_slider_layout.addWidget(self.zoom_in_icon)
        self.zoom_slider_layout.addWidget(self.zoom_slider)
        self.zoom_slider_layout.addWidget(self.zoom_out_icon)

        self.rotate_left_icon = QToolButton()
        self.rotate_left_icon.setIcon(QPixmap("./rotateleft.png"))
        self.rotate_left_icon.setIconSize(icon_size)
        self.rotate_right_icon = QToolButton()
        self.rotate_right_icon.setIcon(QPixmap("./rotateright.png"))
        self.rotate_right_icon.setIconSize(icon_size)
        self.rotate_slider = QSlider()
        self.rotate_slider.setOrientation(Qt.Horizontal)
        self.rotate_slider.setMinimum(-360)
        self.rotate_slider.setMaximum(360)
        self.rotate_slider.setValue(0)
        self.rotate_slider.setTickPosition(QSlider.TicksBelow)

        self.rotate_slider_layout = QHBoxLayout()
        self.rotate_slider_layout.addWidget(self.rotate_left_icon)
        self.rotate_slider_layout.addWidget(self.rotate_slider)
        self.rotate_slider_layout.addWidget(self.rotate_right_icon)

        self.top_layout = QGridLayout()
        self.top_layout.addWidget(self.view, 1, 0)
        self.top_layout.addLayout(self.zoom_slider_layout, 1, 1)
        self.top_layout.addLayout(self.rotate_slider_layout, 2, 0)
        self.setLayout(self.top_layout)

        self.zoom_slider.valueChanged.connect(self.setupMatrix)
        self.zoom_in_icon.clicked.connect(self.zoomIn)
        self.zoom_out_icon.clicked.connect(self.zoomOut)

        self.rotate_slider.valueChanged.connect(self.setupMatrix)
        self.rotate_left_icon.clicked.connect(self.rotateLeft)
        self.rotate_right_icon.clicked.connect(self.rotateRight)

    def zoomIn(self):
        self.zoom_slider.setValue(self.zoom_slider.value() + 1)

    def zoomOut(self):
        self.zoom_slider.setValue(self.zoom_slider.value() - 1)

    def zoomInBy(self, level):
        self.zoom_slider.setValue(self.zoom_slider.value() + level)

    def zoomOutBy(self, level):
        self.zoom_slider.setValue(self.zoom_slider.value() - level)

    def setResetButtonEnabled(self):
        self.resetButtonEnabled = True

    def setupMatrix(self):
        scale = pow(2.0, (self.zoom_slider.value() - 250) / 50)
        matrix = QTransform()
        matrix.scale(scale, scale)
        matrix.rotate(self.rotate_slider.value())

        self.view.setTransform(matrix)
        self.setResetButtonEnabled()

    def rotateLeft(self):
        self.rotate_slider.setValue(self.rotate_slider.value() - 10)

    def rotateRight(self):
        self.rotate_slider.setValue(self.rotate_slider.value() + 10)


class Demo(QWidget):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        self.scene = QGraphicsScene()

        self.populateScene()

        self.h1_splitter = QSplitter(Qt.Horizontal)
        self.h2_splitter = QSplitter(Qt.Horizontal)

        self.v_splitter = QSplitter()
        self.v_splitter.setOrientation(Qt.Vertical)
        self.v_splitter.addWidget(self.h1_splitter)
        self.v_splitter.addWidget(self.h2_splitter)

        self.view0 = View("Top left view")
        self.view0.view.setScene(self.scene)
        self.h1_splitter.addWidget(self.view0)

        self.view1 = View("Top right view")
        self.view1.view.setScene(self.scene)
        self.h1_splitter.addWidget(self.view1)

        self.view2 = View("Bottom left view")
        self.view2.view.setScene(self.scene)
        self.h2_splitter.addWidget(self.view2)

        self.view3 = View("Bottom right view")
        self.view3.view.setScene(self.scene)
        self.h2_splitter.addWidget(self.view3)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.v_splitter)
        self.setLayout(self.layout)

        self.setWindowTitle("Chip Example")

    def populateScene(self):
        image = QImage("./qt4logo.png")
        xx = int(0)
        for i in range(-11000, 11000, 110):
            xx += 1
            yy = int(0)
            for j in range(-7000, 7000, 70):
                yy += 1
                x = float(i + 11000) / 22000.0
                y = float(j + 7000) / 14000.0

                color = QColor(image.pixel(int(image.width() * x), int(image.height() * y)))
                item = Chip(color, xx, yy)
                item.setPos(QPoint(i, j))
                self.scene.addItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec())
