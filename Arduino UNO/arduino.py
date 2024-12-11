import pyfirmata2

# The Arduino IDE must be running in the background with the "Standard Firmata"
# (File -> Examples -> Firmata -> Standard Firmata) sketch uploaded

# Initialize the Arduino UNO
try:
    PORT = pyfirmata2.Arduino.AUTODETECT
except:
    # If the port is not autodetected, find it in the Arduino IDE (usually it is COM3, COM4 or COM5 on PC)
    PORT = 'COM5'
finally:
    board = pyfirmata2.Arduino(PORT)

# Assign the 2nd pin as digital output
digitalOut = board.get_pin('d:2:o')

# digitalOut.write(True) sets the logic signal ON
# digitalOut.write(False) sets the logic signal OFF

board.exit()