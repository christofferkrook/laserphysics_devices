import OSAview
from model import OSAmodel
import tkinter as tk

# controller class for the model-view-controller design pattern of the OSA program
class OSAcontroller:

    # init function to initialize all the variables
    def __init__(self):
        self.model = OSAmodel()
        self.view = OSAview.ANDO_OSA(self, tk.Tk())
        self.set_init_values()

        # bind the wavelength fields
        self.view.start_entry.bind("<Return>", self.start_changed)
        self.view.stop_entry.bind("<Return>", self.stop_changed)
        self.view.center_entry.bind("<Return>", self.update_center)
        self.view.span_entry.bind("<Return>", self.update_span)

        # bind the trace-buttons
        self.view.trace_A.bind("<Button-1>", lambda event: self.set_current_trace('A'))
        self.view.trace_B.bind("<Button-1>", lambda event: self.set_current_trace('B'))
        self.view.trace_C.bind("<Button-1>", lambda event: self.set_current_trace('C'))
        self.view.trace_D.bind("<Button-1>", lambda event: self.set_current_trace('D'))
        self.view.trace_E.bind("<Button-1>", lambda event: self.set_current_trace('E'))

        # scale button
        self.view.scale_button.bind("<Button-1>", lambda event: self.switch_scale())

        # averages-field
        self.view.averages_entry.bind("<Return>", self.resolution_changed)

        # run change_measurement_state function when one of the three buttons are pressed, also pass the function which button was pressed
        self.view.auto_button.bind("<Button-1>", lambda event: self.change_measurement_state('auto'))
        self.view.stop_button.bind("<Button-1>", lambda event: self.change_measurement_state('stop'))
        self.view.single_button.bind("<Button-1>", lambda event: self.change_measurement_state('single'))

        # update hold and display buttons should run change_trace_state function
        self.view.update_button.bind("<Button-1>", lambda event: self.change_trace_state('update'))
        self.view.hold_button.bind("<Button-1>", lambda event: self.change_trace_state('hold'))
        self.view.display_button.bind("<Button-1>", lambda event: self.change_trace_state('display'))



        self.view.run()

    def set_init_values(self):
        self.view.trace_A.config(state=tk.DISABLED)
        self.view.start_entry.insert(0, self.model.get_start())
        self.view.stop_entry.insert(0, self.model.get_stop())
        self.view.scale_button.configure(text=self.model.get_scale())
        self.view.averages_entry.insert(0, self.model.get_averages())
        self.update_center_entry()
        self.update_span_entry()
        self.view.write_to_log("Program started. Initialization complete.")


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

    def set_center(self, center):
        self.model.set_center(center)

    def set_span(self, span):
        self.model.set_span(span)

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
    
    def get_center(self):
        return self.model.get_center()
    
    def get_span(self):
        return self.model.get_span()
    
    # The user changed the start-values and thus the model needs to be updated and then the view, based on the values in the model
    def start_changed(self, event):
        self.set_start(self.view.start_entry.get())
        self.view.write_to_log("Start wavelength set to " + self.model.get_start() + " nm.")
        self.update_center_entry()
        self.update_span_entry()

    def update_stop_entry(self):
        self.view.stop_entry.delete(0, tk.END)
        self.view.stop_entry.insert(0, str(float(self.model.get_start()) + float(self.model.get_span())))

    def update_start_entry(self):
        self.view.start_entry.delete(0, tk.END)
        self.view.start_entry.insert(0, str(float(self.model.get_center()) - float(self.model.get_span()) / 2))


    # The user changed the stop-values and thus the model needs to be updated and then the view, based on the values in the model
    def stop_changed(self, event):
        self.set_stop(self.view.stop_entry.get())
        self.view.write_to_log("Stop wavelength set to " + self.model.get_stop() + " nm.")
        self.update_center_entry()
        self.update_span_entry()

    def update_center_entry(self):
        self.view.center_entry.delete(0, tk.END)
        new_center = str((float(self.model.get_start()) + float(self.model.get_stop())) / 2)
        self.view.center_entry.insert(0, new_center)
        self.model.set_center(new_center)

    def update_center(self):
        self.set_center(self.view.center_entry.get())
        self.view.write_to_log("Center wavelength set to " + self.model.get_center() + " nm.")
        self.update_start_entry()
        self.update_stop_entry()
        self.update_span_entry()

    def update_span_entry(self):
        self.view.span_entry.delete(0, tk.END)
        new_span = str(float(self.model.get_stop()) - float(self.model.get_start()))
        self.view.span_entry.insert(0, new_span)
        self.model.set_span(new_span)

    def update_span(self):
        self.set_span(self.view.span_entry.get())
        self.view.write_to_log("Span wavelength set to " + self.model.get_span() + " nm.")
        self.update_start_entry()
        self.update_stop_entry()
        self.update_center_entry()

    def set_current_trace(self, current_trace):
        print("button pressed")
        self.model.set_current_trace(current_trace)

        # check which is the current button, disable that one, and enable all the others
        if self.model.get_current_trace() == 'A':
            self.view.trace_A.config(state=tk.DISABLED)
            self.view.trace_B.config(state=tk.NORMAL)
            self.view.trace_C.config(state=tk.NORMAL)
            self.view.trace_D.config(state=tk.NORMAL)
            self.view.trace_E.config(state=tk.NORMAL)
        elif self.model.get_current_trace() == 'B':
            self.view.trace_A.config(state=tk.NORMAL)
            self.view.trace_B.config(state=tk.DISABLED)
            self.view.trace_C.config(state=tk.NORMAL)
            self.view.trace_D.config(state=tk.NORMAL)
            self.view.trace_E.config(state=tk.NORMAL)
        elif self.model.get_current_trace() == 'C':
            self.view.trace_A.config(state=tk.NORMAL)
            self.view.trace_B.config(state=tk.NORMAL)
            self.view.trace_C.config(state=tk.DISABLED)
            self.view.trace_D.config(state=tk.NORMAL)
            self.view.trace_E.config(state=tk.NORMAL)
        elif self.model.get_current_trace() == 'D':
            self.view.trace_A.config(state=tk.NORMAL)
            self.view.trace_B.config(state=tk.NORMAL)
            self.view.trace_C.config(state=tk.NORMAL)
            self.view.trace_D.config(state=tk.DISABLED)
            self.view.trace_E.config(state=tk.NORMAL)
        elif self.model.get_current_trace() == 'E':
            self.view.trace_A.config(state=tk.NORMAL)
            self.view.trace_B.config(state=tk.NORMAL)
            self.view.trace_C.config(state=tk.NORMAL)
            self.view.trace_D.config(state=tk.NORMAL)
            self.view.trace_E.config(state=tk.DISABLED)

        # write to log 
        self.view.write_to_log("Current trace set to " + self.model.get_current_trace() + ".")

    def switch_scale(self):
        if self.model.get_scale() == 'LOG':
            self.model.set_scale('LIN')
            self.view.scale_button.configure(text=self.model.get_scale())
            self.view.write_to_log("Scale set to " + self.model.get_scale() + ".")
        elif self.model.get_scale() == 'LIN':
            self.model.set_scale('LOG')
            self.view.scale_button.configure(text=self.model.get_scale())
            self.view.write_to_log("Scale set to " + self.model.get_scale() + ".")

    def resolution_changed(self, event):
        self.model.set_resolution(event)
        self.view.write_to_log("Resolution set to " + self.model.get_resolution() + ".")

    def resolution_changed(self, event):
        self.model.set_resolution(self.view.averages_entry.get())
        self.view.write_to_log("Resolution set to " + self.model.get_resolution() + ".")

    def change_measurement_state(self, button):
        # change value in the model
        if button == 'stop':
            self.model.measurement_state = 'STOP'
        elif button == 'single':
            self.model.measurement_state = 'SINGLE'
        elif button == 'auto':
            self.model.measurement_state = 'AUTO'
        
        # disable the chosen measurement_state_button and enable all the others
        if self.model.measurement_state == 'STOP':
            self.view.stop_button.config(state=tk.DISABLED)
            self.view.single_button.config(state=tk.NORMAL)
            self.view.auto_button.config(state=tk.NORMAL)
        elif self.model.measurement_state == 'SINGLE':
            self.view.stop_button.config(state=tk.NORMAL)
            self.view.single_button.config(state=tk.DISABLED)
            self.view.auto_button.config(state=tk.NORMAL)
        elif self.model.measurement_state == 'AUTO':
            self.view.stop_button.config(state=tk.NORMAL)
            self.view.single_button.config(state=tk.NORMAL)
            self.view.auto_button.config(state=tk.DISABLED)

        # write to log
        self.view.write_to_log("Measurement state set to " + self.model.measurement_state + ".")

    def change_trace_state(self, button):
        # change value in the model
        if button == 'update':
            self.model.trace_state = 'UPDATE'
        elif button == 'hold':
            self.model.trace_state = 'HOLD'
        elif button == 'display':
            self.model.trace_state = 'DISPLAY'
        
        # disable the chosen trace_state_button and enable all the others
        if self.model.trace_state == 'UPDATE':
            self.view.update_button.config(state=tk.DISABLED)
            self.view.hold_button.config(state=tk.NORMAL)
            self.view.display_button.config(state=tk.NORMAL)
        elif self.model.trace_state == 'HOLD':
            self.view.update_button.config(state=tk.NORMAL)
            self.view.hold_button.config(state=tk.DISABLED)
            self.view.display_button.config(state=tk.NORMAL)
        elif self.model.trace_state == 'DISPLAY':
            self.view.update_button.config(state=tk.NORMAL)
            self.view.hold_button.config(state=tk.NORMAL)
            self.view.display_button.config(state=tk.DISABLED)

        # write to log
        self.view.write_to_log("Trace state set to " + self.model.trace_state + ".")