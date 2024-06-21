from torch import nn

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

        self.in_features: int = 0
        self.out_features: int = 0
        self.bias: bool = True

    def forward(self, X):
        self._linear = nn.Linear(X.shape[1], X.shape[1])
