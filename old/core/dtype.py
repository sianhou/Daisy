# coding:utf-8
from PySide6.QtWidgets import QCheckBox, QLineEdit

Bool = 'bool'
Float = 'float'
Int = 'int'
String = 'str'
List = 'list'
Tuple = 'tuple'
Dict = 'dict'
Class = 'class'
Vector = 'vector'

color_map = {
    'bool': '#cc0606',
    'float': '#2fFF09',
    'int': '#22EE90',
    'str': '#be0ba0',
    'list': '#d4aa24',
    'dict': '#ed6c03',
    'class': '#0747bb',
    'vector': '#055c54'
}

default_widget = {
    'bool': QCheckBox,
    'float': QLineEdit,
    'int': QLineEdit,
    'str': QLineEdit,
}
