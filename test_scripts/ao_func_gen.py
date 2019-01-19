import nidaqmx
from nidaqmx.constants import FuncGenType


with nidaqmx.Task() as task:
    task.ao_channels.add_ao_func_gen_chan('Dev1/ao0', type=FuncGenType.SINE, freq=1000, amplitude=1.0)
    task.start()
