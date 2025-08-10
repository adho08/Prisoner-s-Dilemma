from .strategies import Strategy, PBStrategy

class Inverse(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)

    def make_move(self, round: int = 0):
        """
        Returnes the required value to calculate the average of MAX/2
        Start with 1.0/Cooperate
        """
        if round == 0 and self._start != None:
            return self._start
        else:
            return 2 * self.MAX - self._opponent_history[round - 1]

class Adapt(PBStrategy):
    def __init__(self, parameter: int = 1, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None) -> float:
        """
        Starts the first two rounds with full cooperation.
        If the opponent defected more than Adapt, defect parameter/20 more in the next round.
        If the opponen cooperated more than Adapt, go the that level of cooperation in the next round.
        Parameter 0 is identical to AlwaysCooperate. (See Basic.py)
        """
        if round < 2 and self._start != None:
            return self._start
        # if opponent's move is greater than the last own move, go to his level of cooperation
        elif self._opponent_history[-1] >= self._history[-1]:
            return self._opponent_history[-1]
        # else defect parameter/20 more
        else:
            return max(0.0, min(1.0, self._history[-1] - self.parameter/10))

class Adapt2(PBStrategy):
    def __init__(self, parameter: int = 1, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None) -> float:
        """
        Starts the first two rounds with full cooperation.
        If the opponent defected more than Adapt, defect parameter/10 more in the next round.
        If the opponen cooperated more than Adapt, go the that level of cooperation in the next round.
        Parameter 0 is identical to AlwaysCooperate. (See Basic.py)
        """
        if round < 2 and self._start != None:
            return self._start
        # if opponent's move is greater than the last own move, go to his level of cooperation
        elif self._opponent_history[-1] >= self._history[-1]:
            return max(0.0, min(1.0, self._history[-1] + self.parameter/10))
        # else defect parameter/10 more
        else:
            return max(0.0, min(1.0, self._history[-1] - self.parameter/10))
