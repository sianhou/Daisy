from PySide6.QtCore import QRectF
from PySide6.QtGui import QBrush, QColor, QPen, QPainterPath, QFont, QFontMetrics, QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QCheckBox, QLineEdit, QGraphicsProxyWidget

from env.config import EditorConfig


class ParamItem(QGraphicsItem):
    _param_color = QColor('#eeeeee')
    _param_font = QFont(EditorConfig.param_title_font,
                        EditorConfig.param_title_font_size)

    _param_fm = QFontMetrics(_param_font)
    _param_padding = 10

    def __init__(self, title='', type=int, parent=None):
        super(ParamItem, self).__init__(parent=parent)
        self._title = title
        self._type = type
        self._value = type()
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
            self._input_widget.setStyleSheet(f'QCheckBox::indicator {{ '
                                             f'width: {self._param_fm.height()}px;'
                                             f'height: {self._param_fm.height()}px;'
                                             f'vertical-align: middle;'
                                             f'}}')
            self._input_widget.setFixedWidth(self._param_fm.height())
            self._input_widget.setFixedHeight(self._param_fm.height())

        self._widget_proxy = QGraphicsProxyWidget(parent=self)
        self._widget_proxy.setWidget(self._input_widget)
        self._widget_proxy.setPos(self._param_fm.horizontalAdvance(self._title) + self._param_padding,
                                  int(self._param_fm.height() / 4.0))
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

    def getValueFromInputWidget(self):
        temp_value = None
        if isinstance(self._input_widget, QLineEdit):
            temp_value = self._input_widget.text()
        elif isinstance(self._input_widget, QCheckBox):
            temp_value = self._input_widget.isChecked()

        if self._type == bool:
            self.setValue(bool(temp_value))
        elif self._type == float:
            self.setValue(float(temp_value))
        elif self._type == int:
            self.setValue(int(temp_value))
        elif self._type == str:
            self.setValue(str(temp_value))
        else:
            # TODO(housian)
            pass

    def setValue(self, value):
        self._value = value


class ParamItemList(list):
    def __init__(self, *args):
        super().__init__(*args)

        self._default_widget = None

    def __getitem__(self, item):
        for pin in self:
            if pin._title == item:
                return pin._value
        return IndexError

    def __setitem__(self, item, value):
        for pin in self:
            if pin._title == item:
                pin._value = pin._type(value)


class ParamCard(QGraphicsItem):
    def __init__(self, params_list: ParamItemList, parent=None):
        super().__init__(parent=parent)

        self._width = ParamItem._param_padding
        self._height = ParamItem._param_padding
        self._raduis = 10
        self._params_list = params_list
        self._params_list.append(ParamItem(title='!!! overwrite_weight', type=bool))

        self._background_brush = QBrush(QColor('#aa151515'))
        self._default_pen = QPen(QColor('#a1a1a1'))

        if len(self._params_list) > 0:
            for i, param in enumerate(self._params_list):
                temp_width = param._width + 2 * param._param_padding
                self._width = temp_width if temp_width > self._width else self._width
                param.setParentItem(self)
                param.setPos(param._param_padding, self._height)
                self._height += param._height + param._param_padding
        self._height += ParamItem._param_padding
        self.setZValue(10)

    def paint(self, painter, option, widget):
        # 画背景颜色
        node_line = QPainterPath()
        node_line.addRoundedRect(0, 0, self._width, self._height, self._raduis, self._raduis)
        painter.setPen(self._default_pen)
        painter.setBrush(self._background_brush)
        painter.drawPath(node_line.simplified())

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self._width, self._height)

    def addToParaentNode(self, node):
        self._parent_node = node
        self.setParentItem(node)
