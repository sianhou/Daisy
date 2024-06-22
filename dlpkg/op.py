from copy import copy

from torch import nn

from core.node.mininode import MiniNode
from core.port import InputPort, OutputPort


class ParamPin():
    def __init__(self, name='', type=int):
        self.name = name
        self.type = type
        self.value = type()


class ParamPinList():
    def __init__(self):
        self._param_pins: [ParamPin] = []

    def __getitem__(self, item):
        for pin in self._param_pins:
            if pin.name == item:
                return pin.value
        return None


class Linear(MiniNode):
    model_name = 'Linear layer'
    model_params = [
        ParamPin(name='in_features', type=int),
        ParamPin(name='out_features', type=int),
        ParamPin(name='bias', type=bool),
    ]
    num_input_ports = 2
    num_output_ports = 1

    def __init__(self):
        super().__init__()

        self.setup(width=120)
        self.setTitle(title=self.model_name)

        # setup variables
        self.addInputPortList([InputPort() for _ in range(self.num_input_ports)])
        self.addOutputPortList([OutputPort() for _ in range(self.num_output_ports)])
        self.params = [copy(pin) for pin in self.model_params]

        self._model = None
        self._value = None

    def setup_model(self):
        self._model = nn.Linear(in_features=self._model['in_features'], out_features=self._model['out_features'],
                                bias=self._model['bias'])

    def forward(self, x):
        self._value = self._model(x)


if __name__ == '__main__':
    print(Linear.model_params)
    # print(type(Linear.model_params['in_features']))
    # print(type(Linear.model_params['out_features']))
    # print(type(Linear.model_params['bias']))
