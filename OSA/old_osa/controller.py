import OSAview
from model import OSAmodel
import tkinter as tk
import Ando
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from queue import Queue
from tkinter.filedialog import askdirectory
import os 
import csv


# controller class for the model-view-controller design pattern of the OSA program
class OSAcontroller:

    # init function to initialize all the variables
    def __init__(self):
        assert sum([1, 2, 3]) == 6, "Should be 6"
        self.model = OSAmodel()
        self.view = OSAview.ANDO_OSA(self, tk.Tk())
        
        # queue for talking between threads
        self.trace_queue = Queue()

        # bind the wavelength fields
        self.view.start_entry.bind("<Return>", self.start_changed)
        self.view.stop_entry.bind("<Return>", self.stop_changed)
        self.view.center_entry.bind("<Return>", self.update_center)
        self.view.span_entry.bind("<Return>", self.update_span)

        # bind the trace-buttons
        self.view.trace_A.bind("<Button-1>", lambda event: self.set_current_trace('A'))
        self.view.trace_B.bind("<Button-1>", lambda event: self.set_current_trace('B'))
        self.view.trace_C.bind("<Button-1>", lambda event: self.set_current_trace('C'))

        # scale button
        self.view.scale_button.bind("<Button-1>", lambda event: self.switch_scale())

        # averages-field
        self.view.averages_entry.bind("<Return>", self.averages_changed)

        # run change_measurement_state function when one of the three buttons are pressed, also pass the function which button was pressed
        self.view.auto_button.bind("<Button-1>", lambda event: self.change_measurement_state('auto'))
        self.view.stop_button.bind("<Button-1>", lambda event: self.change_measurement_state('stop'))
        self.view.single_button.bind("<Button-1>", lambda event: self.change_measurement_state('single'))

        # update hold and display buttons should run change_trace_state function
        self.view.update_button.bind("<Button-1>", lambda event: self.change_trace_state('update'))
        self.view.hold_button.bind("<Button-1>", lambda event: self.change_trace_state('hold'))
        self.view.display_button.bind("<Button-1>", lambda event: self.change_trace_display_state('display'))

        # bind save_measurement_button
        self.view.save_measurement_button.bind("<Button-1>", lambda event: self.save_measurement())

        # save buttons
        self.view.trace_a_save.bind("<Button-1>", lambda event: self.save_state_change('A'))
        self.view.trace_b_save.bind("<Button-1>", lambda event: self.save_state_change('B'))
        self.view.trace_c_save.bind("<Button-1>", lambda event: self.save_state_change('C'))

        self.view.write_to_log("GUI initialized")
        self.connect_osa()
        self.set_init_values()
        self.update_function()
        self.dequeue_traces()
        #self.test()
        self.view.run()


    def test(self):
        # test current traces
        self.set_current_trace('A')
        assert self.model.get_current_trace() == 'A' and self.OSA.get_current_trace() == 'A', "Trace A assertion failed"
        self.set_current_trace('B')
        assert self.model.get_current_trace() == 'B' and self.OSA.get_current_trace() == 'B', "Trace B assertion failed"
        self.set_current_trace('C')
        assert self.model.get_current_trace() == 'C' and self.OSA.get_current_trace() == 'C', "Trace C assertion failed"

        print("---------- Trace changing tests passed ----------")

        # test trace display status
        curr_state = self.OSA.get_display_status()
        if curr_state == True:
            self.change_trace_display_state('display')
            assert self.model.get_trace_display_state() == False and self.OSA.get_display_status() == False, "Trace display state not display assertion failed"
            self.change_trace_display_state('display')
            assert self.model.get_trace_display_state() == True and self.OSA.get_display_status() == True, "Trace display state display assertion failed"
        else:
            self.change_trace_display_state('display')
            assert self.model.get_trace_display_state() == True and self.OSA.get_display_status() == True, "Trace display state display assertion failed"
            self.change_trace_display_state('display')
            assert self.model.get_trace_display_state() == False and self.OSA.get_display_status() == False, "Trace display state not display assertion failed"

        print("---------- Trace display state tests passed ----------")

        # test trace state
        self.change_trace_state('update')
        assert self.model.get_trace_state() == 'UPDATE' and self.OSA.get_write_status() == True, "Trace state update assertion failed"
        self.change_trace_state('hold')
        assert self.model.get_trace_state() == 'HOLD' and self.OSA.get_write_status() == False, "Trace state hold assertion failed"

        print("---------- Trace state tests passed ----------")

        # test measurement state
        self.change_measurement_state('auto')
        assert self.model.get_measurement_state() == 'AUTO' and self.OSA.get_sweep_status() == 'AUTO', "Measurement state auto assertion failed"
        self.change_measurement_state('single')
        assert self.model.get_measurement_state() == 'SINGLE' and self.OSA.get_sweep_status() == 'SINGLE', "Measurement state single assertion failed"
        self.change_measurement_state('stop')
        assert self.model.get_measurement_state() == 'STOP' and self.OSA.get_sweep_status() == 'STOP', "Measurement state stop assertion failed"

        print("---------- Measurement state tests passed ----------")

        # test scale
        curr_scale = self.OSA.get_scale()
        if curr_scale == 'LOG':
            self.switch_scale()
            assert self.model.get_scale() == 'LIN' and self.OSA.get_scale() == 'LIN', "Scale lin assertion failed"
            self.switch_scale()
            assert self.model.get_scale() == 'LOG' and self.OSA.get_scale() == 'LOG', "Scale log assertion failed"
        else:
            self.switch_scale()
            assert self.model.get_scale() == 'LOG' and self.OSA.get_scale() == 'LOG', "Scale log assertion failed"
            self.switch_scale()
            assert self.model.get_scale() == 'LIN' and self.OSA.get_scale() == 'LIN', "Scale lin assertion failed"

        print("---------- Scale tests passed ----------")

        # test resolution
        self.resolution_changed('0.05')
        assert self.model.get_resolution() == '0.05' and self.OSA.get_resolution() == '0.05', "Resolution 0.05 assertion failed"
        self.resolution_changed('0.1')
        assert self.model.get_resolution() == '0.1' and self.OSA.get_resolution() == '0.1', "Resolution 0.1 assertion failed"
        self.resolution_changed('0.2')
        assert self.model.get_resolution() == '0.2' and self.OSA.get_resolution() == '0.2', "Resolution 0.2 assertion failed"
        self.resolution_changed('0.5')
        assert self.model.get_resolution() == '0.5' and self.OSA.get_resolution() == '0.5', "Resolution 0.5 assertion failed"
        self.resolution_changed('1')
        assert self.model.get_resolution() == '1' and self.OSA.get_resolution() == '1.0', "Resolution 1 assertion failed"
        self.resolution_changed('2')
        assert self.model.get_resolution() == '2' and self.OSA.get_resolution() == '2.0', "Resolution 2 assertion failed"
        self.resolution_changed('5')
        assert self.model.get_resolution() == '5' and self.OSA.get_resolution() == '5.0', "Resolution 5 assertion failed"
        self.resolution_changed('10')
        assert self.model.get_resolution() == '10' and self.OSA.get_resolution() == '10.0', "Resolution 10 assertion failed"

        print("---------- Resolution tests passed ----------")

        # test start
        self.start_changed('350')
        assert self.model.get_start() == '350' and self.OSA.get_start_wl() == '350.00', "Start 350 assertion failed"
        self.start_changed('400')
        assert self.model.get_start() == '400' and self.OSA.get_start_wl() == '400.00', "Start 400 assertion failed"

        print("---------- Start tests passed ----------")

        # test stop
        self.stop_changed('1700')
        assert self.model.get_stop() == '1700' and self.OSA.get_stop_wl() == '1700.00', "Stop 1700 assertion failed"
        self.stop_changed('1600')
        assert self.model.get_stop() == '1600' and self.OSA.get_stop_wl() == '1600.00', "Stop 1600 assertion failed"

        print("---------- Stop tests passed ----------")

        # test center
        self.update_center('1000')
        assert self.model.get_center() == '1000' and self.OSA.get_center_wl() == '1000.00', "Center 1000 assertion failed"
        self.update_center('1200')
        assert self.model.get_center() == '1200' and self.OSA.get_center_wl() == '1200.00', "Center 1200 assertion failed"

        print("---------- Center tests passed ----------")

        # test span
        self.update_span('100')
        assert self.model.get_span() == '100' and self.OSA.get_span() == '100.0', "Span 100 assertion failed"
        self.update_span('200')
        assert self.model.get_span() == '200' and self.OSA.get_span() == '200.0', "Span 200 assertion failed"

        print("---------- Span tests passed ----------")

        # test averages
        self.averages_changed('1')
        assert self.model.get_averages() == '1' and self.OSA.get_averages() == '1', "Averages 1 assertion failed"
        self.averages_changed('2')
        assert self.model.get_averages() == '2' and self.OSA.get_averages() == '2', "Averages 2 assertion failed"

        print("---------- Averages tests passed ----------")

        print(" ***** ALL TESTS PASSED *****")


    def update_function(self):
        # check measurement state
        if self.model.get_measurement_state() == 'STOP':
            self.view.stop_button.config(state=tk.DISABLED)
            self.view.single_button.config(state=tk.NORMAL)
            self.view.auto_button.config(state=tk.NORMAL)

        # run retrieve_traces in separate thread
        if not hasattr(self, 't'):
            self.view.write_to_log("Starting retrieval of traces.")
        if not hasattr(self, 't') or self.t.is_alive() == False:
            self.t = threading.Thread(target=self.retrieve_traces, daemon=True)
            self.t.start()

        self.view.mainwindow.after(20, self.update_function)
        
    def dequeue_traces(self):
        try:
            # dequeue traces 
            if not self.trace_queue.empty():
                traces = self.trace_queue.get()
                #print("Dequeued traces, number of traces in queue left is " + str(self.trace_queue.qsize()))
                # create figure
                fig = Figure(figsize=(5, 4), dpi=100)
                # add subplot
                a = fig.add_subplot(111)
                # plot the traces
                for trace in traces:
                    # plot the trace and put trace[0] as the label
                    a.plot(trace[2], trace[1], label="Trace " + trace[0])

                # draw the canvas
                # add legend
                a.legend()
                self.draw_canvas(fig)
        except Exception as e:
            print("Could not dequeue traces")
            #print(e)
        self.view.mainwindow.after(20, self.dequeue_traces)

    def draw_canvas(self, fig):
        # which widget has focus before
        focus = self.view.get_focused_widget()
        # Draw the canvas on the main thread
        self.view.spectrum_canvas = FigureCanvasTkAgg(fig, master=self.view.frame11)
        self.view.spectrum_canvas.draw()
        self.view.spectrum_canvas.get_tk_widget().grid(column=0, padx=5, pady=5, row=0)

        self.view.change_focus(focus)
        

    def retrieve_traces(self):
        time.sleep(2)

        # check connection status
        if not self.OSA.check_connection_status():
            self.view.write_to_log("Connection to OSA lost.")
            self.model.connected = False
            self.view.change_retrieving_label('none', False)
            self.view.write_to_log("Trying to reconnect...")
            reply = self.OSA.try_to_reconnect()
            if reply:
                self.model.set_connected(True)
                self.view.change_retrieving_label('none', True)
            else:
                return

        self.view.change_retrieving_label("retrieving", self.model.get_connected())
        # check what the measurement-status is. This is done here, in this thread, so the program does not slow down if the mainthread tries to chec kthis while it is already retrieving.
        sweep_status = self.OSA.get_sweep_status()
        self.model.set_measurement_state(sweep_status)

        try:
            # check which are set to display
            disp_a = self.OSA.inst.query('DSPA?')
            if disp_a[0] == '1': 
                disp_a = True
            else:
                disp_a = False
            disp_b = self.OSA.inst.query('DSPB?')
            if disp_b[0] == '1':
                disp_b = True
            else:
                disp_b = False
            disp_c = self.OSA.inst.query('DSPC?')
            if disp_c[0] == '1':
                disp_c = True
            else:
                disp_c = False

            if disp_a:
                trace_a = self.OSA.inst.query("LDATA")
                trace_a = trace_a.split(',')
                trace_a = trace_a[1:-1]
                trace_a = [float(x) for x in trace_a]
                lam_a = self.OSA.inst.query("WDATA")
                lam_a = lam_a.split(',')
                lam_a = lam_a[1:-1]
                lam_a = [float(x) for x in lam_a]
            if disp_b:
                trace_b = self.OSA.inst.query("LDATB")
                trace_b = trace_b.split(",")
                trace_b = trace_b[1:-1]
                trace_b = [float(x) for x in trace_b]
                lam_b = self.OSA.inst.query("WDATB")
                lam_b = lam_b.split(",")
                lam_b = lam_b[1:-1]
                lam_b = [float(x) for x in lam_b]
            if disp_c:
                trace_c = self.OSA.inst.query("LDATC")
                trace_c = trace_c.split(",")
                trace_c = trace_c[1:-1]
                trace_c = [float(x) for x in trace_c]
                lam_c = self.OSA.inst.query("WDATC")
                lam_c = lam_c.split(",")
                lam_c = lam_c[1:-1]
                lam_c = [float(x) for x in lam_c]
            self.view.change_retrieving_label("none", self.model.get_connected())
            # combine trace_a-lam_a, trace_b-lam_b, trace_c-lam_c into tuples of vectors to hold the returned parameters
            traces = []
            if disp_a:
                traces.append(('A', trace_a, lam_a)) 
            if disp_b:
                traces.append(('B', trace_b, lam_b))
            if disp_c:
                traces.append(('C', trace_c, lam_c))
            self.trace_queue.put(traces)
        except Exception as e:
            print("Could not retrieve traces")
            print(e)

    def connect_osa(self):
        print("connecting to OSA")
        self.view.write_to_log("Connecting to OSA...")
        # connect to the OSA
        self.OSA = Ando.Ando(5)
        if self.OSA.inst == None:
            self.view.write_to_log("Could not connect to GPIB address 5")
            self.model.connected = False
        else:
            self.view.write_to_log("Connected to GPIB address 5")
            self.model.connected = True
            self.view.log_label.configure(text="Status: Connected.")

    def set_init_values(self):
        # setting start trace
        curr_trace = self.OSA.get_current_trace()
        self.model.set_current_trace(curr_trace)
        if self.model.get_current_trace() == 'A':
            self.view.trace_A.config(state=tk.DISABLED)
        elif self.model.get_current_trace() == 'B':
            self.view.trace_B.config(state=tk.DISABLED)
        elif self.model.get_current_trace() == 'C':
            self.view.trace_C.config(state=tk.DISABLED)

        # updating display-values etc 
        curr_disp_status = self.OSA.get_display_status()
        self.model.set_trace_display_state(curr_disp_status)
        if curr_disp_status:
            self.view.display_button.config(state=tk.DISABLED)

        # updating write-status
        curr_write_status = self.OSA.get_write_status()
        self.model.trace_state = curr_write_status
        if curr_write_status:
            self.view.update_button.config(state=tk.DISABLED)
        elif not curr_write_status:
            self.view.hold_button.config(state=tk.DISABLED)

        # get sweep status
        sweep_status = self.OSA.get_sweep_status()
        self.model.set_measurement_state(sweep_status)
        if sweep_status == 'STOP':
            self.view.stop_button.config(state=tk.DISABLED)
        elif sweep_status == 'SINGLE':
            self.view.single_button.config(state=tk.DISABLED)
        elif sweep_status == 'AUTO':
            self.view.auto_button.config(state=tk.DISABLED)

        # start and stop initial states
        self.model.set_start(self.OSA.get_start_wl())
        self.model.set_stop(self.OSA.get_stop_wl())
        self.view.start_entry.insert(0, self.model.get_start())
        self.view.stop_entry.insert(0, self.model.get_stop())
        self.update_center_entry()
        self.update_span_entry()

        # averages
        self.model.set_averages(self.OSA.get_averages())
        self.view.averages_entry.insert(0, self.model.get_averages())

        # scale
        curr_scale = self.OSA.get_scale()
        self.model.set_scale(curr_scale)
        self.view.scale_button.configure(text=self.model.get_scale())
        
        # resolution
        curr_res = self.OSA.get_resolution()
        self.model.set_resolution(curr_res)
        # change resolution optionmenu to display the current resolution
        self.view.change_resolution_menu(curr_res)
        
        self.view.write_to_log("Start-values set.")
    
    # The user changed the start-values and thus the model needs to be updated and then the view, based on the values in the model
    def start_changed(self, event):
        self.model.set_start(self.view.start_entry.get())
        start_wl = self.OSA.set_start_wl(self.model.get_start())
        self.view.write_to_log("Start wavelength set to " + start_wl + " nm.")
        self.update_center_entry()
        self.update_span_entry()

    def update_stop_entry(self):
        self.view.stop_entry.delete(0, tk.END)
        self.view.stop_entry.insert(0, str(float(self.model.get_start()) + float(self.model.get_span())))

    def update_start_entry(self):
        self.view.start_entry.delete(0, tk.END)
        self.view.start_entry.insert(0, str(float(self.model.get_center()) - float(self.model.get_span()) / 2))

    def averages_changed(self, event):
        self.model.set_averages(self.view.averages_entry.get())
        self.OSA.set_averages(self.model.get_averages())
        self.view.write_to_log("Averages set to " + self.OSA.get_averages() + ".")

    # The user changed the stop-values and thus the model needs to be updated and then the view, based on the values in the model
    def stop_changed(self, event):
        self.model.set_stop(self.view.stop_entry.get())
        stop_wl = self.OSA.set_stop_wl(self.model.get_stop())
        self.view.write_to_log("Stop wavelength set to " + stop_wl + " nm.")
        self.update_center_entry()
        self.update_span_entry()

    def update_center_entry(self):
        self.view.center_entry.delete(0, tk.END)
        new_center = str((float(self.model.get_start()) + float(self.model.get_stop())) / 2)
        self.view.center_entry.insert(0, new_center)
        self.model.set_center(new_center)

    def update_center(self, event):
        self.model.set_center(self.view.center_entry.get())
        center_wl = self.OSA.set_center_wl(self.model.get_center())
        self.view.write_to_log("Center wavelength set to " + center_wl + " nm.")
        self.update_start_entry()
        self.update_stop_entry()
        self.update_span_entry()

    def update_span_entry(self):
        self.view.span_entry.delete(0, tk.END)
        new_span = str(float(self.model.get_stop()) - float(self.model.get_start()))
        self.view.span_entry.insert(0, new_span)
        self.model.set_span(new_span)

    def update_span(self, event):
        self.model.set_span(self.view.span_entry.get())
        span = self.OSA.set_span(self.model.get_span())
        self.view.write_to_log("Span wavelength set to " + span + " nm.")
        self.update_start_entry()
        self.update_stop_entry()
        self.update_center_entry()

    def set_current_trace(self, current_trace):
        self.model.set_current_trace(current_trace)
        curr = self.OSA.set_current_trace(self.model.get_current_trace())
        current_display_state = self.OSA.get_display_status()
        current_hold_state = self.OSA.get_write_status()

        # check which is the current button, disable that one, and enable all the others
        if curr == 'A':
            self.view.trace_A.config(state=tk.DISABLED)
            self.view.trace_B.config(state=tk.NORMAL)
            self.view.trace_C.config(state=tk.NORMAL)
        elif curr == 'B':
            self.view.trace_A.config(state=tk.NORMAL)
            self.view.trace_B.config(state=tk.DISABLED)
            self.view.trace_C.config(state=tk.NORMAL)
        elif curr == 'C':
            self.view.trace_A.config(state=tk.NORMAL)
            self.view.trace_B.config(state=tk.NORMAL)
            self.view.trace_C.config(state=tk.DISABLED)

        # check which is the current trace display state, disable that one, and enable all the others
        if current_display_state:
            self.model.set_trace_display_state(True)
            self.view.display_button.config(state=tk.DISABLED)
        else:
            self.model.set_trace_display_state(False)
            self.view.display_button.config(state=tk.NORMAL)
        if current_hold_state:
            self.model.set_trace_state('UPDATE')
            self.view.update_button.config(state=tk.DISABLED)
            self.view.hold_button.config(state=tk.NORMAL)
        else:
            self.model.set_trace_state('HOLD')
            self.view.hold_button.config(state=tk.DISABLED)
            self.view.update_button.config(state=tk.NORMAL)

        # write to log 
        self.view.write_to_log("Current trace set to " + self.model.get_current_trace() + ".")

    def switch_scale(self):
        if self.model.get_scale() == 'LOG':
            self.model.set_scale('LIN')
            self.OSA.set_scale(self.model.get_scale())
            self.view.scale_button.configure(text=self.model.get_scale())
            self.view.write_to_log("Scale set to " + self.OSA.get_scale() + ".")
        elif self.model.get_scale() == 'LIN':
            self.model.set_scale('LOG')
            self.OSA.set_scale(self.model.get_scale())
            self.view.scale_button.configure(text=self.model.get_scale())
            self.view.write_to_log("Scale set to " + self.OSA.get_scale() + ".")

    def resolution_changed(self, event):
        self.model.set_resolution(event)
        self.OSA.set_resolution(self.model.get_resolution())
        self.view.write_to_log("Resolution set to " + self.OSA.get_resolution() + ".")

    def change_measurement_state(self, button):
        # change value in the model
        if button == 'stop':
            self.model.measurement_state = 'STOP'
            self.OSA.set_sweep_status('STOP')
        elif button == 'single':
            self.model.measurement_state = 'SINGLE'
            self.OSA.set_sweep_status('SINGLE')
        elif button == 'auto':
            self.model.measurement_state = 'AUTO'
            self.OSA.set_sweep_status('AUTO')
        
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
            self.OSA.set_write_status(True)
        elif button == 'hold':
            self.model.trace_state = 'HOLD'
            self.OSA.set_write_status(False)
        
        # disable the chosen trace_state_button and enable all the others
        if self.model.trace_state == 'UPDATE':
            self.view.update_button.config(state=tk.DISABLED)
            self.view.hold_button.config(state=tk.NORMAL)
        elif self.model.trace_state == 'HOLD':
            self.view.update_button.config(state=tk.NORMAL)
            self.view.hold_button.config(state=tk.DISABLED)

        # write to log
        self.view.write_to_log("Trace state set to " + self.model.trace_state + ".")

    def change_trace_display_state(self, button):
        self.model.trace_display_state = not self.model.trace_display_state
        state = self.OSA.set_display_status(self.model.get_trace_display_state())

        if state:
            self.view.display_button.config(state=tk.DISABLED)
            self.view.write_to_log("Trace display state set to display.")
        else:
            self.view.display_button.config(state=tk.NORMAL)
            self.view.write_to_log("Trace display state set to not display.")

    def save_measurement(self):
        # open a new tkinter-window with three checkboxes, 'A', 'B' and 'C', a button to choose a directory and a button to save
        self.view.write_to_log("Saving measurement...")
        # ask for save-directory
        self.model.save_dir = askdirectory(initialdir = os.getcwd(),title = "Select directory")
        #f = asksaveasfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        filename = tk.simpledialog.askstring("Filename", "Please enter a filename", parent=self.view.mainwindow)

        # check which traces are set to save
        if self.model.save_a:
            # save trace A
            self.save_trace('A', filename+"_A")
            self.view.write_to_log("Trace A saved to directory as " + filename+"_A" + ".csv")
        if self.model.save_b:
            # save trace B
            self.save_trace('B', filename+"_B")
            self.view.write_to_log("Trace B saved to directory as " + filename+"_B" + ".csv")
        if self.model.save_c:
            # save trace C
            self.save_trace('C', filename+"_C")
            self.view.write_to_log("Trace C saved to directory as " + filename+"_C" + ".csv")

    def save_trace(self, trace, filename):
        trace, lam = self.OSA.get_trace(trace)
        if len(trace) == len(lam):
            # write to file
            with open(self.model.save_dir + '/' + filename +  '.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                # make list of tuples of (wavelength, trace)
                trace = list(zip(lam, trace))
                writer.writerows(trace)

    def save_state_change(self, button):
        if button == 'A':
            self.model.save_a = not self.model.save_a
        elif button == 'B':
            self.model.save_b = not self.model.save_b
        elif button == 'C':
            self.model.save_c = not self.model.save_c

        if self.model.save_a:
            self.view.trace_a_save.config(state=tk.DISABLED)
        else:
            self.view.trace_a_save.config(state=tk.NORMAL)
        if self.model.save_b:
            self.view.trace_b_save.config(state=tk.DISABLED)
        else:
            self.view.trace_b_save.config(state=tk.NORMAL)
        if self.model.save_c:
            self.view.trace_c_save.config(state=tk.DISABLED)
        else:
            self.view.trace_c_save.config(state=tk.NORMAL)

        self.view.write_to_log("Save state changed for trace " + button + ".")