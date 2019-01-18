from nidaqmx.constants import LineGrouping
from nidaqmx.stream_writers import DigitalMultiChannelWriter
from .channels import Channels


class DOChannels(Channels):

    def __init__(self, device_name):
        super().__init__(self, device_name)

    def _setup_channels(self, channels_config):
        number_of_channels = len(channels_config)
        name_of_lines = self.device_name + 'port0/line0:' + str(number_of_channels - 1)
        self.task.do_channels.add_do_chan(line=name_of_lines, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        self.task.stop()

    def _setup_task(self, **kwargs):
        writer = DigitalMultiChannelWriter(self.task.in_stream)
        waveform = kwargs['waveform']
        writer.write_many_sample_port_uint32(data=waveform)
