import nidaqmx
import numpy as np
from nidaqmx.stream_writers import DigitalSingleChannelWriter
from nidaqmx.constants import AcquisitionType
from time import sleep


def done_event(*args):
    print('measurement done')
    return 0

def pulse(time):
    waveform = np.ones(time, dtype=np.uint32)
    waveform = np.append(waveform, np.uint32(0))
    return waveform


if __name__ == '__main__':
    virtual_task = nidaqmx.Task()
    do_task = nidaqmx.Task()
    # create a virtual analog input channel
    virtual_task.ai_channels.add_ai_voltage_chan('Dev1/ai0')
    virtual_task.timing.cfg_samp_clk_timing(1000, sample_mode=AcquisitionType.CONTINUOUS)
    virtual_task.start()
    # configure the digital output task
    do_task.do_channels.add_do_chan('Dev1/port0/line0:31')
    do_task.register_done_event(done_event)
    writer = DigitalSingleChannelWriter(do_task.out_stream, auto_start=False)
    do_task.timing.cfg_samp_clk_timing(1000, source='/Dev1/ai/SampleClock')  # set digital sampling time
    writer.write_many_sample_port_uint32(data=pulse(10))
    do_task.start()
    print('start to write')
    # start the measurement
    sleep(1)
    virtual_task.close()
    do_task.close()
