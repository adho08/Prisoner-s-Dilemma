from .strategies import Strategy, PBStrategy
from numpy import mean

class Average(PBStrategy):
    def __init__(self, parameter: int = 2, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round: int = 0) -> float:
        """
        Starts with full cooperation in the first parameter rounds.
        Returnes the average of the opponent's last parameter+1 moves.
        It is parameter+1 to unify the parameter list from 0 to 10, so the parameter 0 doesn't throw a ZeroDivisionError.
        Parameter 0 is identical to Tit4Tat. (See TitForTat.py)
        """
        if round <= self.parameter and self._start != None:
            return self._start
        else:
            return float(mean(self._opponent_history[-1 * (self.parameter + 1):]))
