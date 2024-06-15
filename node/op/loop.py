from core import dtype
from node.port import NodeInput, NodeOutput
from vg_node import Node

pkg_name = 'Loop'


class ForeachNode(Node):
    package_name = pkg_name
    node_title = "foreach"
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
