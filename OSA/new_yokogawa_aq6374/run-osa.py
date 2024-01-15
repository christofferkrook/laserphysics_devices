from yokogawaPy import OSA
import numpy as np
import matplotlib.pyplot as plt
import os


def printCommands():
    print("What do you want to do ?")
    print("Options are:")
    print("    - commands        - prints the available commands")
    print("    - connect         - connects to the OSA at adress 1")
    print("    - quit            - quits the program")
    print("    - startwl*        - sets the start wavelength (nanometers)")
    print("    - stopwl*         - sets the stop wavelength (nanometers)")
    print("    - centerandspan   - sets the center wavelength and span (nanometers)")
    print("    - resolution*     - sets the resolution (nm)")
    print("    - choosetrace     - chooses the trace to be displayed [A, B or C]")
    print("    - retrievetrace   - retrieves the trace")
    print("    - scale*          - switches between log/lin scale")
    print("    - savedirectory*  - sets the directory where the data is saved")
    print("    - averages*       - sets the number of averages")
    print("----------------------\n")

def startwl(disp):
    reply = osa.query(':SENSE:WAVELENGTH:START?')
    reply = str(float(reply[1:-1]) * 1e9)
    if disp:
        print("The start wavelength is " + reply + " nm.")
    return float(reply)

def stopwl(disp):
    reply = osa.query(':SENSE:WAVELENGTH:STOP?')
    reply = str(float(reply[1:-1]) * 1e9)
    if disp:
        print("The stop wavelength is " + reply + " nm.")
    return float(reply)

print("Welcome to the OSA - control program. PLease ensure device GPIB adress is set to 1.")
trace = "A"
save_dir = os.getcwd() + "/osa-data"
r = os.path.isdir(save_dir)
if r == False:
    os.mkdir(save_dir)

printCommands()

