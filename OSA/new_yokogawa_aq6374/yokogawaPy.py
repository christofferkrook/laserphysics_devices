# to open communication
# sudo chmod 666 /dev/gpib0
# must be written in the terminal. Perhaps I should write a bash-script to do
# all of these start-up things now.

import pyvisa
import numpy as np


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