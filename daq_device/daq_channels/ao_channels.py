import numpy as np
from nidaqmx.stream_writers import AnalogMultiChannelWriter
from nidaqmx.constants import AcquisitionType, RegenerationMode
from nidaqmx.errors import DaqError
from .channels import Channels
from .analog_waveform_convert import analog_waveform_convert


class AOChannels(Channels):

    def __init__(self, device_name):
        super().__init__(device_name)
        self._setup_channels()

    def _setup_channels(self):
        number_of_channels = 2
        self.waveform = np.zeros(50, dtype=np.float64)
        for i in range(number_of_channels):
            channel_name = self.device_name + "ao" + str(i)
            self.task.ao_channels.add_ao_voltage_chan(channel_name)
        self.task.out_stream.regen_mode = RegenerationMode.ALLOW_REGENERATION
        self.writer = AnalogMultiChannelWriter(self.task.out_stream)

    def set_analog_waveform(self, analog_waveform, period, sampling_rate):
        self.waveform = analog_waveform_convert(analog_waveform, period, sampling_rate)

    def start_task(self):
        self.writer.write_many_sample(self.waveform)
        self.task.start()

    @property
    def timing_configuration(self):
        # timing configuration is a tuple as (sampling_rate, number_of_samples_per_channnel)
        return self._timing_configuration

    @timing_configuration.setter
    def timing_configuration(self, value):
        try:
            self.task.timing.cfg_samp_clk_timing(rate=value,
                                                 sample_mode=AcquisitionType.CONTINUOUS)
        except DaqError as error:
            print(error)
        self._timing_configuration = value
