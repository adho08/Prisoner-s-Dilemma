from abc import ABC, abstractmethod
import random
from functools import total_ordering

@total_ordering
class Strategy(ABC):
    def __init__(self, start: float | None, name: str | None = None):

        self.start = start

        self.isNice = None if self.start == None or self.start == 0.5 else True if self.start > 0.5 else False
        # These attributes have to be defined inside each strategy as they depend heavily on their behaviour
        self.retaliates = None
        self.isForgiving = None
        self.isEnvious = None

        self.history: list[float] = []
        self.opponent_history: list[float] = []
        self.points: float = 0

        self.MAX = 0
        self.MC = 0
        self.MIN = 0
        self.MD = 0

        self.parameter = 0
        
        # set the name of the instance to the name of the class by default
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def make_move(self, round: int = 0) -> float:
        raise NotImplementedError("Subclasses must implement this method")

    # Update the history or own moves, opponent moves and points
    def update(self, move: float, opponent_move: float, payoff: float) -> None:
        self.history.append(move)
        self.opponent_history.append(opponent_move)
        self.points += payoff

    def reset(self) -> None:
        self.history = []
        self.opponent_history = []

    def set_payoffs(self, max: int, min: int, mc: int, md: int) -> None:
        self.MAX = max
        self.MC = min
        self.MIN = mc
        self.MD = md

    def append_to_name(self, name: str) -> None:
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

# Parameter-Based Strategy
class PBStrategy(Strategy):
    def __init__(self, parameter: int = 0, start: float | None = None, name: str | None = None) -> None:
        super().__init__(start, name)
        self.parameter = parameter

    def set_parameter(self, value: int):
        self.parameter = value

    def increment_parameter(self):
        self.parameter += 1

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

class Neutral(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.5, name)
        self.retaliates = False
        self.isForgiving = True
        self.isEnvious = False

    def make_move(self, round: int = 0) -> float:
        return 0.5

class Tit4TatB(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.0, name)
        self.retaliates = True 
        self.isForgiving = True
        self.isEnvious = False

    def make_move(self, round=None):
        # return the same as the opponent returned in the last round, start with 1.0/Cooperate
        if round == 0 and self.start != None:
            return self.start
        else:
            return self.opponent_history[-1]

class Adapt(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)
        self.retaliates = True
        self.isForgiving = True
        self.isEnvious = False

    def make_move(self, round=None) -> float:
        if round < 2 and self.start != None:
            return self.start
        elif self.opponent_history[-1] >= self.history[-1]:
            return self.opponent_history[-1]
        else:
            return self.history[-1] - 0.2 if self.history[-1] > 0.2 else 0.0

class Average(PBStrategy):
    def __init__(self, parameter = 2, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self.retaliates = True
        self.isForgiving = True
        self.isEnvious = False
    
    # Update the history or own moves, opponent moves and points and increment parameter by one
    def update(self, move: float, opponent_move: float, payoff: float) -> None:
        self.history.append(move)
        self.opponent_history.append(opponent_move)
        self.points += payoff

    def make_move(self, round: int = 0) -> float:
        """
        starts with full cooperation
        returnes the average of the opponent's last parameter moves
        """
        if round < self.parameter and self.start != None:
            return self.start
        else:
            return sum(self.opponent_history[-1 * self.parameter:])/len(self.opponent_history[-1 * self.parameter:])
