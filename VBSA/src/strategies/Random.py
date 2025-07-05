from strategies import Strategy, PBStrategy

class Random(PBStrategy):
    def __init__(self, parameter: int = 1, start = None, name: str | None = None):
        super().__init__(parameter, start, name)

    def make_move(self, round: int = 0):
        return 1.0 if np.random.choice([True, False], p=[1 - self.parameter/10, self.parameter/10]) else 0.0
