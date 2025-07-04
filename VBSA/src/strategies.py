from abc import ABC, abstractmethod
import random
import numpy as np
from functools import total_ordering

@total_ordering
class Strategy(ABC):
    def __init__(self, start: float | None, name: str | None = None):

        self._start = start

        self._isNice = None if self._start == None or self._start == 0.5 else True if self._start > 0.5 else False
        # These attributes have to be defined inside each strategy as they depend heavily on their behaviour
        self._retaliates = None
        self._isForgiving = None
        self._isEnvious = None

        self._history: list[float] = []
        self._opponent_history: list[float] = []
        self.points: float = 0

        self.MAX = 0
        self.MC = 0
        self.MIN = 0
        self.MD = 0

        self.parameter = 0
        
        # set the name of the instance to the name of the class by default
        if name is None:
            self._name = self.__class__.__name__
        else:
            self._name = name

    def make_move(self, round: int = 0) -> float:
        raise NotImplementedError("Subclasses must implement this method")

    # Update the history or own moves, opponent moves and points
    def update(self, move: float, opponent_move: float, payoff: float) -> None:
        self._history.append(move)
        self._opponent_history.append(opponent_move)
        self.points += payoff

    def reset(self) -> None:
        self._history = []
        self._opponent_history = []
        self.points = 0

    def set_payoffs(self, max: int, min: int, mc: int, md: int) -> None:
        self.MAX = max
        self.MC = min
        self.MIN = mc
        self.MD = md

    def append_to_name(self, name: str) -> None:
        self._name += name

    def __repr__(self):
        return self._name

    def __format__(self, format_spec):
        return self._name

    def __eq__(self, other) -> bool:
        return self.points == other.points

    def __lt__(self, other) -> bool:
        return self.points < other.points

    def __gt__(self, other) -> bool:
        if self.points >= other.points:
            return self._name >= other.name
        return self.points >= other.points

# Parameter-Based Strategy
class PBStrategy(Strategy):
    def __init__(self, parameter: int = 0, start: float | None = None, name: str | None = None) -> None:
        super().__init__(start, name)
        self.init_param = parameter
        self.parameter = parameter

    def reset_parameter(self) -> None:
        self.parameter = self.init_param

class AlwaysCooperate(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)
        self._retaliates = False
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None):
        return 1.0

class AlwaysDefect(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.0, name)
        self._retaliates = True 
        self._isForgiving = False
        self._isEnvious = True 

    def make_move(self, round=None):
        return 0.0

class Tit4Tat(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)
        self._retaliates = True 
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None):
        # return the same as the opponent returned in the last round, start with 1.0/Cooperate
        if round == 0 and self._start != None:
            return self._start
        else:
            return self._opponent_history[-1]

class Random(PBStrategy):
    def __init__(self, parameter: int = 1, start = None, name: str | None = None):
        super().__init__(parameter, start, name)

    def make_move(self, round: int = 0):
        return 1.0 if np.random.choice([True, False], p=[1 - self.parameter/10, self.parameter/10]) else 0.0

class Inverse(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(1.0, name)

    def make_move(self, round: int = 0):
        """
        returnes the required value to calculate the average of MAX/2
        start with 1.0/Cooperate
        """
        if round == 0 and self._start != None:
            return self._start
        else:
            return 2 * self.MAX - self._opponent_history[round - 1]

class Neutral(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.5, name)
        self._retaliates = False
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round: int = 0) -> float:
        return 0.5

class Tit4TatB(Strategy):
    def __init__(self, name: str | None = None):
        super().__init__(0.0, name)
        self._retaliates = True 
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None):
        # return the same as the opponent returned in the last round, start with 1.0/Cooperate
        if round == 0 and self._start != None:
            return self._start
        else:
            return self._opponent_history[-1]

class Adapt(PBStrategy):
    def __init__(self, parameter: int = 1, start = 1.0, name: str | None = None):
        super().__init__(parameter, start, name)
        self._retaliates = True
        self._isForgiving = True
        self._isEnvious = False

    def make_move(self, round=None) -> float:
        if round < 2 and self._start != None:
            return self._start
        # if opponent's move is greater than the last own move, go to his level of cooperation
        elif self._opponent_history[-1] >= self._history[-1]:
            return self._opponent_history[-1]
        # else defect parameter/20 more
        else:
            return max(0.0, min(1.0, self._history[-1] - self.parameter/20))

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
