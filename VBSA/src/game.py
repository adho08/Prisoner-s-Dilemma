from strategies import *
import random

class PrisonersDilemma(object):

<<<<<<< HEAD


    # ------------------ interpolated payoff matrix version ------------------ 
    # Awarding points
=======
    # awarding points
>>>>>>> 34aea383a68f348416b24a659b43105da0343277
    MAX: int = 5 
    MC: int = 3
    MIN: int = 0
    MD: int = 1

    # Cooperate = True
    # Defect = False
    payoffs = [
        [tuple((MD, MD)), tuple((MIN, MAX))],
        [tuple((MAX, MIN)), tuple((MC, MC))]
    ]

    # ------------------ algebraic version ------------------ 
    # cost-to-benefit ratio
    c = 0.5

    @staticmethod
    def make_distinctive(strategies: list[Strategy]) -> None:

        for strategy in strategies:
            # give game payoffs to class Strategy
            strategy.set_payoffs(PrisonersDilemma.MAX, PrisonersDilemma.MIN, PrisonersDilemma.MC, PrisonersDilemma.MD)

        # make names of strategies in list unique to be counted as one strategy each when evaluating/ranking
        n_strategies = {}
        for strategy in strategies:
            if strategy.__class__ not in n_strategies:
                n_strategies[strategy.__class__] = []
            n_strategies[strategy.__class__].append(strategy)

        for strategy_list in n_strategies.values():
            for i, strategy in enumerate(strategy_list):
                strategy.appendName(f" ({i})")

    # Created by ChapGPT
    @staticmethod
    def award_interpolated(x: float, y: float) -> tuple[float, float]:
        
        # if x and y are not between 0 and 1, raise an error
        if not (0 <= x <= 1) or not (0 <= y <= 1):
            raise ValueError("\nStrategies can only submit cooperation between 0 and 1", x if not (0 <= x <= 1) else y)
        
        noise = 0.2

        # set noise to deviate the actual amount of cooperation/defection
        noise_x = round(random.triangular(-noise, noise, 0.0), 2)
        noise_y = round(random.triangular(-noise, noise, 0.0), 2)

        # add noise (deviation of the actual amount of cooperation/defection)
        x_deviation = x + noise_x
        x = max(0.0, min(1.0, x_deviation))

        y_deviation = y + noise_y
        y = max(0.0, min(1.0, y_deviation))

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
        (a00, b00), (a01, b01) = PrisonersDilemma.payoffs[0]
        (a10, b10), (a11, b11) = PrisonersDilemma.payoffs[1]

        a_interp: float = round(lerp2(a00, a01, a10, a11), 2)
        b_interp: float = round(lerp2(b00, b01, b10, b11), 2)

        return (a_interp, b_interp)

    @classmethod
    def award_algebraic(cls, x: float, y: float) -> tuple[float, float]:

        v1 = x - cls.c*y
        v2 = y - cls.c*x

        return v1, v2
