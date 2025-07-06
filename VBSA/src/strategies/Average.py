from .strategies import Strategy, PBStrategy

class Average(PBStrategy):
    def __init__(self, parameter: int = 2, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False
    
    def make_move(self, round: int = 0) -> float:
        """
        Starts with full cooperation.
        Returnes the average of the opponent's last parameter moves.
        Parameter 1 is identical to Tit4Tat. (See TitForTat.py)
        Parameter 0 throws a ZeroDivisionError.
        """
        if round <= self.parameter and self._start != None:
            return self._start
        elif self.parameter < 1:
            raise ValueError("Parameter out of range")
        else:
            return sum(self._opponent_history[-1 * self.parameter:])/len(self._opponent_history[-1 * self.parameter:])
