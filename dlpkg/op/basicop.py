from core import dtype
from core.node.mininode import MiniNode
from core.port import InputPort

pkg_name = 'basic mathematical operations'


class AddNode(MiniNode):
    def __init__(self, parent=None):
        super(AddNode, self).__init__(parent)

        self.addInputPortList([InputPort(port_dtype=dtype.Float)])
