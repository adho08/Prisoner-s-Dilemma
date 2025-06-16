from abc import ABC, abstractmethod
import random
from functools import total_ordering

@total_ordering
class Strategy(ABC):
    def __init__(self, start: float | None, name: str | None = None):

        self.start = start

        self.isNice = None if self.start == None else True if self.start >= 0.5 else False
        # These attributes have to be defined inside each strategy as they depend heavily on their behaviour
        self.retaliates = None
        self.isForgiving = None
        self.isEnvious = None

        self.history: list[float] = []
        self.opponent_history: list[float] = []
        self.points: int = 0

        self.MAX = 0
        self.MC = 0
        self.MIN = 0
        self.MD = 0
        
        # set the name of the instance to the name of the class by default
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def make_move(self, round: int = 0) -> float:
        raise NotImplementedError("Subclasses must implement this method")

    # Update the history or own moves, opponent moves and points
    def update(self, move: bool, opponent_move: bool, payoff: int) -> None:
        self.history.append(move)
        self.opponent_history.append(opponent_move)
        self.points += payoff

    def reset(self) -> None:
        self.history = []
        self.opponent_history = []

    @classmethod
    def setPayoffs(self, max: int, min: int, mc: int, md: int) -> None:
        self.MAX = max
        self.MC = min
        self.MIN = mc
        self.MD = md

    def appendName(self, name: str) -> None:
        self.name += name

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
        super().__init__(1.0, name)
        self.retaliates = False
        self.isForgiving = True
        self.isEnvious = False

    def make_move(self, round=None):
        return 1.0

class AlwaysDefect(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.0, name)
        self.retaliates = True 
        self.isForgiving = False
        self.isEnvious = True 

    def make_move(self, round=None):
        return 0.0

class Tit4Tat(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)
        self.retaliates = True 
        self.isForgiving = True
        self.isEnvious = False

    def make_move(self, round=None):
        # return the same as the opponent returned in the last round, start with 1.0/Cooperate
        if round == 0 and self.start != None:
            return self.start
        else:
            return self.opponent_history[-1]

class Random(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(None, name)

    def make_move(self, round: int = 0):
        return random.uniform(0, 1)

class Inverse(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)

    def make_move(self, round: int = 0):
        """
        returnes the required value to calculate the average of MAX/2
        start with 1.0/Cooperate
        """
        if round == 0 and self.start != None:
            return self.start
        else:
            return 2 * self.MAX - self.opponent_history[round - 1]

class Average2(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)
        self.retaliates = True
        self.isForgiving = True
        self.isEnvious = False

    def make_move(self, round: int = 0) -> float:
        """
        starts with cooperation
        returnes the average of the opponent's last two moves
        """
        if round < 2 and self.start != None:
            return self.start
        else:
            return (self.opponent_history[-1] + self.opponent_history[-2])/2
