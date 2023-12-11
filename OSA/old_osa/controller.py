import OSAview
from model import OSAmodel
import tkinter as tk

# controller class for the model-view-controller design pattern of the OSA program
class OSAcontroller:

    # init function to initialize all the variables
    def __init__(self):
        self.model = OSAmodel()
        self.view = OSAview.ANDO_OSA(tk.Tk())
        self.set_init_values()

        # bind the buttons to the functions
        self.view.start_entry.bind("<Return>", self.start_changed)
        self.view.start_entry.bind("<FocusOut>", self.start_changed)

        self.view.run()

    def set_init_values(self):
        self.view.update_chosen_trace(self.model.get_current_trace())
        self.view.start_entry.insert(0, self.model.get_start())
        self.view.stop_entry.insert(0, self.model.get_stop())
        self.view.scale_button.configure(text=self.model.get_scale())
        self.view.averages_entry.insert(0, self.model.get_averages())

    # setters for the parameters in the model
    def set_current_trace(self, current_trace):
        self.model.set_current_trace(current_trace)

    def set_start(self, start):
        self.model.set_start(start)

    def set_stop(self, stop):
        self.model.set_stop(stop)

    def set_scale(self, scale):
        self.model.set_scale(scale)

    def set_averages(self, averages):
        self.model.set_averages(averages)

    # getters for the parameters in the model
    def get_current_trace(self):
        return self.model.get_current_trace()
    
    def get_start(self):
        return self.model.get_start()

    def get_stop(self):
        return self.model.get_stop()
    
    def get_scale(self):
        return self.model.get_scale()
    
    def get_averages(self):
        return self.model.get_averages()
    
    # The user changed the start-values and thus the model needs to be updated and then the view, based on the values in the model
    def start_changed(self, event):
        self.set_start(self.view.start_entry.get())
        self.view.write_to_log("Start wavelength set to " + self.model.get_start + " nm.")
        self.update_center_entry()
        self.update_span_entry()