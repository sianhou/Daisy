from core import dtype
from node.port import NodeInput, NodeOutput
from vg_node import Node

pkg_name = 'X2Y'


class Bool2String(Node):
    package_name = pkg_name
    node_title = 'bool -> string'
    node_description = 'converts bool to string'

    input_pins = [
        NodeInput(pin_name='bool', pin_class=dtype.Bool, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='string', pin_class=dtype.String, pin_type='data')
    ]

    def run(self):
        self.output_pins[0].setValue('True' if self.input_pins[0].getValue() else 'False')


class Float2Int(Node):
    package_name = pkg_name
    node_title = 'float -> int'
    node_description = 'convert float to int'

    input_pins = [
        NodeInput(pin_name='float', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='int', pin_class=dtype.Int, pin_type='data')
    ]

    def run(self):
        self.output_pins[0].setValue(int(self.input_pins[0].getValue()))


class Float2String(Node):
    package_name = pkg_name
    node_title = 'float -> string'
    node_description = 'convert float to string'

    input_pins = [
        NodeInput(pin_name='float', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='string', pin_class=dtype.String, pin_type='data')
    ]

    def run(self):
        self.output_pins[0].setValue(f"{self.input_pins[0].getValue()}")


class Int2Float(Node):
    package_name = pkg_name
    node_title = 'int -> float'
    node_description = 'convert int to float'

    input_pins = [
        NodeInput(pin_name='int', pin_class=dtype.Int, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='float', pin_class=dtype.Float, pin_type='data')
    ]

    def run(self):
        self.output_pins[0].setValue(float(self.input_pins[0].getValue()))


class Int2String(Node):
    package_name = pkg_name
    node_title = 'int -> string'
    node_description = 'convert int to string'

    input_pins = [
        NodeInput(pin_name='int', pin_class=dtype.Int, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='string', pin_class=dtype.String, pin_type='data')
    ]

    def run(self):
        self.output_pins[0].setValue(f"{self.input_pins[0].getValue()}")
