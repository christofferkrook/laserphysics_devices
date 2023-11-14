from ThorlabsPM100 import ThorlabsPM100, USBTMC
import numpy as np

inst = USBTMC(device="/dev/usbtmc0")
power_meter = ThorlabsPM100(inst=inst)

power_meter.sense.average.count = 10
power = power_meter.read
