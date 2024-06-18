import sys
from PySide6.QtWidgets import QApplication

from vg_editor import VisualGraphEditor

if __name__ == "__main__":
    app = QApplication([])

    vg = VisualGraphEditor()

    sys.exit(app.exec())
