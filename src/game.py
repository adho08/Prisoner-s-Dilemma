from strategies import Strategy

class PrisonersDilemma:

    def __init__(self, strategies: list[Strategy]):
        # stored strategies in a list
        self.strategies: list[Strategy] = strategies

        # awarding points
        self.MAX: int = 5
        self.MC: int = 3
        self.MIN: int = 0
        self.MD: int = 1

        # Type alias
        Matrix2x2 = tuple[tuple[tuple[int, int], tuple[int, int]],
                  tuple[tuple[int, int], tuple[int, int]]]

        # cooperate = True
        # defect = False
        self.payoffs: Matrix2x2 = (  # Player 2 defects   Player 2 cooperates
                                    ((self.MD, self.MD), (self.MAX, self.MIN)),  # Player 1 defects
                                    ((self.MIN, self.MAX), (self.MC, self.MC))   # Player 1 cooperates
                                )

    def award(self, move1: bool, move2: bool) -> tuple[int, int]:
        return self.payoffs[move1][move2]
