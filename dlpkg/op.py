from torch import nn

from core.node.dlnode import DLNode
from core.parampin import ParamPin, ParamPinList


# class ParamPinList():
#     def __init__(self):
#         self._param_pins: [ParamPin] = []
#
#     def __getitem__(self, item):
#         for pin in self._param_pins:
#             if pin.name == item:
#                 return pin.value
#         return None


class Linear(DLNode):
    model_name = 'Linear layer'

    num_input_ports = 2
    num_output_ports = 1

    def setupParams(self):
        self._params = [
            ParamPin(name='in_features', type=int),
            ParamPin(name='out_features', type=int),
            ParamPin(name='bias', type=bool),
        ]

    def setup_model(self):
        self._model = nn.Linear(in_features=self._model['in_features'], out_features=self._model['out_features'],
                                bias=self._model['bias'])

    def forward(self, x):
        self._value = self._model(x)


if __name__ == '__main__':
    param_list = ParamPinList()
    param_list.append(ParamPin(name='in_features', type=int))
    param_list.append(ParamPin(name='out_features', type=int))
    param_list.append(ParamPin(name='bias', type=bool))

    param_list['in_features'] = 1
    param_list['out_features'] = 2
    param_list['bias'] = 0

    print(param_list['in_features'])
    print(param_list['out_features'])
    print(param_list['bias'])

    # print(Linear.model_params)
    # print(type(Linear.model_params['in_features']))
    # print(type(Linear.model_params['out_features']))
    # print(type(Linear.model_params['bias']))
