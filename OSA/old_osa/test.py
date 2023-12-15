import pyvisa as visa

rm = visa.ResourceManager()
addr = rm.list_resources()[0]  # I have a single USB instrument connected
i = rm.open_resource(addr)
print(i.query('*IDN?'))
# Unplug the device, replug the device
print(i.query('*IDN?'))

# Unplug again, replug
i = rm.open_resource(addr)
print(i.query('*IDN?'))