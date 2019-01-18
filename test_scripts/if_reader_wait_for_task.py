import nidaqmx
import numpy as np
from time import sleep
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.constants import TerminalConfiguration


def done_event(*args):
    print('measurement done')


if __name__ == '__main__':
    number_of_channels = 2
    number_of_samples = 100
    data = np.empty([number_of_channels, number_of_samples], dtype=float)
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev1/ai0', terminal_config=TerminalConfiguration.NRSE)
        task.ai_channels.add_ai_voltage_chan('Dev1/ai1', terminal_config=TerminalConfiguration.NRSE)
        task.register_done_event(done_event)
        task.stop()
        print('task is stopped')
        sleep(2)
        reader = AnalogMultiChannelReader(task.in_stream)
        reader.read_many_sample(data=data, number_of_samples_per_channel=number_of_samples)
        print('read is triggered')
        sleep(2)
        task.start()
        print('task is started')
