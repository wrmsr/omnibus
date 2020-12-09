class C:
    def __new__(cls, x):
        bcls = type(
            '$' + cls.__name__,
            (cls,),
            {
                '__new__': super().__new__,
            },
        )
        return bcls.__new__(bcls)

    def __init__(self, x):
        super().__init__()
        self.x = x

    def __repr__(self):
        return f'{type(self).__name__}(x={self.x})'


print(C(1))
