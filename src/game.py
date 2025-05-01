from strategies import Strategy

class CPDVector1D:

    def __init__(self, c: float = 0, d: float = 0):
        self.c = self._clamp(c)
        self.d = self._clamp(d)

    # ensure the components c and d are between 0 and 1
    def _clamp(self, value: float) -> float:
        return max(0.0, min(1.0, value))


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

    def award(self, move1: CPDVector1D, move2: CPDVector1D) -> tuple[int, int]:
        
        return (1, 1)
