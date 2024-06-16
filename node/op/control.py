from core import dtype
from node.port import NodeOutput, NodeInput
from vg_node import Node

pkg_name = 'Control'


class BeginNode(Node):
    package_name = pkg_name
    node_title = 'begin'
    node_description = '每个图必须包含一个begin'

    input_pins = []
    output_pins = [
        NodeOutput(pin_name='Begin', pin_type='exec')
    ]

    def run(self):
        self.run_output(0)


class PrintNode(Node):
    package_name = pkg_name
    node_title = 'print'
    node_description = 'print information to console'

    input_pins = [NodeInput(pin_name='', pin_type='exec'),
                  NodeInput(pin_name='str', pin_class=dtype.String)]
    output_pins = [NodeOutput(pin_name='', pin_type='exec'),
                   NodeOutput(pin_name='str', pin_class=dtype.String)]

    def run(self):
        # print('test value')
        print(self.input_pins[1].getValue())
