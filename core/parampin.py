class ParamPin():
    def __init__(self, name='', type=int):
        self.name = name
        self.type = type
        self.value = type()


class ParamPinList(list):
    def __init__(self, *args):
        super().__init__(*args)

    def __getitem__(self, item):
        for pin in self:
            if pin.name == item:
                return pin.value
        return IndexError

    def __setitem__(self, item, value):
        for pin in self:
            if pin.name == item:
                pin.value = pin.type(value)
