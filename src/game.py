class PrisonersDilemma:

    def __init__(self, strategies):
        # stored strategies in a list
        self.strategies = strategies

        # awarding points
        self.MAX = 5
        self.MC = 3
        self.MIN = 0
        self.MD = 1

    def award(self, move1, move2):
        # cooperate = True
        # defect = False

        payoffs = ( # Player 2 defects    Player 2 cooperates
                    ((self.MD, self.MD), (self.MAX, self.MIN)),  # Player 1 defects
                    ((self.MIN, self.MAX), (self.MC, self.MC))   # Player 1 cooperates
                )

        return payoffs[move1][move2]
