# to open communication
# sudo chmod 666 /dev/gpib0
# must be written in the terminal. Perhaps I should write a bash-script to do
# all of these start-up things now.

import pyvisa
import numpy as np
import os


class OSA(object):

    def __init__(self, adress, verb):
        self.connected = False
        resources = pyvisa.ResourceManager('@py')
        self.osa = resources.open_resource('GPIB0::' + str(adress))
        self.verb = verb
        try:
            name = self.osa.query('*IDN?')
            self.connected = True
            if self.verb:
                print("Successfully connected to Yokogawa OSA.")
                # split string name at ','
                substrings = name.split(',')
                print("Serialnumber : " + substrings[2])
                print("Firmware version : " + substrings[3][0:-1])
        except:
            print('Could not connect to ESP300 - stage. Perhaps the GPIB adress is wrong or the permission is not enabled?')

    def query(self, mess):
        if self.connected:
            return self.osa.query(mess)
        else:
            print("Not connected to OSA")
        
    def write(self, mess):
        if self.connected:
            self.osa.write(mess)
        else:
            print("Not connected to OSA")

    def get_startwl(self):
        reply = self.query(':SENSE:WAVELENGTH:START?')
        reply = str(float(reply[1:-1]) * 1e9)
        print("The start wavelength is " + reply + " nm.")
        return float(reply)
    
    def get_stopwl(self):
        reply = self.query(':SENSE:WAVELENGTH:STOP?')
        reply = str(float(reply[1:-1]) * 1e9)
        print("The stop wavelength is " + reply + " nm.")
        return float(reply)
    
    def set_startwl(self, wl):
        swl = self.get_stopwl()
        if float(wl) > swl:
            print("The new start wavelength must be smaller than the current stopwavelength, please change the stop wavelength first.")
        else:
            self.write(":SENSE:WAVELENGTH:START " + wl + ".000NM")
            print("Changing start wavelength...")
            self.get_startwl()
            print("Start-wl set to " + str(wl) + " nm.")

    def set_stopwl(self, wl):
        swl = self.get_startwl()
        if float(wl) < swl:
            print("The new stop wavelength must be larger than the current startwavelength, please change the start wavelength first.")
        else:
            self.write(":SENSE:WAVELENGTH:STOP " + wl + ".000NM")
            print("Changing stop wavelength...")
            self.get_stopwl()
            print("Stop-wl set to " + str(wl) + " nm.")

    def get_scale(self):
        scale = self.query(":DISPLAY:TRACE:Y1:SPACING?")
        if scale[0] == '0':
            print("Current scale is LOGARITHMIC")
            return 'LOG'
        elif scale[0] == '1':
            print("Current scale is LINEAR")
            return 'LIN'
        
    def set_scale(self, scale):
        if scale == 'LOG':
            self.write(":DISPLAY:TRACE:Y1:SPACING LOG")
            print("Scale set to LOGARITHMIC")
        elif scale == 'LIN':
            self.write(":DISPLAY:TRACE:Y1:SPACING LIN")
            print("Scale set to LINEAR")
        
    def get_resolution(self):
        reply = str(float(self.query(":SENSE:BANDWIDTH?")) * 1e9)
        print("The resolution is set to " + reply + " nm.")

        return float(reply)
    
    def set_resolution(self, res):
        self.write(":SENSE:BANDWIDTH:RESOLUTION " + res + "NM")
        res = str(float(self.query(":SENSE:BANDWIDTH?")) * 1e9)
        print("The resolution is changed to " + res + " nm.")

    def get_averages(self):
        ave = self.query(":SENSE:AVERAGE:COUNT?")
        ave = ave[0:-1].strip()
        print("The number of averages is " + ave + ".")
        return int(ave)
    
    def set_average(self, ave):
        self.write(":SENSE:AVERAGE:COUNT " + str(ave))
        ave = self.query(":SENSE:AVERAGE:COUNT?")
        ave = ave[0:-1].strip()
        print("The number of averages is " + ave + ".")
    
    def get_current_trace(self):
        tra = self.query(":TRACE:ACTIVE?")
        print("Current trace is " + tra[-2])
        return tra[-2]
    
    def set_current_trace(self, trace):
        self.write(":TRACE:ACTIVE TR" + trace)
        tra = self.query(":TRACE:ACTIVE?")
        print("Current trace is " + tra[-2])

    def retrieve_trace(self, save_dir, filename):
        currtrace = self.query(":TRACE:ACTIVE?")
        currtrace = currtrace[0:3]
        wavelength_axis = self.query(":TRACE:X? " + currtrace)
        wavelength_axis = np.asarray(wavelength_axis.strip().split(',')[1:], 'f')
        int_axis = self.query(":TRACE:Y? " + currtrace)
        int_axis = np.asarray(int_axis.strip().split(',')[1:], 'f')
        np.savetxt(save_dir + "/" + filename + ".txt", np.transpose([wavelength_axis, int_axis]))