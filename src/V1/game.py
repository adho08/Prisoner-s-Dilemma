class PrisonersDilemma:

    def __init__(self, strategy1, strategy2):
        self.strategy1 = strategy1
        self.strategy2 = strategy2

        # awarding points
        self.MAX = 5
        self.MIN = 0
        self.MC = 3
        self.MD = 1

    def award(self, s1, s2):
        # cooperate = 1
        # defect = 0

        p1 = 0
        p2 = 0

        # PD Matrix evaluation
        if not s1 and s2: 
            # s1 defects
            # s2 cooperates
            p1 = self.MAX
            p2 = self.MIN
            
        if s1 and not s2:
            # s1 cooperates
            # s2 defects
            p2 = self.MAX
            p1 = self.MIN
            
        if s1 and s2:
            # s1 cooperates
            # s2 cooperates
            p1 = self.MC
            p2 = self.MC

        if not(s1 and s2):
            # s1 defects
            # s2 defects
            p1 = self.MD
            p2 = self.MD

        return (p1, p2)
