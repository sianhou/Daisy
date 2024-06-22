from torch import nn

from core.dtype import Int, Bool
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

        self._params = dict()
        self._params['in_features'] = Int()
        self._params['out_features'] = Int()
        self._params['bias'] = Bool()

        # self.in_features: int = 0
        # self.out_features: int = 0
        # self.bias: bool = True
        self._model = None
        self._value = None

    def setupModel(self):
        self._model = nn.Linear(self.in_features, self.out_features, bias=self.bias)

    def forward(self, x):
        self._value = self._model(x)
