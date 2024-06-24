from torch import nn

from core.node.dln import DLN
from core.paramcard import ParamItem, ParamItemList


class Linear(DLN):
    pkg_name = 'Basic Layer'
    model_name = 'Linear layer'

    num_input_ports = 2
    num_output_ports = 1

    def setupParams(self):
        self._params = [
            ParamItem(title='in_features', type=int),
            ParamItem(title='out_features', type=int),
            ParamItem(title='bias', type=bool),
        ]

    def setupModel(self):
        self._model = nn.Linear(in_features=self._model['in_features'], out_features=self._model['out_features'],
                                bias=self._model['bias'])

    def forward(self, x):
        self._value = self._model(x)


if __name__ == '__main__':
    param_list = ParamItemList()
    param_list.append(ParamItem(title='in_features', type=int))
    param_list.append(ParamItem(title='out_features', type=int))
    param_list.append(ParamItem(title='bias', type=bool))

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
