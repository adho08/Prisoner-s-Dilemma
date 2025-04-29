from strategies import Strategy
import numpy as np

class PrisonersDilemma:

    def __init__(self, strategies: list[Strategy]):
        # stored strategies in a list
        self.strategies = strategies

        # awarding points
        self.MAX: int = 5
        self.MC: int = 3
        self.MIN: int = 0
        self.MD: int = 1

        # cooperate = True
        # defect = False
        self.payoffs = [
            [tuple((self.MD, self.MD)), tuple((self.MAX, self.MIN))],
            [tuple((self.MIN, self.MAX)), tuple((self.MC, self.MC))]
        ]

    def award(self, move1: bool, move2: bool) -> tuple[int, int]:
        return self.payoffs[move1][move2]
