class Strategy:

    def __init__(self, name):
        self.name = name

    def make_move(self):
        # Return True for 'c' or False for 'd'
        raise NotImplementedError("Subclasses must implement this method")

class Cooperate(Strategy):
    def __init__(self):
        super().__init__("Cooperate")

    def make_move(self):
        return True

class Defect(Strategy):
    def __init__(self):
        super().__init__("Defect")

    def make_move(self):
        return False
