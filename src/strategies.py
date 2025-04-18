import random
from functools import total_ordering

@total_ordering
class Strategy:
    def __init__(self, start, name):
        self.start = start
        self.history = []
        self.opponent_history = []
        self.points = 0

        # set the name of the instance to the name of the class by default
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def make_move(self, round):
        # Return True for 'c' or False for 'd'
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, move, opponent_move):
        self.history.append(move)
        self.opponent_history.append(opponent_move)

    def reset(self):
        self.history = []
        self.opponent_history = []

    def __repr__(self):
        return self.name

    def __eq__(self, other):
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

    def make_move(self, round):
        return False

class Tit4Tat(Strategy):
    def __init__(self, name=None):
        super().__init__(True, name)

    def make_move(self, round):
        if round == 0:
            return self.start
        else:
            return self.opponent_history[round - 1]

class Random(Strategy):
    def __init__(self, name=None):
        super().__init__(True, name)

    def make_move(self, round):
        return random.choice([True, False])
