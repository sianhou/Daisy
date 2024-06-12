from vg_node import Node
from vg_node_port import NodeInput, NodeOutput


class AddNode(Node):
    package_name = 'Basic Operation'
    node_title = 'Add'
    node_description = 'Adds two numbers'
    input_pins = [
        NodeInput(pin_name='num1', pin_class='float', pin_type='data', pin_color='#99ff22'),
        NodeInput(pin_name='num2', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]
    output_pins = [
        NodeOutput(pin_name='sum', pin_class='float', pin_type='data', pin_color='#99ff22'),
    ]

    def setup(self):
        self.node_title = 'Add'
        self.node_description = 'Adds two numbers'
        self.input_pins = [
            NodeInput(pin_name='num1', pin_class='float', pin_type='data', pin_color='#99ff22'),
            NodeInput(pin_name='num2', pin_class='float', pin_type='data', pin_color='#99ff22'),
        ]
        self.output_pins = [
            NodeOutput(pin_name='sum', pin_class='float', pin_type='data', pin_color='#99ff22'),
        ]

    def run(self):
        sum = 0;
        for pin in self.input_pins:
            sum += pin.getValue()

        self.output_pins[0].setValue(sum)
