import torch
from torch import nn


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self._linear = nn.Linear(in_features=784, out_features=10).reset_parameters('linear', torch.rand(784, 10))

    def forward(self, x):
        return self._linear(x)


linear = Net()
print(linear)
