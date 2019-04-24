
class Actuator():
    def __init__(self):
        self.type = None

    def next_move(self):
        raise NotImplementedError()


class Behavioral(Actuator):
    def __init__(self):
        Actuator.__init__(self)
    
    def next_action(self):
        raise NotImplementedError()
