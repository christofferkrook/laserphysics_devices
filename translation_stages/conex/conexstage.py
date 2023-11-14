'''

Created on 22 aug. 2022

 

@author: chk

'''

 

import serial.tools.list_ports
from pickle import NONE
import time

 

class CONEX(object):
    '''
    classdocs
    '''
    def __init__(self, verb, stage):
        self.verb = verb
        if stage == "16mm":
            deviceID = 12297
            if self.verb:
                print("Trying to locate and ID 16mm-stage with device ID 12297")

        self.port = None
        ports = serial.tools.list_ports.comports(include_links=True)
        for port in ports :
            if port.pid == deviceID:
                if self.verb:
                    print("Found it at " + port.device)
                self.port = port.device
                break
        try:
            if port.pid != deviceID:
                print("Could not find the translation stage")
            else:
                self.stage = serial.Serial(self.port,baudrate=57600,timeout=0.0001,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
                
        except:
            print('No ports connected.')
            return
        self.refStage()
        

        #self.moveAbsoluteAndWait(12)
        #print(self.getCurrentPos())
        #self.wait(2)
        #self.goToOpenLoop()
        #self.setAmplitude(0.5)
        #self.setFrequency(60)
        #self.Jog()
        #self.waitUntilStopped()
        #self.closeCom()

        self.status_dict = {
            "0A" : 'ROL after reset',
            "0B" : 'ROL after HOMING state',
            "0C" : 'ROL after STEPPING state',
            "0D" : 'ROL after CONFIGURATION state',
            "0E" : 'ROL after with no parameters',
            "0F" : 'ROL after JOGGING state',
            "10" : 'ROL after SCANNING state',
            "11" : 'ROL after READY CLOSED LOOP state',
            "14" : 'CONFIGURATION',
            "1E" : 'HOMING',
            "1F" : 'REFERENCING',
            "28" : 'MOVING OPEN LOOP (OL)',
            "29" : 'MOVING CLOSED LOOP (CL)',
            "32" : 'RCL after HOMING state',
            "33" : 'RCL after MOVING CL state',
            "34" : 'RCL after DISABLE state',
            "35" : 'RCL after REFERENCING state',
            "3C" : 'DISABLE: after READY CLOSED LOOP state',
            "3D" : 'DISABLE after MVOING CL state',
            "46" : 'JOGGING',
            "50" : 'SCANNING'
        }

           

    def refStage(self):
        if self.verb:
            print('Referencing')
        self.write('OR')
        self.wait(0.1)
        self.write('RFH')
        self.wait(0.2)
        self.expectCode('35');
        #self.waitUntilStopped()
        self.isReady = True

        if self.isReady:
            if not(self.verb):
                print('Translation stage is ready')

    def expectCode(self, code):

        while True:
            self.write('TS')
            reply = self.read()
            if reply == "":
                while reply == "":
                    reply = self.read()
            if reply[7:9] == code:
                break

           

    def waitUntilStopped(self):
        hasAlerted = False
        if self.verb:
            print('Waiting until movement stopped')
        while True:
            if self.checkIfMoving():
                if self.verb & hasAlerted == False:
                    print('Still moving')
                    hasAlerted = True
            else:
                if self.verb:
                    print('Halted!')
                break

     

    def goToClosedLoop(self):
        self.write('OR')
        self.wait(0.01)

    def goToOpenLoop(self):
        self.write('Ol')
        self.wait(0.01)

    def write(self, mess):
        self.stage.write(bytes(''.join(['1', mess, '\r\n']), 'utf-8'))

    def read(self):
        return self.stage.read(32).decode('utf-8')

    def closeCom(self):
        if self.verb:
            print('Closing communication')
        self.stopMovement()
        self.goToClosedLoop()
        ret = self.stage.close()

    def checkIfMoving(self):
        self.write('MS')
        #self.wait(0.001)
        reply = self.read()
        if reply == "":
            while reply == "":
                reply = self.read()
        if reply[len(reply)-3:len(reply)-2] == '1':
            return True
        else:
            return False

    def moveAbsolute(self, pos):
        if self.verb:
            print("Moving absolute to " + str(pos))
        self.write(''.join(['PA', str(pos)]))

    def moveAbsoluteAndWait(self, pos):

        self.moveAbsolute(pos)

        self.expectCode('33')

        self.wait(0.1)

       

    def moveRelative(self, pos):
        if self.verb:
            print("Moving Relative to " + str(pos))
        self.write(''.join(['PR', str(pos)]))

    def moveRelativeAndWait(self, pos):
        self.moveRelative(pos)
        self.waitUntilStopped()

    def stopMovement(self):
        if self.verb:
            print("Stopping movement")
        self.write('ST')

    def getCurrentPos(self):
        self.write('TP')
        reply = self.read()
        if reply == "":
            while reply == "":
                reply = self.read()
        pos = reply
        return float(pos[3:12])

   
    def wait(self, tau):
        if self.verb:
            print('Waiting')
        time.sleep(float(tau))

    def getStatus(self):
        while True:
            self.write('TS')
            reply = self.read()
            if reply == "":
                while reply == "":
                    reply = self.read()
            else:
                break
        return self.interp_status(reply[7:9])
    
    def interp_status(self, message):
        stat = self.status_dict[message]
        return stat


    def setFrequency(self, val):
        self.goToOpenLoop()
        if self.verb:
            print("Setting frequency of translation stage to " + str(val))
        self.write(''.join(['XF', str(val)]))

    def getFrequency(self):
        self.goToOpenLoop()
        self.wait(0.1)
        self.write(''.join(['XF?']))
        self.wait(0.1)
        reply = self.read()
        value = str(reply)
        value = value.replace('1XF', '')
        value = value.replace('\r\n', '')
        if self.verb:
            print("Frequency of translation stage is " + (value))
        return (value)


    def setAmplitude(self, val):
        self.goToOpenLoop()
        if self.verb:
            print("Setting amplitude of translation stage steps to " + str(val))
        self.write(''.join(['XU', str(-val*100), ",", str(val*100)]))
        self.wait(0.01)


    def getAmplitude(self):
        self.goToOpenLoop()
        self.wait(0.1)
        self.write(''.join(['XU?']))
        self.wait(0.1)
        reply = self.read()
        value = str(reply)
        value = value.replace('\r\n', '')
        a, b= value.split(', ')
        value = b
        if self.verb:
            print("Amplitude of translation stage is " + value)
        return str(int(value)/100)

    def Jog(self, steps):
        if self.verb:
            print('Starting jog in positive direction')
        self.goToOpenLoop()
        self.wait(0.01)
        self.write('XR' + str(steps))


