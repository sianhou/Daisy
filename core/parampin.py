from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QCheckBox, QLineEdit


class ParamPin():
    def __init__(self, name='', type=int):
        self.name = name
        self.type = type
        self.value = type()

        # setup default_widget
        self._default_widget = None
        if self.type == bool:
            self._default_widget = QCheckBox()
        elif self.type == float:
            self._default_widget = QLineEdit()
            self._default_widget.setValidator(QDoubleValidator())
        elif self.type == int:
            self._default_widget = QLineEdit()
            self._default_widget.setValidator(QIntValidator())
        elif self.type == str:
            self._default_widget = QLineEdit()

        self._proxy = None


class ParamPinList(list):
    def __init__(self, *args):
        super().__init__(*args)

        self._default_widget = None

    def __getitem__(self, item):
        for pin in self:
            if pin.name == item:
                return pin.value
        return IndexError

    def __setitem__(self, item, value):
        for pin in self:
            if pin.name == item:
                pin.value = pin.type(value)