while True:
    command = input("---- Command: ")
    if command == "connect":
        osa = OSA(1, True)
        scale = osa.query(":DISPLAY:TRACE:Y1:SPACING?")
        if scale[0] == '0':
            print("Current scale is LOGARITHMIC")
        elif scale[0] == '1':
            print("Current scale is LINEAR")
        print("Default save directory set to PWD (" + save_dir + ")")
        tra = osa.query(":TRACE:ACTIVE?")
        print("Current trace is " + tra[-2])
    elif command == "startwl":
        wl = input("What is your desired start wavelength? (nm): ")
        swl = stopwl(False)
        if float(wl) > swl:
            print("The new start wavelength must be smaller than the current stopwavelength, please change the stop wavelength first.")
        else:
            osa.write(":SENSE:WAVELENGTH:START " + wl + ".000NM")
            print("Changing start wavelength...")
            startwl(True)

    elif command == "stopwl":
        wl = input("What is your desired stop wavelength? (nm): ")
        swl = startwl(False)
        if float(wl) < swl:
            print("The new stop wavelength must be larger than the current startwavelength, please change the start wavelength first.")
        else:
            osa.write(":SENSE:WAVELENGTH:STOP " + wl + ".000NM")
            print("Changing stop wavelength...")
            stopwl(True)

    elif command == "startwl?":
        startwl(True)

    elif command == "stopwl?":
        stopwl(True)

    elif command == "commands":
        printCommands() 

    elif command == "centerandspan":
        center = input("What is your desired center wavelength? (nm): ")
        span = input("What is your desired span? (nm): ")
        start = str(int(np.floor(float(center) - float(span)/2)))
        stop = str(int(np.floor(float(center) + float(span)/2)))

        # checking so setting new values will not clash with current
        currstop = stopwl(False)
        currstart = startwl(False)

        if float(start) > currstop:
            osa.write(":SENSE:WAVELENGTH:STOP " + "2449" + ".000NM")
        if float(stop) < currstart:
            osa.write(":SENSE:WAVELENGTH:START " + "300" + ".000NM")

        osa.write(":SENSE:WAVELENGTH:START " + start + ".000NM")
        osa.write(":SENSE:WAVELENGTH:stop " + stop + ".000NM")
        print("Changing center and span...")
        startwl(True)
        stopwl(True)
        print("Current center is " + center + " nm.")
    
    elif command == "resolution?":
        reply = str(float(osa.query(":SENSE:BANDWIDTH?")) * 1e9)
        print("The resolution is set to " + reply + " nm.")
    
    elif command == "resolution":
        res = input("What is your desired resolution? Options are 0.05 0.1 0.2 0.5 1 2 5 10 (nm)): ")
        osa.write(":SENSE:BANDWIDTH:RESOLUTION " + res + "NM")
        res = str(float(osa.query(":SENSE:BANDWIDTH?")) * 1e9)
        print("The resolution is changed to " + res + " nm.")
    
    elif command == "choosetrace":
        tra = osa.query(":TRACE:ACTIVE?")
        rep = input("The current trace is " + tra[-2] + ", do you want to change it (y/n) ? ")
        if rep == "y":
            tra = input("Which trace do you want to choose? (A, B or C): ")
            osa.write(":TRACE:ACTIVE TR" + tra)
            tra = osa.query(":TRACE:ACTIVE?")
            print("Trace changed to " + tra[-2])
    
    elif command == "retrievetrace":
        currtrace = osa.query(":TRACE:ACTIVE?")
        currtrace = currtrace[0:3]
        wavelength_axis = osa.query(":TRACE:X? " + currtrace)
        wavelength_axis = np.asarray(wavelength_axis.strip().split(',')[1:], 'f')
        int_axis = osa.query(":TRACE:Y? " + currtrace)
        int_axis = np.asarray(int_axis.strip().split(',')[1:], 'f')
        plt.plot(wavelength_axis, int_axis)
        plt.show(block = False)
        r = input("Do you want to save this trace to a file? (y/n) : ")
        if r == "y":
            filename = input("What is the filename? (do not include .txt): ")
            np.savetxt(save_dir + "/" + filename + ".txt", np.transpose([wavelength_axis, int_axis]))
    
    elif command == "scale":
        currscale = osa.query(":DISPLAY:TRACE:Y1:SPACING?")
        if currscale[0] == '1':
            osa.write(":DISPLAY:TRACE:Y1:SPACING LOG")
        elif currscale[0] == '0':
            osa.write(":DISPLAY:TRACE:Y1:SPACING LIN")
        newscale = osa.query(":DISPLAY:TRACE:Y1:SPACING?")

        if newscale[0] == '1' and currscale[0] == '0':
            print("Changing scale to LOGARITHMIC from LINEAR")
        elif newscale[0] == '0' and currscale[0] == '1':
            print("Changing scale to LINEAR from LOGARITHMIC")
            
    elif command == "scale?":
        currscale = osa.query(":DISPLAY:TRACE:Y1:SPACING?")
        if currscale[0] == '0':
            currscale = "LOGARITHMIC"
        elif currscale[0] == '1':
            currscale = "LINEAR"
        print("Current scale is " + currscale)

    elif command == "savedirectory":
        r = input("Current save_dir is " + save_dir + ", do you want to change it? (y/n) : ")
        if r == "y":
            save_dir = input("What is the new save_dir? : ")
            print("Changing save_dir to " + save_dir)
    
    elif command == "savedirectory?":
        print("Current save_dir is " + save_dir)

    elif command == "averages":
        ave = osa.query(":SENSE:AVERAGE:COUNT?")
        ave = ave[0:-1].strip()
        r = input("Current number of averages is " + ave + ", do you want to change it? (y/n) : ")
        if r == "y":
            ave = input("What is the new number of averages? : ")
            osa.write(":SENSE:AVERAGE:COUNT " + ave)
            print("Changing number of averages to " + ave)
        ave = osa.query(":SENSE:AVERAGE:COUNT?")
        ave = ave[0:-1].strip()
        print("Number of averages changed to " + ave + ".")

    elif command == "quit":
        try:
            osa.osa.close()
        except:
            print("Not connected to OSA. Nothing to close.")
        break
    else:
        print(" --- Command not recognized")
