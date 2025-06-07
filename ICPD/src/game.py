from strategies import *

class PrisonersDilemma:

    def __init__(self, strategies: list[Strategy]):
        # Stored strategies in a list and make names unique
        self.strategies = strategies

        # Make names of strategies in list unique to be counted as one strategy each when evaluating/ranking
        n_strategies = {}
        for strategy in self.strategies:
            if strategy.__class__ not in n_strategies:
                n_strategies[strategy.__class__] = []
            n_strategies[strategy.__class__].append(strategy)

        for strategy_list in n_strategies.values():
            for i, strategy in enumerate(strategy_list):
                strategy.appendName(f" ({i})")

        # Awarding points
        self.MAX: int = 5
        self.MC: int = 3
        self.MIN: int = 0
        self.MD: int = 1

        # Give game payoffs to class Strategy
        Strategy.setPayoffs(self.MAX, self.MIN, self.MC, self.MD)

        # Cooperate = True
        # Defect = False
        self.payoffs = [
            [tuple((self.MD, self.MD)), tuple((self.MIN, self.MAX))],
            [tuple((self.MAX, self.MIN)), tuple((self.MC, self.MC))]
        ]

    # Created by ChapGPT
    def award(self, x: float, y: float) -> tuple[float, float]:

        # Set x and y within range of 0 - 1
        x = max(0, min(x, 1))
        y = max(0, min(y, 1))

        """
        Bilinear interpolation of a 2x2 matrix where each element is a tuple (a, b).
        Returns an interpolated tuple (a_interp, b_interp).
        """
        def lerp2(a00: int, a01: int, a10: int, a11: int) -> float:
            return (
                a00 * (1 - x) * (1 - y) +
                a01 * x * (1 - y) +
                a10 * (1 - x) * y +
                a11 * x * y
            )
        
        # Extract the four tuples
        (a00, b00), (a01, b01) = self.payoffs[0]
        (a10, b10), (a11, b11) = self.payoffs[1]

        a_interp: float = lerp2(a00, a01, a10, a11)
        b_interp: float = lerp2(b00, b01, b10, b11)

        return (a_interp, b_interp)
