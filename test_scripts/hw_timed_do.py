import nidaqmx
import numpy as np
from nidaqmx.stream_writers import DigitalSingleChannelWriter
from nidaqmx.constants import AcquisitionType, RegenerationMode
from time import sleep


def done_event(*args):
    print('measurement done')
    return 0


def pulse(time):
    waveform = np.ones(time, dtype=np.uint32)
    ending_sequence = np.zeros(1, dtype=np.uint32)
    waveform = np.append(ending_sequence, waveform)
    waveform = np.append(waveform, ending_sequence)
    return waveform


if __name__ == '__main__':
    virtual_task = nidaqmx.Task()
    do_task = nidaqmx.Task()
    # create a virtual analog input channel
    virtual_task.ao_channels.add_ao_voltage_chan('Dev1/ao0')
    virtual_task.timing.cfg_samp_clk_timing(1000, sample_mode=AcquisitionType.CONTINUOUS)
    virtual_task.start()
    # configure the digital output task
    do_task.do_channels.add_do_chan('Dev1/port0/line0:31')
    do_task.register_done_event(done_event)
    do_task.out_stream.regen_mode=RegenerationMode.DONT_ALLOW_REGENERATION
    writer = DigitalSingleChannelWriter(do_task.out_stream, auto_start=False)
    do_task.timing.cfg_samp_clk_timing(1000, source='/Dev1/ao/SampleClock')  # set digital sampling time
    writer.write_many_sample_port_uint32(pulse(200))
    # do_task.write(pulse(300),auto_start=False)
    print('start to write')
    do_task.start()
    # start the measurement
    sleep(3)
    virtual_task.close()
    do_task.close()
