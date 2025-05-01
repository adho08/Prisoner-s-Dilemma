import random
from functools import total_ordering
import game

@total_ordering
class Strategy(object):
    def __init__(self, start: bool, name: str | None = None):
        self.start = start
        self.history: list[bool] = []
        self.opponent_history: list[bool] = []
        self.points: int = 0

        # set the name of the instance to the name of the class by default
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def make_move(self, round: int = 0) -> CPDVector1D:
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, move: bool, opponent_move: bool, payoff: int) -> None:
        self.history.append(move)
        self.opponent_history.append(opponent_move)
        self.points += payoff

    def reset(self) -> None:
        self.history = []
        self.opponent_history = []

    def __repr__(self):
        return self.name

    def __eq__(self, other) -> bool:
        return self.points == other.points

    def __lt__(self, other) -> bool:
        return self.points < other.points

    def __gt__(self, other) -> bool:
        if self.points >= other.points:
            return self.name >= other.name
        return self.points >= other.points

class AlwaysCooperate(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(True, name)

    def make_move(self, round):
        return True

class AlwaysDefect(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(False, name)

    def make_move(self, round=None) -> bool:
        # return always False/Defect
        return False

class Tit4Tat(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(True, name)

    def make_move(self, round=None):
        # return the same as the opponent returned in the last round, start with True/Cooperate
        if round == 0:
            return self.start
        else:
            return self.opponent_history[round - 1]

class Random(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(True, name)

    def make_move(self, round=None):
        return random.choice([True, False])
