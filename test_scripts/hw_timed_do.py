import nidaqmx
import numpy as np
from nidaqmx.stream_writers import DigitalSingleChannelWriter
from time import sleep

def done_event(*args):
    print('measurement done')


def pulse(time):
    waveform = np.ones(time, dtype=np.uint32)
    waveform = np.append(waveform, 0)
    return waveform


if __name__ == '__main__':
    virtual_task = nidaqmx.Task()
    do_task = nidaqmx.Task()
    # don't know whether the task should be stopped forehand
    virtual_task.stop()
    do_task.stop()
    # create a virtual analog input channel
    virtual_task.ai_channels.add_ai_voltage_chan('Dev1/ai0')
    virtual_task.timing.cfg_samp_clk_timing(1000)
    # configure the digital output task
    do_task.do_channels.add_do_chan('Dev1/port0/line0:31')
    writer = DigitalSingleChannelWriter(do_task.out_stream, auto_start=False)
    # set do sampling time triggered by analog sampling clock
    do_task.timing.cfg_samp_clk_timing(1000, source='Dev1/ai/sample_clock')
    writer.write_many_sample_port_uint32(data=pulse(1000))
    # start the measurement
    virtual_task.start()
    do_task.start()
    sleep(3)
    virtual_task.close()
    do_task.stop()