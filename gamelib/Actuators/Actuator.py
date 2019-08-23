from gamelib.Constants import PAUSED,RUNNING,STOPPED

class Actuator():
    def __init__(self):
        self.type = None
        self.state = RUNNING
    
    def start(self):
        """Set the actuator state to RUNNING.

        If the actuator state is not RUNNING, actuators' next_move() function (and all derivatives) should not return anything.

        Example::
        
            mygame.start()
        """
        self.state = RUNNING
    
    def pause(self):
        """Set the actuator state to PAUSED.

        Example::
        
            mygame.pause()
        """
        self.state = PAUSED
    
    def stop(self):
        """Set the actuator state to STOPPED.
        
        Example::
        
            mygame.stop()
        """
        self.state = STOPPED

    def next_move(self):
        raise NotImplementedError()


class Behavioral(Actuator):
    def __init__(self):
        Actuator.__init__(self)
    
    def next_action(self):
        raise NotImplementedError()
