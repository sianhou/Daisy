from old.core import dtype
from old.node.port import NodeInput, NodeOutput
from old.vg_node import Node

pkg_name = 'Branch'


class BranchNode(Node):
    package_name = pkg_name
    node_title = "if-else"
    node_description = "Exectue based on input condition"

    input_pins = [
        NodeInput(pin_name='IF', pin_type='exec'),
        NodeInput(pin_name='Condition', pin_class=dtype.Bool)
    ]

    output_pins = [
        NodeOutput(pin_name='True', pin_type='exec'),
        NodeOutput(pin_name='False', pin_type='exec')
    ]

    def setup(self):
        self.node_title = "Branch"
        self.node_description = "Exectue based on input condition"

        self.input_pins = [
            NodeInput(pin_name='IF', pin_type='exec'),
            NodeInput(pin_name='Condition', pin_class=dtype.Bool)
        ]

        self.output_pins = [
            NodeOutput(pin_name='True', pin_type='exec'),
            NodeOutput(pin_name='False', pin_type='exec')
        ]

    def run(self):
        if self.input_pins[1]:
            self.exec(0)
        else:
            self.exec(1)
