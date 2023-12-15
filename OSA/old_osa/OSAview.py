#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput
import os 
import time
from controller import OSAcontroller


class ANDO_OSA:
    def __init__(self, osa_controller,  master=None):
        
        # build ui
        self.frame11 = ttk.Frame(master)
        self.frame11.configure(height=400, width=800)
        self.spectrum_canvas = tk.Canvas(self.frame11)
        self.spectrum_canvas.configure(
            background="#ffffff", height=500, width=600)
        self.spectrum_canvas.grid(column=0, padx=5, pady=5, row=0)
        
        self.settings_frame = ttk.Frame(self.frame11)
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
        self.center_entry = ttk.Entry(self.wl_frame)
        self.center_entry.grid(column=2, padx="5 0", pady=5, row=1)
        self.span_label = ttk.Label(self.wl_frame)
        self.span_label.configure(text='Span')
        self.span_label.grid(column=3, padx=5, row=0)
        self.span_entry = ttk.Entry(self.wl_frame)
        self.span_entry.grid(column=3, padx=5, row=1)
        self.wl_frame.grid(column=0, pady=5, row=0)
        
        
        self.trace_frame = ttk.Frame(self.settings_frame)
        self.trace_frame.configure(height=200, relief="raised", width=200)
        self.trace_A = ttk.Button(self.trace_frame)
        self.trace_A.configure(text='Trace A')
        self.trace_A.grid(column=1, padx=5, row=1)
        self.trace_B = ttk.Button(self.trace_frame)
        self.trace_B.configure(text='Trace B')
        self.trace_B.grid(column=2, padx=5, row=1)
        self.trace_C = ttk.Button(self.trace_frame)
        self.trace_C.configure(text='Trace C')
        self.trace_C.grid(column=3, padx=5, row=1)


        self.update_button = ttk.Button(self.trace_frame)
        self.update_button.configure(text='Update')
        self.update_button.grid(column=1, pady=5, row=2)
        self.hold_button = ttk.Button(self.trace_frame)
        self.hold_button.configure(text='Hold')
        self.hold_button.grid(column=2, row=2)
        self.display_button = ttk.Button(self.trace_frame)
        self.display_button.configure(text='Display')
        self.display_button.grid(column=3, row=2)
                                 
        self.stop_button = ttk.Button(self.trace_frame)
        self.stop_button.configure(text='Stop')
        self.stop_button.grid(column=1, pady=5, row=0)
        self.stop_button.config(state=tk.DISABLED)
        self.single_button = ttk.Button(self.trace_frame)
        self.single_button.configure(text='Single')
        self.single_button.grid(column=2, pady=5, row=0)
        self.auto_button = ttk.Button(self.trace_frame)
        self.auto_button.configure(text='Auto')
        self.auto_button.grid(column=3, pady=5, row=0)
        self.trace_frame.grid(column=0, pady=5, row=2)
        
        
        self.log_frame = ttk.Frame(self.settings_frame)
        self.log_frame.configure(height=200, relief="raised", width=200)
        # make text-field called log_window with a scrollbar to the right to scroll in the log 
        self.log_window = tk.Text(self.log_frame)
        self.log_window.configure(height=10, width=50)
        self.log_window.grid(column=0, padx=5, pady="0 5", row=1)
        self.log_label = ttk.Label(self.log_frame)
        self.log_label.configure(text='Status: Not connected.')
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
        self.save_frame.grid(column=0, pady=5, row=4)
        
        
        self.settings = ttk.Frame(self.settings_frame)
        self.settings.configure(height=200, relief="raised", width=200)
        self.averages_label = ttk.Label(self.settings)
        self.averages_label.configure(text='Averages :')
        self.averages_label.grid(column=0, padx=5, pady=5, row=0)
        self.averages_entry = ttk.Entry(self.settings)
        self.averages_entry.grid(column=1, padx=5, pady=5, row=0)
        #self.averages_entry.configure(validatecommand=self.update_averages_number)
        self.resolution_label = ttk.Label(self.settings)
        self.resolution_label.configure(text='Resolution :')
        self.resolution_label.grid(column=2, padx=5, row=0)
        self.__tkvar = tk.StringVar(value=0.05)
        self.__values = ['0.05', ' 0.1', ' 0.2', ' 0.5', ' 1', ' 2', ' 5', ' 10']
        #self.resolution_option = ttk.OptionMenu(self.settings, __tkvar, 0.05, *self.__values, command=self.resolution_changed)
        self.resolution_option = ttk.OptionMenu(self.settings, self.__tkvar, 0.05, *self.__values, command = osa_controller.resolution_changed)
        self.resolution_option.grid(column=4, padx=5, pady=5, row=0)
        self.scale_button = ttk.Button(self.settings)
        self.scale_button.configure(text='LOG')
        self.scale_button.grid(column=5, padx=5, row=0)
        self.settings.grid(column=0, padx=5, pady=5, row=1)
        self.settings_frame.grid(column=1, row=0)
        self.frame11.pack(expand=False)

        #self.set_init_values()

        # Main widget
        

        # Main widget
        self.mainwindow = self.frame11
        master.iconphoto(True, tk.PhotoImage(file="troive_icon.png"))
        


    def run(self):
        self.mainwindow.mainloop()

    def write_to_log(self, message):
        self.log_window.insert(tk.END, time.strftime("%H:%M:%S", time.localtime()) + " " + message + "\n")
        self.log_window.see(tk.END)

    def change_resolution_menu(self, option):
        self.__tkvar.set(option)