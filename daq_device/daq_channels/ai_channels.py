
import nidaqmx
from nidaqmx.constants import TerminalConfiguration
from process_ai_data import process_ai_data

class AIChannels:

    def __init__(self, num_of_channels, device_name):
        if num_of_channels > 32:
            print('Too many channels, set to 32')
            self.num_of_channels = 32
        else:
            self.num_of_channels = num_of_channels
        self.device_name = device_name
        self.ai_task = nidaqmx.Task()

    def set_up_channels(self, config):
        for (channel_name, channel_config) in config.items():
            channel_name = self.device_name + channel_name
            self.ai_task.ai_channels.add_ai_voltage_chan(physical_channel=channel_name,
                                                         terminal_config=channel_config['terminal_config'],
                                                         min_val=channel_config['min_val'],
                                                         max_val=channel_config['max_val'])
        self.ai_task.stop()
        self.ai_task.register_done_event()

    def done_callback(self, *args):
        self.ai_task.stop()
        process_ai_data(self.acquired_data)
        self.is_locked = False

    def set_sample_rate(self, rate):
        try:
            self.ai_task.timing.cfg_samp_clk_timing(rate=rate)
        except nidaqmx.errors.DaqError:
            print('Invalid sampling rate')

    def start_acquisition(self):
        self.ai_task.start()
        self.ai_task.wait_until_done()
        self.ai_task.stop()
