import numpy as np
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.constants import READ_ALL_AVAILABLE, AcquisitionType
from nidaqmx.errors import DaqError
from .process_ai_data import process_ai_data
from .channels import Channels


class AIChannels(Channels):

    def __init__(self, device_name):
        super().__init__(self, device_name)
        self.acquired_data = np.empty(0, dtype=np.uint32)

    def _setup_channels(self, channels_config):  # channel_config is a dict of dict
        self.number_of_channels = len(channels_config)
        for (channel_name, config) in channels_config.items():
            channel_name = self.device_name + channel_name
            self.task.ai_channels.add_ai_voltage_chan(physical_channel=channel_name,
                                                      terminal_config=config['terminal_config'],
                                                      min_val=config['min_val'],
                                                      max_val=config['max_val'])
        self.reader = AnalogMultiChannelReader(self.task.in_stream)

    def _done_event(self, *args):
        self.reader.read_many_sample(data=self.acquired_data, number_of_samples_per_chan=READ_ALL_AVAILABLE)
        process_ai_data(self.acquired_data)
        self.is_locked = False
        return 0

    @property
    def number_of_samples(self):
        return self._number_of_samples

    @number_of_samples.setter
    def number_of_samples(self, value):
        try:
            self.task.timing.cfg_samp_clk_timing(rate=self.rate,
                                                 sample_mode=AcquisitionType.FINITE,
                                                 samps_per_chan=value)
            self.acquired_data = np.empty([self.number_of_channels, value], dtype=np.uint32)
        except DaqError as error:
            print(error)
