from vg_node import Node
from vg_node_port import NodeInput, NodeOutput


class BranchNode(Node):
    def setup(self):
        self.node_title = "Branch"
        self.node_description = "Exectue based on input condition"

        self.input_pins = [
            NodeInput(pin_name='IF', pin_type='exec'),
            NodeInput(pin_name='Condition', pin_class='bool', pin_color='#ff3300')
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
