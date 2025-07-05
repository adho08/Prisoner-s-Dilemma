from strategies.py import Strategy, PBStrategy

class Average(PBStrategy):
    def __init__(self, parameter: int = 2, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False
    
    # Update the history or own moves, opponent moves and points and increment parameter by one
    def update(self, move: float, opponent_move: float, payoff: float) -> None:
        self._history.append(move)
        self._opponent_history.append(opponent_move)
        self.points += payoff

    def make_move(self, round: int = 0) -> float:
        """
        starts with full cooperation
        returnes the average of the opponent's last parameter moves
        """
        if round <= self.parameter and self._start != None:
            return self._start
        elif self.parameter < 1:
            raise ValueError("Parameter out of range")
        else:
            return sum(self._opponent_history[-1 * self.parameter:])/len(self._opponent_history[-1 * self.parameter:])
