from gamelib.Constants import ACT_PAUSED,ACT_RUNNING,ACT_STOPPED

class Actuator():
    def __init__(self):
        self.type = None
        self.state = ACT_RUNNING
    
    def start(self):
        self.state = ACT_RUNNING
    
    def pause(self):
        self.state = ACT_PAUSED
    
    def stop(self):
        self.state = ACT_STOPPED

    def next_move(self):
        raise NotImplementedError()


class Behavioral(Actuator):
    def __init__(self):
        Actuator.__init__(self)
    
    def next_action(self):
        raise NotImplementedError()
