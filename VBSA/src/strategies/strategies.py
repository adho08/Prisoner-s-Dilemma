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

        super().__init__()

    @abstractmethod
    def make_move(self, round: int = 0) -> float:
        pass

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
    @abstractmethod
    def __init__(self, parameter: int = 0, start: float | None = None, name: str | None = None) -> None:
        super().__init__(start, name)
        self._init_parameter = self.parameter_list[0]
        self.parameter = self._init_parameter 

    @property
    def parameter_list(self) -> list[int]:
        return list(range(0, 10))

    def reset_parameter(self) -> None:
        self.parameter = self._init_parameter 
