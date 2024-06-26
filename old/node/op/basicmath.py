from old.core import dtype
from old.node.port import NodeInput, NodeOutput
from old.vg_node import Node

pkg_name = 'Basic Math'


class AddNode(Node):
    package_name = pkg_name
    node_title = 'add'
    node_description = 'z = x + y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input(1)
        y = self.input(2)
        z = x + y
        self.output(1, z)


class MinusNode(Node):
    package_name = pkg_name
    node_title = 'minus'
    node_description = 'z = x - y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input(1)
        y = self.input(2)
        z = x - y
        self.output(1, z)


class MultiplyNode(Node):
    package_name = pkg_name
    node_title = 'multiply'
    node_description = 'z = x * y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input(1)
        y = self.input(2)
        z = x * y
        self.output(1, z)


class DivideNode(Node):
    package_name = pkg_name
    node_title = 'divide'
    node_description = 'z = x / y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input(1)
        y = self.input(2)
        z = x / y
        self.output(1, z)


class GreaterNode(Node):
    package_name = pkg_name
    node_title = 'greater'
    node_description = 'x > y'

    input_pins = [
        NodeInput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeInput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]
    output_pins = [
        NodeOutput(pin_name='isTrue', pin_class=dtype.Bool, pin_type='data'),
        NodeOutput(pin_name='x', pin_class=dtype.Float, pin_type='data'),
        NodeOutput(pin_name='y', pin_class=dtype.Float, pin_type='data'),
    ]

    def run(self):
        x = self.input(1)
        y = self.input(2)
        z = x > y
        self.output(1, z)
        # self.output_pins[1].setValue(self.input_pins[0].getValue())
        # self.output_pins[2].setValue(self.input_pins[1].getValue())
