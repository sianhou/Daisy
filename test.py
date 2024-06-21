import inspect

from torch import nn

params = vars(nn.Linear)
print(params)

sig = inspect.signature(nn.Linear.__init__)
print(sig)
