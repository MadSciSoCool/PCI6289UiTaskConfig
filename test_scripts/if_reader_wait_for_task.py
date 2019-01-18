import nidaqmx
import numpy as np
from time import sleep
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.constants import TerminalConfiguration, AcquisitionType, READ_ALL_AVAILABLE


def done_event(*args):
    print('measurement done')
    return 0


if __name__ == '__main__':
    number_of_channels = 2
    number_of_samples = 15
    data = np.empty([number_of_channels, number_of_samples], dtype=float)
    with nidaqmx.Task() as task:
        task.stop()
        task.ai_channels.add_ai_voltage_chan('Dev1/ai0', terminal_config=TerminalConfiguration.NRSE)
        task.ai_channels.add_ai_voltage_chan('Dev1/ai1', terminal_config=TerminalConfiguration.NRSE)
        task.register_done_event(done_event)
        task.timing.cfg_samp_clk_timing(1000, sample_mode=AcquisitionType.FINITE, samps_per_chan=15)
        reader = AnalogMultiChannelReader(task.in_stream)
        print('reader is defined')
        sleep(2)
        task.start()
        reader.read_many_sample(data, number_of_samples_per_channel=READ_ALL_AVAILABLE)
        print('reading is triggered')
        task.wait_until_done()
        sleep(1)
        print(data)
