# program to use pyvisa to talk with gpib adress 5

import pyvisa as visa

rm = visa.ResourceManager()
print(rm.list_resources())
