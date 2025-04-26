from __future__ import annotations
import random
from functools import total_ordering

@total_ordering
class Strategy:
    def __init__(self, start, name):
        self.start: bool = start
        self.history: list[bool] = []
        self.opponent_history: list[bool] = []
        self.points: int = 0

        # set the name of the instance to the name of the class by default
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def make_move(self, round: int = 0) -> bool:
        # Return True for 'c' or False for 'd'
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, move, opponent_move) -> None:
        self.history.append(move)
        self.opponent_history.append(opponent_move)

    def reset(self) -> None:
        self.history = []
        self.opponent_history = []

    def __repr__(self):
        return self.name

    def __eq__(self, other: Strategy):
        return self.points == other.points

    def __lt__(self, other):
        return self.points < other.points

    def __gt__(self, other):
        if self.points >= other.points:
            return self.name >= other.name
        return self.points >= other.points

class AlwaysCooperate(Strategy):
    def __init__(self, name=None):
        super().__init__(True, name)

    def make_move(self, round):
        return True

class AlwaysDefect(Strategy):
    def __init__(self, name=None):
        super().__init__(False, name)

    def make_move(self, round=None):
        # pylint: disable=unused-argument
        return False

class Tit4Tat(Strategy):
    def __init__(self, name=None):
        super().__init__(True, name)

    def make_move(self, round=1):
        if round == 0:
            return self.start
        else:
            return self.opponent_history[round - 1]

class Random(Strategy):
    def __init__(self, name=None):
        super().__init__(True, name)

    def make_move(self, round):
        return random.choice([True, False])
