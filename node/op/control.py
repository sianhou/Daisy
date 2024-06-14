from core import dtype
from vg_node import Node
from node.port import NodeInput, NodeOutput


class BranchNode(Node):
    package_name = 'Control'
    node_title = "Branch"
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


class ForeachNode(Node):
    package_name = 'Control'
    node_title = "Foreach"
    node_description = "Foreach loop"

    input_pins = [
        NodeInput(pin_type='exec'),
        NodeInput(pin_name='start', pin_class=dtype.Int, pin_type='data'),
        NodeInput(pin_name='end', pin_class=dtype.Int, pin_type='data'),
        NodeInput(pin_name='arrays', pin_class='list', pin_type='data', use_default_widget=False)
    ]

    output_pins = [
        NodeOutput(pin_name='Loop Body', pin_type='exec'),
        NodeOutput(pin_name='index', pin_class=dtype.Int, pin_type='data'),
        NodeOutput(pin_name='index', pin_class=dtype.Int, pin_type='data'),
        NodeOutput(pin_name='Completed', pin_type='exec')
    ]

    def run(self):
        pass
