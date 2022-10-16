class Immutable:
    _restrict = False

    def __init__(self) -> None:
        self._restrict = True
    
    def __delattr__(self, *args, **kwargs):
        if self._restrict:
            raise AttributeError('can\'t delete attribute')
        object.__delattr__(self, *args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        if self._restrict:
            raise AttributeError('can\'t set attribute')
        object.__setattr__(self, *args, **kwargs)
