import profile
import sys

from PySide6.QtWidgets import QApplication

from core.editor import NodeEditor


def run():
    app = QApplication(sys.argv)
    window = NodeEditor()
    sys.exit(app.exec())


if __name__ == '__main__':
    profile.run('run()')
