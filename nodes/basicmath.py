from vg_node import Node
from vg_node_port import NodeInput, NodeOutput


class AddNode(Node):
    package_name = 'Basic Operation'
    node_title = 'Add'
    node_description = 'z = x + y'

    input_pins = [
        NodeInput(pin_name='x', pin_class='float', pin_type='data', pin_color='#99ff22'),
        NodeInput(pin_name='y', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class='float', pin_type='data', pin_color='#99ff22'),
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
        NodeInput(pin_name='x', pin_class='float', pin_type='data', pin_color='#99ff22'),
        NodeInput(pin_name='y', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class='float', pin_type='data', pin_color='#99ff22'),
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
        NodeInput(pin_name='x', pin_class='float', pin_type='data', pin_color='#99ff22'),
        NodeInput(pin_name='y', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class='float', pin_type='data', pin_color='#99ff22'),
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
        NodeInput(pin_name='x', pin_class='float', pin_type='data', pin_color='#99ff22'),
        NodeInput(pin_name='y', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]

    def run(self):
        x = self.input_pins[0].getValue()
        y = self.input_pins[1].getValue()
        z = x / y
        self.output_pins[0].setValue(z)


class GreaterNode(Node):
    package_name = 'Basic Operation'
    node_title = 'Greater'
    node_description = 'z = 1 if x > y else 0'

    input_pins = [
        NodeInput(pin_name='x', pin_class='float', pin_type='data', pin_color='#99ff22'),
        NodeInput(pin_name='y', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]
    output_pins = [
        NodeOutput(pin_name='z', pin_class='bool', pin_type='data', pin_color='#ff3300'),
    ]

    def run(self):
        x = self.input_pins[0].getValue()
        y = self.input_pins[1].getValue()
        z = 1 if x > y else 0
        self.output_pins[0].setValue(z)
