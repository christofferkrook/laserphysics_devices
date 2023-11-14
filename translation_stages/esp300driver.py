# to open communication
# sudo chmod 666 /dev/gpib0
# must be written in the terminal. Perhaps I should write a bash-script to do
# all of these start-up things now.

import pyvisa
import numpy as np


class esp300stage(object):

    def __init__(self, adress, verb):
        self.connected = False
        resources = pyvisa.ResourceManager('@py')
        self.stage = resources.open_resource('GPIB0::' + str(adress))
        self.verb = verb
        try:
            name = self.stage.query('1ID?')
            pos = self.stage.query('1TP')
            self.connected = True
            if self.verb:
                print("Successfully connected to ESP300 - stage. \nID is " + name[0:len(name)-2] + " and current position is " + pos[0:len(pos)-2] + " mm.")
        except:
            print('Could not connect to ESP300 - stage. Perhaps the GPIB adress is wrong or the permission is not enabled?')


    def getPosition(self):
        pos = self.stage.query("1TP")
        return float(pos[0:len(pos)-2])

    def moveAbsolute(self, position):
        if self.verb:
            print("Moving stage to " + str(np.round(position, 2)))
        target = "1PA" + str(np.round(position, 5))
        self.stage.write(target)
        self.checkIfMoving()
        if self.verb:
            print("Movement stopped")

    def closeCommunication(self):
        print("Closing communication")

    def checkIfMoving(self):
        move_status = self.stage.query("1MD?")
        move_status = move_status[0:len(move_status)-2]
        while move_status != "1":
            move_status = self.stage.query("1MD?")
            move_status = move_status[0:len(move_status)-2]