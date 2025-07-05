from strategies import Strategy, PBStrategy
 
class Tit4Tat(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)
        self._retaliates = True 
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None):
        # return the same as the opponent returned in the last round, start with 1.0/Cooperate
        if round == 0 and self._start != None:
            return self._start
        else:
            return self._opponent_history[-1]

class Tit4TatB(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.0, name)
        self._retaliates = True 
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None):
        # return the same as the opponent returned in the last round, start with 1.0/Cooperate
        if round == 0 and self._start != None:
            return self._start
        else:
            return self._opponent_history[-1]
