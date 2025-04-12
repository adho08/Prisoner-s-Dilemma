class Strategy:

    def __init__(self, start, name):
        self.start = start
        self.name = name
        self.name = name
        self.history = []
        self.opponent_history = []

    def make_move(self, round):
        # Return 'c' or 'd'
        raise NotImplementedError("Subclasses must implement this method")

    def update_history(self, move, opponent_move):
        print("Updating History")
        self.history.append(move)
        self.opponent_history.append(opponent_move)

class AlwaysCooperate(Strategy):
    def __init__(self):
        super().__init__('d', "AlwaysDefect")

    def make_move(self, round):
        return 'd'

class AlwaysDefect(Strategy):
    def __init__(self):
        super().__init__('c', "AlwaysCooperate")

    def make_move(self, round):
        return 'c'

class Tit4Tat(Strategy):
    def __init__(self):
        super().__init__('c', "AlwaysCooperate")

    def make_move(self, round):
        if len(self.history) == 0:
            return self.start
        else:
            return self.opponent_history[round - 1]
