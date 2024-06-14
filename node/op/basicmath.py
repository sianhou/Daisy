from core import dtype
from vg_node import Node
from node.port import NodeInput, NodeOutput


class AddNode(Node):
    package_name = 'Basic Operation'
    node_title = 'Add'
    node_description = 'z = x + y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input_pins[0].getValue()
        y = self.input_pins[1].getValue()
        z = x + y
        self.output_pins[0].setValue(z)


class MinusNode(Node):
    package_name = 'Basic Operation'
    node_title = 'Minus'
    node_description = 'z = x - y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input_pins[0].getValue()
        y = self.input_pins[1].getValue()
        z = x - y
        self.output_pins[0].setValue(z)


class MultiplyNode(Node):
    package_name = 'Basic Operation'
    node_title = 'Multiply'
    node_description = 'z = x * y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input_pins[0].getValue()
        y = self.input_pins[1].getValue()
        z = x * y
        self.output_pins[0].setValue(z)


class DivideNode(Node):
    package_name = 'Basic Operation'
    node_title = 'Divide'
    node_description = 'z = x / y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input_pins[0].getValue()
        y = self.input_pins[1].getValue()
        z = x / y
        self.output_pins[0].setValue(z)


class GreaterNode(Node):
    package_name = 'Basic Dule'
    node_title = 'Greater'
    node_description = 'z = 1 if x > y else 0'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Bool, pin_type='data'),
    ]

    def run(self):
        x = self.input_pins[0].getValue()
        y = self.input_pins[1].getValue()
        z = 1 if x > y else 0
        self.output_pins[0].setValue(z)
