from nidaqmx.constants import LineGrouping
from nidaqmx.stream_writers import DigitalMultiChannelWriter
from nidaqmx.errors import DaqError
from nidaqmx.constants import AcquisitionType
from .channels import Channels


class DOChannels(Channels):

    def __init__(self, device_name):
        super().__init__(self, device_name)

    def _setup_channels(self, channels_config):
        number_of_channels = len(channels_config)
        name_of_lines = self.device_name + 'port0/line0:' + str(number_of_channels - 1)
        self.task.do_channels.add_do_chan(line=name_of_lines, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        self.writer = DigitalMultiChannelWriter(self.task.out_stream)
        self.waveform = channels_config['waveform']

    def _start(self, **kwargs):
        self.task.start()
        self.writer.write_many_sample_port_uint32(self.waveform)

    @property
    def timing_configuration(self):
        # timing configuration is a tuple as (sampling_rate, source, number_of_samples_per_channnel)
        return self._timing_configuration

    @timing_configuration.setter
    def timing_configuration(self, value):
        rate, source, samps_per_chan = value
        try:
            self.task.timing.cfg_samp_clk_timing(rate=rate,
                                                 source=source,
                                                 sample_mode=AcquisitionType.FINITE,
                                                 samps_per_chan=samps_per_chan)
        except DaqError as error:
            print(error)
        self._timing_configuration = value
