from torch import nn

from core.node.dln import DLN
from core.paramcard import ParamItem, ParamItemList, InputParamItem, OutputParamItem


class Linear(DLN):
    pkg_name = 'Basic Layer'
    model_name = 'Linear'

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


class Int(DLN):
    pkg_name = 'Scalar'
    model_name = 'Int'

    num_input_ports = 0
    num_output_ports = 1

    def setupParams(self):
        self._input_params = []
        self._output_params = [
            OutputParamItem(title='x', type=int)
        ]

    def run(self):
        self.updateParams()
        print(f"One[info]: value = {self._output_params[0].getValue()}")

    def forward(self, x):
        print(f"value = {x}")


class Add(DLN):
    pkg_name = 'Math'
    model_name = 'Add'

    num_input_ports = 2
    num_output_ports = 1

    def setupParams(self):
        self._input_params = [
            InputParamItem(title='x', type=int),
            InputParamItem(title='y', type=int)
        ]
        self._output_params = [
            OutputParamItem(title='z', type=int)
        ]
        #
        # self._params = [
        #
        #     ,
        # ]

    def run(self):
        x, y, z = None, None, None
        if len(self._input_params[0]._port._edges) == 0:
            self._input_params[0].getValueFromInputWidget()
            x = self._input_params[0].getValue()
        else:
            self._input_params[0]._port._edges[0]._source_port._param_item.getValueFromInputWidget()
            x = self._input_params[0]._port._edges[0]._source_port._param_item.getValue()

        if len(self._input_params[1]._port._edges) == 0:
            self._input_params[1].getValueFromInputWidget()
            y = self._input_params[1].getValue()
        else:
            self._input_params[1]._port._edges[0]._source_port._param_item.getValueFromInputWidget()
            y = self._input_params[1]._port._edges[0]._source_port._param_item.getValue()

        z = x + y
        print(f"Add[info]: value = {z}")


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
