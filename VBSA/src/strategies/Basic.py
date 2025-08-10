from .strategies import Strategy, PBStrategy

class AlwaysCooperate(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)
        self._retaliates = False
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None):
        return 1.0

    def reset_parameter(self):
        return 0

class AlwaysDefect(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.0, name)
        self._retaliates = True 
        self._isForgiving = False
        self._isEnvious = True 

    def make_move(self, round=None):
        return 0.0

    def reset_parameter(self):
        return 0

class Neutral(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.5, name)
        self._retaliates = False
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round: int = 0) -> float:
        return 0.5
