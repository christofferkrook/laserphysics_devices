import os

# class called OSAmodel to hold all the OSA variables
class OSAmodel:
    # init function to initialize all the variables
    def __init__(self):
        self.current_trace = 'A'
        self.start = '350'
        self.stop = '1700'
        self.scale = 'LOG'
        self.averages = '1'
        self.center = str((float(self.start) + float(self.stop)) / 2)
        self.span = str(float(self.stop) - float(self.start))
        self.resolution = '0.05'
        self.measurement_state = "STOP"
        self.trace_state = "HOLD"
        self.trace_display_state = False
        self.connected = False
        self.save_dir = os.getcwd()+"/data"
        self.save_a = False
        self.save_b = False
        self.save_c = False

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
    
    def get_center(self):
        return self.center
    
    def get_span(self):
        return self.span
    
    def get_resolution(self):
        return self.resolution
    
    def get_measurement_state(self):
        return self.measurement_state
    
    def get_trace_state(self):
        return self.trace_state
    
    def get_connected(self):
        return self.connected
    
    def get_trace_display_state(self):
        return self.trace_display_state
    
    def get_save_dir(self):
        return self.save_dir
    
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

    def set_center(self, center):
        self.center = center

    def set_span(self, span):
        self.span = span
        
    def set_resolution(self, resolution):
        self.resolution = resolution

    def set_measurement_state(self, measurement_state):
        self.measurement_state = measurement_state

    def set_trace_state(self, trace_state):
        self.trace_state = trace_state

    def set_connected(self, connected):
        self.connected = connected

    def set_trace_display_state(self, trace_display_state):
        self.trace_display_state = trace_display_state

    def set_save_dir(self, save_dir):
        self.save_dir = save_dir