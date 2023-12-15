import pyvisa as visa
import numpy as np

# creation of class
    
class Ando:

        # init
    def __init__(self, gpib_address):
        self.gpib_address = gpib_address
        self.rm = visa.ResourceManager()
        try:
            self.inst = self.rm.open_resource('GPIB0::' + str(gpib_address) + '::INSTR')
        except:
            self.inst = None
            print('Could not connect to GPIB address ' + str(gpib_address))
        self.inst.timeout = 10000
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'

        opened_resources = self.rm.list_opened_resources()
        self.resource_name = opened_resources[0]

    def check_connection_status(self):
        try:
            self.inst.query('*IDN?')
            return True
        except:
            return False
        
    def try_to_reconnect(self):
        self.rm2 = visa.ResourceManager()
        try:
            print(self.rm2.list_resources())
            self.inst = self.rm2.open_resource('GPIB0::' + str(self.gpib_address) + '::INSTR')
            return True
        except:
            return False

    # get the current trace
    def get_current_trace(self):
        try:
            trace = self.inst.query('ACTV?').strip()
            if trace[0] == '2':
                return 'C'
            elif trace[0] == '1':
                return 'B'
            elif trace[0] == '0':
                return 'A'
            return 
        except:
            print("Could not get current trace")

    # set the current trace
    def set_current_trace(self, trace):
        if trace == 'A':
            self.inst.write('ACTV0')
        elif trace == 'B':
            self.inst.write('ACTV1')
        elif trace == 'C':
            self.inst.write('ACTV2')
        return self.get_current_trace()

    # get display-status of current trace
    def get_display_status(self):
        try:
            status = self.inst.query('DSP' + self.get_current_trace() + '?').strip()
            if status[0] == '1':
                return True
            elif status[0] == '0':
                return False
            return
        except:
            print("Could not get display status")

    def set_display_status(self, status):
        if status:
            self.inst.write('DSP' + self.get_current_trace())
        else:
            self.inst.write('BLK' + self.get_current_trace())
        return self.get_display_status()

    def get_write_status(self):
        try:
            status = self.inst.query('TR' + self.get_current_trace() + '?').strip()
            if status[0] == '0':
                return True
            elif status[0] == '1':
                return False
            return
        except:
            print("Could not get write status")

    def set_write_status(self, status):
        if status:
            self.inst.write('WRT' + self.get_current_trace())
        else:
            self.inst.write('FIX' + self.get_current_trace())
        return self.get_write_status()

    def get_sweep_status(self):
        try:
            status = self.inst.query('SWEEP?').strip()
            if status[0] == '0':
                return 'STOP'
            elif status[0] == '1':
                return 'SINGLE'
            elif status[0] == '2':
                return 'REPEAT'
            elif status[0] == '3':
                return 'AUTO'
            elif status[0] == '4':
                return 'SEGMENT_MEASURE'
        except:
            print("Could not get sweep status")

    def set_sweep_status(self, sweep):
        if sweep == 'STOP':
            self.inst.write('STP')
        elif sweep == 'SINGLE':
            self.inst.write('SGL')
        elif sweep == 'AUTO':
            self.inst.write('RPT')
        elif sweep == 'SEGMENT_MEASURE':
            self.inst.write('MEAS')
        return self.get_sweep_status()

    def get_start_wl(self):
        try:
            reply = self.inst.query('STAWL?').strip()
            # remove everything after '.00'
            return reply
        except:
            print("Could not get start wavelength")

    def set_start_wl(self, wl):
        self.inst.write('STAWL' + str(wl) + ".00")
        return self.get_start_wl()

    def get_stop_wl(self):
        try:
            reply = self.inst.query('STPWL?').strip()
            return reply
        except:
            print("Could not get stop wavelength")

    def set_stop_wl(self, wl):
        self.inst.write('STPWL' + str(wl) + ".00")
        return self.get_stop_wl()

    def get_center_wl(self):
        try:
            return self.inst.query('CTRWL?').strip()
        except:
            print("Could not get center wavelength")

    def set_center_wl(self, wl):
        self.inst.write('CTRWL' + str(wl) + ".00")
        return self.get_center_wl()

    def get_averages(self):
        try:
            return self.inst.query('AVG?').strip()
        except:
            print("Could not get averages")

    def set_averages(self, averages):
        self.inst.write('AVG' + str(averages))
        return self.get_averages()

    def get_resolution(self):
        try:
            return self.inst.query('RESLN?').strip()
        except:
            print("Could not get resolution")

    def set_resolution(self, resolution):
        self.inst.write('RESLN' + str(resolution))
        return self.get_resolution()

    def get_scale(self):
        try:
            reply = self.inst.query('LSCL?')
            if reply.strip() == '0':
                return 'LIN'
            else:
                return 'LOG'
        except:
            print("Could not get scale")

    def set_scale(self, scale):
        if scale == 'LOG':
            self.inst.write('LSCL5.0')
            self.inst.write('ATREF1')
            self.inst.write('ATSCL1')
        elif scale == 'LIN':
            self.inst.write('LSCLLIN')
            self.inst.write('ATREF1')
            self.inst.write('ATSCL1')
        return self.get_scale()
    