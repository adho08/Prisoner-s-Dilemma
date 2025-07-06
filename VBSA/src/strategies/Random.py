from .strategies import Strategy, PBStrategy
import numpy as np
import random

class RandomDiscrete(PBStrategy):
    def __init__(self, parameter: int = 1, start = None, name: str | None = None):
        super().__init__(parameter, start, name)

    def make_move(self, round: int = 0):
        """
        Can only return either 1.0 or 0.0.
        Returns 1.0 with a chance of 1-parameter/10. Returning 0.0 has a chance of parameter/10.
        It is recommended to pass in a list of parameter of range from 0 to 10 inclusively.
        Parameter 0 has identical to AlwaysCooperate and parameter 1 corresponds to AlwaysDefect. (See Basic.py)
        """
        return 1.0 if np.random.choice([True, False], p=[1 - self.parameter/10, self.parameter/10]) else 0.0

class RandomNeutral(PBStrategy):
    def __init__(self, parameter: int = 1, start = None, name: str | None = None):
        super().__init__(parameter, start, name)

    def make_move(self, round: int = 0):
        """
        Base case is 0.5.
        The deviation is dependend on the parameter.
        Return the base with the deviation being added or subtracted chances being 50%.
        Parameter 0 is identical to Neutral. (See Basic.py)
        """
        deviation = self.parameter/20
        return 0.5 + deviation if np.random.choice([True, False]) else 0.5 - deviation
