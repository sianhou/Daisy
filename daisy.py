import sys

from PySide6.QtWidgets import QApplication

from core.editor import NodeEditor

if __name__ == '__main__':
    app = QApplication([])
    editor = NodeEditor()
    sys.exit(app.exec())
