
class Actuator():
    def __init__(self):
        self.type = None

    def next_move(self):
        raise NotImplementedError()