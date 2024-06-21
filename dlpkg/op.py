from core.port import InputPort, OutputPort
from dlpkg.dlnode import DeepLearningNode


class Linear(DeepLearningNode):
    op_name = 'Linear'

    def __init__(self):
        super().__init__()

        self.setup(width=120)
        self.setTitle(title=self.op_name)

        self.addInputPortList([InputPort()])
        self.addOutputPortList([OutputPort()])
