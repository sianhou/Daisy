import sys

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QWidget, QApplication, QSlider, QToolButton, QHBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Ensure using PySide6 back-end for Matplotlib
matplotlib.use('QtAgg')


class MplCanvas(FigureCanvas):

    def __init__(self, width=5, height=4, dpi=100, id=1, parent=None):
        self.fig = plt.figure(figsize=(width, height), dpi=dpi, num=id, clear=True)
        self.axes = self.fig.add_subplot(111)
        self._width = width
        self._height = height
        self._dpi = dpi

        super(MplCanvas, self).__init__(self.fig)

    def reset(self, id=1):
        # self.fig.clear()
        self.fig = plt.figure(figsize=(self._width, self._height), dpi=self._dpi, num=id, clear=True)
        self.axes = self.fig.add_subplot(111)


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("PySide6 and Matplotlib Example")
        self.setGeometry(100, 100, 800, 600)

        self._layout = QGridLayout()
        self.setLayout(self._layout)

        self._first = -1
        self._second = -1

    def setupPlotFirst(self):
        self._first_canvas = MplCanvas(width=5, height=4, dpi=100, id=1)

        self._first_slider = QSlider()
        self._first_slider.setOrientation(Qt.Horizontal)
        self._first_slider.setTickInterval(10)
        self._first_slider.setMinimum(int(self._first_min))
        self._first_slider.setMaximum(int(self._first_max))
        self._first_slider.setValue(int(self._first))
        self._first_slider.setTickPosition(QSlider.TicksBelow)

        self._first_slider_left_icon = QToolButton()
        self._first_slider_left_icon.setIcon(QPixmap("./rotateleft.png"))
        self._first_slider_left_icon.setIconSize(QSize(15, 15))

        self._first_slider_right_icon = QToolButton()
        self._first_slider_right_icon.setIcon(QPixmap("./rotateright.png"))
        self._first_slider_right_icon.setIconSize(QSize(15, 15))

        self._first_slider_layout = QHBoxLayout()
        self._first_slider_layout.addWidget(self._first_slider_left_icon)
        self._first_slider_layout.addWidget(self._first_slider)
        self._first_slider_layout.addWidget(self._first_slider_right_icon)

        self._first_toolbar = NavigationToolbar(self._first_canvas, self)

        self._layout.addWidget(self._first_canvas, 0, 0)
        self._layout.addLayout(self._first_slider_layout, 1, 0)
        self._layout.addWidget(self._first_toolbar, 2, 0)

        self._first_slider.valueChanged.connect(self.plotall)
        self._first_slider_left_icon.clicked.connect(self.leftFirst)
        self._first_slider_right_icon.clicked.connect(self.rightFirst)

    def setupPlotSecond(self):
        self._second_canvas = MplCanvas(width=5, height=4, dpi=100, id=2)

        self._second_slider = QSlider()
        self._second_slider.setOrientation(Qt.Horizontal)
        self._second_slider.setTickInterval(10)
        self._second_slider.setMinimum(int(self._second_min))
        self._second_slider.setMaximum(int(self._second_max))
        self._second_slider.setValue(int(self._second))
        self._second_slider.setTickPosition(QSlider.TicksBelow)

        self._second_slider_left_icon = QToolButton()
        self._second_slider_left_icon.setIcon(QPixmap("./rotateleft.png"))
        self._second_slider_left_icon.setIconSize(QSize(15, 15))

        self._second_slider_right_icon = QToolButton()
        self._second_slider_right_icon.setIcon(QPixmap("./rotateright.png"))
        self._second_slider_right_icon.setIconSize(QSize(15, 15))

        self._second_slider_layout = QHBoxLayout()
        self._second_slider_layout.addWidget(self._second_slider_left_icon)
        self._second_slider_layout.addWidget(self._second_slider)
        self._second_slider_layout.addWidget(self._second_slider_right_icon)

        self._second_toolbar = NavigationToolbar(self._second_canvas, self)

        self._layout.addWidget(self._second_canvas, 0, 1)
        self._layout.addLayout(self._second_slider_layout, 1, 1)
        self._layout.addWidget(self._second_toolbar, 2, 1)

        self._second_slider.valueChanged.connect(self.plotall)
        self._second_slider_left_icon.clicked.connect(self.leftSecond)
        self._second_slider_right_icon.clicked.connect(self.rightSecond)

    def readCSV(self, filename, legend, sep=r'\s+', header=None, header_titles=None):
        self._header_titles = header_titles
        self._legend = legend
        self._data = []
        for name in filename:
            data = pd.read_csv(name, sep=sep, header=header)
            if header is None:
                data.columns = self._header_titles
            self._data.append(data)

        self._first_min = self._data[0][header_titles[0]].min()
        self._first_max = self._data[0][header_titles[0]].max()

        self._second_min = self._data[0][header_titles[1]].min()
        self._second_max = self._data[1][header_titles[1]].max()

        self._third_min = self._data[0][header_titles[2]].min()
        self._third_max = self._data[0][header_titles[2]].max()

        for data in self._data:
            self._first_min = min(data[header_titles[0]].min(), self._first_min)
            self._first_max = max(data[header_titles[0]].max(), self._first_max)

            self._second_min = min(data[header_titles[1]].min(), self._second_min)
            self._second_max = max(data[header_titles[1]].max(), self._second_max)

            self._third_min = min(data[header_titles[2]].min(), self._third_min)
            self._third_max = max(data[header_titles[2]].max(), self._third_max)

        self._first = int((self._first_min + self._first_max) / 2)
        self._second = int((self._second_min + self._second_max) / 2)

        self.setupPlotFirst()
        self.setupPlotSecond()
        self.plotall()

    def plotFirst(self):
        self._first = self._first_slider.value()
        header0, header1, header2 = self._header_titles[0], self._header_titles[1], self._header_titles[2]

        x = []
        y = []

        for data in self._data:
            filtered_df = data[data[header0] == self._first]
            x.append(filtered_df[header1])
            y.append(filtered_df[header2])

        self._first_canvas.reset(id=1)

        colors = matplotlib.colormaps['viridis'].resampled(len(x))
        for i in range(len(x)):
            self._first_canvas.axes.scatter(x[i], y[i], s=2, marker='o', color=colors(i), label=self._legend[i])

        self._first_canvas.axes.grid(True)
        self._first_canvas.axes.set_xlim(self._second_min, self._second_max)
        self._first_canvas.axes.set_xlabel(f'subline - {self._first}', fontsize=12)
        self._first_canvas.axes.vlines(x=self._second, ymin=self._third_min, ymax=self._third_max, colors='r')
        self._first_canvas.axes.set_ylim(self._third_min, self._third_max)
        self._first_canvas.axes.set_ylabel(f'depth', fontsize=12)
        self._first_canvas.axes.legend()
        self._first_canvas.fig.tight_layout()
        self._first_canvas.draw()

    def plotSecond(self):
        self._second = self._second_slider.value()
        header0, header1, header2 = self._header_titles[0], self._header_titles[1], self._header_titles[2]

        x = []
        y = []
        for data in self._data:
            filtered_df = data[data[header1] == self._second]
            x.append(filtered_df[header0])
            y.append(filtered_df[header2])

        self._second_canvas.reset(id=2)

        colors = matplotlib.colormaps['viridis'].resampled(len(x))
        for i in range(len(x)):
            self._second_canvas.axes.scatter(x[i], y[i], s=2, marker='o', color=colors(i), label=self._legend[i])

        self._second_canvas.axes.grid(True)
        self._second_canvas.axes.set_xlim(self._first_min, self._first_max)
        self._second_canvas.axes.set_xlabel(f'crossline - {self._second}', fontsize=12)
        self._second_canvas.axes.vlines(x=self._first, ymin=self._third_min, ymax=self._third_max, colors='r')
        self._second_canvas.axes.set_ylim(self._third_min, self._third_max)
        self._second_canvas.axes.set_ylabel(f'depth', fontsize=12)
        self._second_canvas.axes.legend()
        self._second_canvas.fig.tight_layout()
        self._second_canvas.draw()

    def leftFirst(self):
        self._first_slider.setValue(self._first_slider.value() - 1)

    def rightFirst(self):
        self._first_slider.setValue(self._first_slider.value() + 1)

    def leftSecond(self):
        self._second_slider.setValue(self._second_slider.value() - 1)

    def rightSecond(self):
        self._second_slider.setValue(self._second_slider.value() + 1)

    def plotall(self):
        self.plotFirst()
        self.plotSecond()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.readCSV(["elev.txt", "elev_shift.txt", "elev_smooth.txt", "elev_smooth2.txt"],
                   legend=["elev", "elev_shift", "elev_smooth", "elev_smooth2"], sep=r'\s+',
                   header=None,
                   header_titles=['subline', 'crossline', 'depth'])
    window.show()
    sys.exit(app.exec())
