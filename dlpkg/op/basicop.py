from base.port import InputPort
from dlpkg.dlnode import DeepLearningNode
from env import dtype

pkg_name = 'basic mathematical operations'


class AddNode(DeepLearningNode):
    def __init__(self, parent=None):
        super(AddNode, self).__init__(parent)

        self.addInputPortList([InputPort(port_dtype=dtype.Float)])
