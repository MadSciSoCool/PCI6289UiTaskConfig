from .channels import Channels


class AOChannels(Channels):

    def __init__(self, device_name):
        super().__init__(self, device_name)

    def _setup_channels(self, channels_config):  # channel_config is a dict of dict
        for (channel_name, config) in channels_config.items():
            channel_name = self.device_name + channel_name
            self.task.ao_channels.add_ao_func_gen_chan(physical_channel=channel_name,
                                                       type=config['type'],
                                                       freq=config['freq'],
                                                       amplitude=config['amplitude'])
