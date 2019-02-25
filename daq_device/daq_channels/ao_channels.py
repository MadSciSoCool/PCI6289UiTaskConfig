from nidaqmx.stream_writers import AnalogMultiChannelWriter
from nidaqmx.constants import AcquisitionType
from nidaqmx.errors import DaqError
from .channels import Channels
from .analog_waveform import analog_waveform


class AOChannels(Channels):

    def __init__(self, device_name):
        super().__init__(device_name)

    def _setup_channels(self, channels_config):  # channel_config is a dict of dict
        for (channel_name, config) in channels_config.items():
            channel_name = self.device_name + channel_name
            self.task.ao_channels.add_ao_voltage_chan(channel_name)
        self.writer = AnalogMultiChannelWriter(self.task.out_stream)
        self.waveform = analog_waveform(channels_config, sample_rate=self.timing_configuration[0])

    def _start(self):
        self.task.start()
        self.writer.write_many_sample(self.waveform)

    @property
    def timing_configuration(self):
        # timing configuration is a tuple as (sampling_rate, number_of_samples_per_channnel)
        return self._timing_configuration

    @timing_configuration.setter
    def timing_configuration(self, value):
        rate, samps_per_chan = value
        try:
            self.task.timing.cfg_samp_clk_timing(rate=rate,
                                                 sample_mode=AcquisitionType.FINITE,
                                                 samps_per_chan=samps_per_chan)
        except DaqError as error:
            print(error)
        self._timing_configuration = value
