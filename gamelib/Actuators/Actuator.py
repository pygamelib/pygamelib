from gamelib.Constants import PAUSED,RUNNING,STOPPED

class Actuator():
    def __init__(self):
        self.type = None
        self.state = RUNNING
    
    def start(self):
        self.state = RUNNING
    
    def pause(self):
        self.state = PAUSED
    
    def stop(self):
        self.state = STOPPED

    def next_move(self):
        raise NotImplementedError()


class Behavioral(Actuator):
    def __init__(self):
        Actuator.__init__(self)
    
    def next_action(self):
        raise NotImplementedError()
