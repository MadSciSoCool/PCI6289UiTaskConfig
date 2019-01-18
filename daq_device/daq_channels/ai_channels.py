import numpy as np
from nidaqmx.stream_readers import AnalogMultiChannelReader
from .process_ai_data import process_ai_data
from .channels import Channels


class AIChannels(Channels):

    def __init__(self, device_name):
        super().__init__(self, device_name)
        self.number_of_channels = 0
        self.number_of_samples = 0
        self._allocate()

    def _setup_channels(self, channels_config):  # channel_config is a dict of dict
        self.number_of_channels = len(channels_config)
        for (channel_name, config) in channels_config.items():
            channel_name = self.device_name + channel_name
            self.ai_task.ai_channels.add_ai_voltage_chan(physical_channel=channel_name,
                                                         terminal_config=config['terminal_config'],
                                                         min_val=config['min_val'],
                                                         max_val=config['max_val'])
        self.task.stop()

    def _setup_task(self, **kwargs):
        self.number_of_samples = kwargs['number_of_samples']
        reader = AnalogMultiChannelReader(self.task.in_stream)
        reader.read_many_sample(data=self.acquired_data, number_of_samples_per_channel=self.number_of_samples)

    def _done_event(self, *args):
        self.ai_task.stop()
        process_ai_data(self.acquired_data)
        self.is_locked = False

    def _allocate(self):
        self.acquired_data = np.empty(shape=[self.number_of_channels, self.number_of_samples], dtype=float)
