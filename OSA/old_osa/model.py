

# class called OSAmodel to hold all the OSA variables
class OSAmodel:
    # init function to initialize all the variables
    def __init__(self):
        self.current_trace = 'A'
        self.start = '350'
        self.stop = '1700'
        self.scale = 'LOG'
        self.averages = '1'

    # get setters without the @property notation 
    def get_current_trace(self):
        return self.current_trace
    
    def get_start(self):
        return self.start
    
    def get_stop(self):
        return self.stop
    
    def get_scale(self):
        return self.scale
    
    def get_averages(self):
        return self.averages
    
    # setters
    def set_current_trace(self, current_trace):
        self.current_trace = current_trace

    def set_start(self, start):
        self.start = start

    def set_stop(self, stop):
        self.stop = stop

    def set_scale(self, scale):
        self.scale = scale

    def set_averages(self, averages):
        self.averages = averages

    
