#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput
import os 
import time


class ANDO_OSA:
    def __init__(self, master=None):
        
        # build ui
        frame11 = ttk.Frame(master)
        frame11.configure(height=400, width=800)
        self.spectrum_canvas = tk.Canvas(frame11)
        self.spectrum_canvas.configure(
            background="#ffffff", height=500, width=600)
        self.spectrum_canvas.grid(column=0, padx=5, pady=5, row=0)
        
        self.settings_frame = ttk.Frame(frame11)
        self.settings_frame.configure(height=200, relief="raised", width=200)
        self.wl_frame = ttk.Frame(self.settings_frame)
        self.wl_frame.configure(height=200, relief="raised", width=200)
        self.start_label = ttk.Label(self.wl_frame)
        self.start_label.configure(padding=2, text='Start')
        self.start_label.grid(column=0, pady=5, row=0)
        self.stop_label = ttk.Label(self.wl_frame)
        self.stop_label.configure(padding=2, text='Stop')
        self.stop_label.grid(column=1, pady=5, row=0)
        self.center_label = ttk.Label(self.wl_frame)
        self.center_label.configure(padding=2, text='Center')
        self.center_label.grid(column=2, pady=5, row=0)
        self.start_entry = ttk.Entry(self.wl_frame)
        self.start_entry.grid(column=0, padx=5, pady=5, row=1)
        self.stop_entry = ttk.Entry(self.wl_frame)
        self.stop_entry.grid(column=1, pady=5, row=1)
        self.stop_entry.bind("<Return>", self.update_stop)
        self.stop_entry.bind("<FocusOut>", self.update_stop)
        self.center_entry = ttk.Entry(self.wl_frame)
        self.center_entry.grid(column=2, padx="5 0", pady=5, row=1)
        self.center_entry.bind("<Return>", self.update_center)
        self.center_entry.bind("<FocusOut>", self.update_center)
        self.span_label = ttk.Label(self.wl_frame)
        self.span_label.configure(text='Span')
        self.span_label.grid(column=3, padx=5, row=0)
        self.span_entry = ttk.Entry(self.wl_frame)
        self.span_entry.grid(column=3, padx=5, row=1)
        self.span_entry.bind("<Return>", self.update_span)
        self.span_entry.bind("<FocusOut>", self.update_span)
        self.wl_frame.grid(column=0, pady=5, row=0)
        
        
        self.trace_frame = ttk.Frame(self.settings_frame)
        self.trace_frame.configure(height=200, relief="raised", width=200)
        self.trace_A = ttk.Button(self.trace_frame)
        self.trace_A.configure(text='Trace A')
        self.trace_A.grid(column=0, padx=5, row=1)
        self.trace_B = ttk.Button(self.trace_frame)
        self.trace_B.configure(text='Trace B')
        self.trace_B.grid(column=1, padx=5, row=1)
        self.trace_C = ttk.Button(self.trace_frame)
        self.trace_C.configure(text='Trace C')
        self.trace_C.grid(column=2, padx=5, row=1)
        self.trace_D = ttk.Button(self.trace_frame)
        self.trace_D.configure(text='Trace D')
        self.trace_D.grid(column=3, padx=5, row=1)
        self.trace_E = ttk.Button(self.trace_frame)
        self.trace_E.configure(text='Trace E')
        self.trace_E.grid(column=4, padx=5, row=1)
        self.trace_A.configure(command=self.update_chosen_trace)
        self.trace_B.configure(command=self.update_chosen_trace)
        self.trace_C.configure(command=self.update_chosen_trace)
        self.trace_D.configure(command=self.update_chosen_trace)
        self.trace_E.configure(command=self.update_chosen_trace)
        
        self.update_button = ttk.Button(self.trace_frame)
        self.update_button.configure(text='Update')
        self.update_button.grid(column=1, pady=5, row=2)
        self.hold_button = ttk.Button(self.trace_frame)
        self.hold_button.configure(text='Hold')
        self.hold_button.grid(column=2, row=2)
        self.display_button = ttk.Button(self.trace_frame)
        self.display_button.configure(text='Display')
        self.display_button.grid(column=3, row=2)
        self.stop_indicator = ttk.Checkbutton(self.trace_frame)
        self.stop_indicator.configure(text='Stop')
        self.stop_indicator.grid(column=1, pady=5, row=0)
        self.stop_indicator.configure(command=self.stop_measurement)
        self.single_indicator = ttk.Checkbutton(self.trace_frame)
        self.single_indicator.configure(text='Single')
        self.single_indicator.grid(column=2, pady=5, row=0)
        self.single_indicator.configure(
            command=self.perform_single_measurement)
        self.auto_indicator = ttk.Checkbutton(self.trace_frame)
        self.auto_indicator.configure(text='Auto')
        self.auto_indicator.grid(column=3, pady=5, row=0)
        self.auto_indicator.configure(command=self.start_auto_measurement)
        self.trace_frame.grid(column=0, pady=5, row=2)
        
        
        self.log_frame = ttk.Frame(self.settings_frame)
        self.log_frame.configure(height=200, relief="raised", width=200)
        self.log_window = tk.Text(self.log_frame)
        self.log_window.configure(height=10, width=50)
        self.log_window.grid(column=0, padx=5, pady="0 5", row=1)
        self.log_label = ttk.Label(self.log_frame)
        self.log_label.configure(text='Log:')
        self.log_label.grid(column=0, padx=5, pady="5 0", row=0, sticky="w")
        self.log_frame.grid(column=0, padx=5, pady=5, row=3)
        
        
        self.save_frame = ttk.Frame(self.settings_frame)
        self.save_frame.configure(height=200, relief="raised", width=200)
        self.save_label = ttk.Label(self.save_frame)
        self.save_label.configure(text='Save directory :')
        self.save_label.grid(column=0, padx=5, row=0)
        self.save_dir_chooser = PathChooserInput(self.save_frame)
        self.save_dir_chooser.configure(mustexist=True, type="directory")
        self.save_dir_chooser.grid(column=1, padx=5, row=0)
        self.save_measurement_button = ttk.Button(self.save_frame)
        self.save_measurement_button.configure(text='Save measurement')
        self.save_measurement_button.grid(column=2, padx=5, pady=5, row=0)
        self.save_measurement_button.configure(command=self.save_measurement)
        self.save_frame.grid(column=0, pady=5, row=4)
        
        
        self.settings = ttk.Frame(self.settings_frame)
        self.settings.configure(height=200, relief="raised", width=200)
        self.averages_label = ttk.Label(self.settings)
        self.averages_label.configure(text='Averages :')
        self.averages_label.grid(column=0, padx=5, pady=5, row=0)
        self.averages_entry = ttk.Entry(self.settings)
        self.averages_entry.grid(column=1, padx=5, pady=5, row=0)
        self.averages_entry.configure(
            validatecommand=self.update_averages_number)
        self.resolution_label = ttk.Label(self.settings)
        self.resolution_label.configure(text='Resolution :')
        self.resolution_label.grid(column=2, padx=5, row=0)
        __tkvar = tk.StringVar(value=0.05)
        self.__values = ['0.05', ' 0.1', ' 0.2', ' 0.5', ' 1', ' 2', ' 5', ' 10']
        self.resolution_option = ttk.OptionMenu(
            self.settings, __tkvar, 0.05, *self.__values, command=self.resolution_changed)
        self.resolution_option.grid(column=4, padx=5, pady=5, row=0)
        self.scale_button = ttk.Button(self.settings)
        self.scale_button.configure(text='LOG', command=self.scale_changed)
        self.scale_button.grid(column=5, padx=5, row=0)
        self.settings.grid(column=0, padx=5, pady=5, row=1)
        self.settings_frame.grid(column=1, row=0)
        frame11.pack(expand=False)

        #self.set_init_values()

        # Main widget
        self.write_to_log("GUI initialized")

        # Main widget
        self.mainwindow = frame11

    # def set_init_values(self):
    #     self.start_entry.insert(0, "350")
    #     self.stop_entry.insert(0, "1750")
    #     self.update_center_entry()
    #     self.update_span_entry()
    #     self.averages_entry.insert(0, "1")
    #     self.resolution = self.__values[0]
    #     self.scale = "LOG"
    #     self.update_chosen_trace(self.trace_A)
    #     self.write_to_log("Initial values set")

    def run(self):
        self.mainwindow.mainloop()

    def update_start(self, event):
        start_wl = str(self.start_entry.get())
        self.write_to_log("Start wavelength set to " + start_wl + " nm.")
        self.update_center_entry()
        self.update_span_entry()

    def update_stop(self, event):
        stop_wl = str(self.stop_entry.get())
        self.write_to_log("Stop wavelength set to " + stop_wl + " nm.")
        self.update_center_entry()
        self.update_span_entry()

    def update_center_entry(self):
        start_wl = self.start_entry.get()
        stop_wl = self.stop_entry.get()
        if start_wl == "" or stop_wl == "":
            return
        else:
            start_wl = float(start_wl)
            stop_wl = float(stop_wl)
        center_wl = (start_wl + stop_wl) / 2
        self.center_entry.delete(0, tk.END)
        self.center_entry.insert(0, str(center_wl))

    def update_center(self, event):
        span = float(self.span_entry.get())
        center_wl = float(self.center_entry.get())
        if span == "" or center_wl == "":
            return
        start_wl = center_wl - span / 2
        stop_wl = center_wl + span / 2
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, str(start_wl))
        self.stop_entry.delete(0, tk.END)
        self.stop_entry.insert(0, str(stop_wl))
        self.write_to_log("Center wavelength set to " + str(center_wl) + " nm.")

    def update_span(self, event):
        span = float(self.span_entry.get())
        center_wl = float(self.center_entry.get())
        if span == "" or center_wl == "":
            return
        start_wl = center_wl - span / 2
        stop_wl = center_wl + span / 2
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, str(start_wl))
        self.stop_entry.delete(0, tk.END)
        self.stop_entry.insert(0, str(stop_wl))
        self.write_to_log("Span set to " + str(span) + " nm.")

    def update_span_entry(self):
        start = float(self.start_entry.get())
        stop = float(self.stop_entry.get())
        span = stop - start
        self.span_entry.delete(0, tk.END)
        self.span_entry.insert(0, str(span))

    def resolution_changed(self, event):
        self.resolution = event
        self.write_to_log("Resolution set to " + event + " nm.")

    def scale_changed(self):
        if self.scale == "LOG":
            self.scale = "LIN"
            self.scale_button.configure(text='LIN')
        else:
            self.scale = "LOG"
            self.scale_button.configure(text='LOG')
        self.write_to_log("Scale set to " + self.scale + ".")

    def update_chosen_trace(self, button):
        # button is 'A', 'B', 'C', 'D' or 'E', disable this button and enable the rest. print a suitable print to the log 

        if button == 'A':
            self.trace_A.configure(state='disabled')
            self.trace_B.configure(state='normal')
            self.trace_C.configure(state='normal')
            self.trace_D.configure(state='normal')
            self.trace_E.configure(state='normal')
            self.write_to_log("Trace A chosen.")
        elif button == 'B':
            self.trace_A.configure(state='normal')
            self.trace_B.configure(state='disabled')
            self.trace_C.configure(state='normal')
            self.trace_D.configure(state='normal')
            self.trace_E.configure(state='normal')
            self.write_to_log("Trace B chosen.")
        elif button == 'C':
            self.trace_A.configure(state='normal')
            self.trace_B.configure(state='normal')
            self.trace_C.configure(state='disabled')
            self.trace_D.configure(state='normal')
            self.trace_E.configure(state='normal')
            self.write_to_log("Trace C chosen.")
        elif button == 'D':
            self.trace_A.configure(state='normal')
            self.trace_B.configure(state='normal')
            self.trace_C.configure(state='normal')
            self.trace_D.configure(state='disabled')
            self.trace_E.configure(state='normal')
            self.write_to_log("Trace D chosen.")
        elif button == 'E':
            self.trace_A.configure(state='normal')
            self.trace_B.configure(state='normal')
            self.trace_C.configure(state='normal')
            self.trace_D.configure(state='normal')
            self.trace_E.configure(state='disabled')
            self.write_to_log("Trace E chosen.")

    def stop_measurement(self):
        pass

    def perform_single_measurement(self):
        pass

    def start_auto_measurement(self):
        pass

    def save_measurement(self):
        pass

    def update_averages_number(self):
        pass

    def write_to_log(self, message):
        # current time
        ct = time.localtime()
        # write to log
        self.log_window.insert(tk.END, time.strftime("%H:%M:%S", ct) + " " + message + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = ANDO_OSA(root)
    app.run()