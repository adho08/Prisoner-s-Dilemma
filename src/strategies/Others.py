from .strategies import Strategy, PBStrategy
import builtins

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
    def __init__(self, parameter: int = 1, start = 0.5, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None) -> float:
        """
        Starts the first two rounds with full cooperation.
        If the opponent defected more than Adapt, defect parameter/10 more in the next round.
        If the opponent cooperated more than Adapt, go the that level of cooperation in the next round.
        Parameter 0 is identical to AlwaysCooperate. (See Basic.py)
        """
        if round < 2 and self._start != None:
            return self._start
        # if opponent's move is greater than the last own move, cooperate parameter/10 more than last round 
        elif self._opponent_history[-1] >= self._history[-1]:
            return max(0.0, min(1.0, self._history[-1] + self.parameter/10))
        # else defect parameter/10 more
        else:
            return max(0.0, min(1.0, self._history[-1] - self.parameter/10))

class Adapt3(PBStrategy):
    def __init__(self, parameter: int = 1, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None) -> float:
        """
        Starts the first two rounds with full cooperation.
        If the opponent defected more than Adapt, defect parameter/10 more in the next round.
        If the opponent cooperated more than Adapt, go the that level of cooperation in the next round.
        Parameter 0 is identical to AlwaysCooperate. (See Basic.py)
        """
        if round < 2 and self._start != None:
            return self._start
        # if opponent's move is greater than the last own move, go to his level of cooperation
        elif self._opponent_history[-1] >= self._history[-1]:
            print(self._history[-1] + self.parameter/10, builtins.round(max(0.0, min(1.0, self._history[-1] + self.parameter/10))))
            return builtins.round(self._history[-1] + self.parameter/10)
        # else defect parameter/10 more
        else:
            print(builtins.round(self._history[-1] - self.parameter/10))
            return builtins.round(self._history[-1] - self.parameter/10)

class AdaptContinuous(PBStrategy):
    def __init__(self, parameter: int = 1, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None) -> float:
        """
        Start first round with full cooperation.
        It takes the difference between the two contributions and adds that difference to its previous contribution.
        This shift is the difference multiplied by the parameter/5.
        Parameter 0 is AlwaysCooperate.
        Parameter 5 is Tit-For-Tat.
        Parameter 10 will submit twice the difference applied on the previous investment.
        """
        if round == 1 and self._start != None:
            return self._start
        else:
            s = self.parameter/5 * (self._opponent_history[-1] - self._history[-1])
            return max(0.0, min(1.0, self._history[-1] + s))

class AdaptDiscrete(PBStrategy):
    def __init__(self, parameter: int = 1, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None) -> float:
        """
        Start first round with full cooperation.
        It takes the difference between the two contributions and adds that difference to its previous contribution.
        This shift is the difference multiplied by the parameter/5.
        Parameter 0 is AlwaysCooperate.
        """
        if round == 1 and self._start != None:
            return self._start
        else:
            s = self.parameter/5 * (self._opponent_history[-1] - self._history[-1])
            i = self._history[-1] + s
            return 1.0 if i >= 0.5 else 0.0 # round to nearest integer (0.5 is rounded upwards)
