from PySide6.QtCore import QRectF
from PySide6.QtGui import QDoubleValidator, QIntValidator, QFontMetrics, QColor, QFont
from PySide6.QtWidgets import QCheckBox, QLineEdit, QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget

from env.config import EditorConfig


class ParamItem(QGraphicsItem):
    _param_color = QColor('#eeeeee')
    _param_font = QFont(EditorConfig.param_item_title_font,
                        EditorConfig.param_item_title_font_size)

    _param_fm = QFontMetrics(_param_font)
    _param_padding = 10

    def __init__(self, title='', type=int, parent=None):
        super(ParamItem, self).__init__(parent=parent)
        self._title = title
        self._type = type
        self.value = type()
        self._width = 10
        self._height = 10

        # setup title
        self._title_item = QGraphicsTextItem(self)
        self._title_item.setPlainText(self._title)
        self._title_item.setFont(self._param_font)
        self._title_item.setDefaultTextColor(QColor('#eeeeee'))
        self._title_item.setPos(0, 0)
        self._title_item.setParentItem(self)

        # setup default_widget
        self._input_widget = None
        if self._type == bool:
            self._input_widget = QCheckBox()
        elif self._type == float:
            self._input_widget = QLineEdit()
            self._input_widget.setValidator(QDoubleValidator())
        elif self._type == int:
            self._input_widget = QLineEdit()
            self._input_widget.setValidator(QIntValidator())
        elif self._type == str:
            self._input_widget = QLineEdit()

        if isinstance(self._input_widget, QLineEdit):
            self._input_widget.setTextMargins(0, 0, 0, 0)
            self._input_widget.setFixedWidth(100)
            self._input_widget.setFixedHeight(self._param_fm.height())
        elif isinstance(self._input_widget, QCheckBox):
            self._input_widget.setFixedWidth(self._param_fm.height())
            self._input_widget.setFixedHeight(self._param_fm.height())

        self._widget_proxy = QGraphicsProxyWidget(parent=self)
        self._widget_proxy.setWidget(self._input_widget)
        self._widget_proxy.setPos(self._param_fm.horizontalAdvance(self._title) + self._param_padding, 0)
        self._widget_proxy.setParentItem(self)

        self.updateSize()

    def updateSize(self):
        self._width = self._param_fm.horizontalAdvance(
            self._title) + self._param_padding + self._input_widget.size().width()
        self._height = self._param_fm.height()

    def boundingRect(self):
        return QRectF(0, 0, self._width, self._height)

    def paint(self, painter, option, widget):
        pass


class ParamItemList(list):
    def __init__(self, *args):
        super().__init__(*args)

        self._default_widget = None

    def __getitem__(self, item):
        for pin in self:
            if pin._title == item:
                return pin.value
        return IndexError

    def __setitem__(self, item, value):
        for pin in self:
            if pin._title == item:
                pin.value = pin._type(value)
