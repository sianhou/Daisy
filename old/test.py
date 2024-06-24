import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QCursor, Qt


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cursor Example")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Move your mouse over the buttons")
        layout.addWidget(self.label)

        button_normal = QPushButton("Normal Cursor")
        button_normal.setCursor(QCursor(Qt.ArrowCursor))
        button_normal.clicked.connect(self.set_normal_cursor)
        layout.addWidget(button_normal)

        button_cross = QPushButton("Cross Cursor")
        button_cross.setCursor(QCursor(Qt.CrossCursor))
        button_cross.clicked.connect(self.set_cross_cursor)
        layout.addWidget(button_cross)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def set_normal_cursor(self):
        QApplication.restoreOverrideCursor()
        self.label.setText("Normal Cursor Set")

    def set_cross_cursor(self):
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        self.label.setText("Cross Cursor Set")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
