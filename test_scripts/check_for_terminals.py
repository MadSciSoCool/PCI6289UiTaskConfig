import nidaqmx.system


system = nidaqmx.system.System.local()
device = system.devices['Dev1']
for terminal in device.terminals:
    print(terminal)