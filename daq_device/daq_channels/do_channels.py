import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType, RegenerationMode
from nidaqmx.stream_writers import DigitalSingleChannelWriter
from nidaqmx.errors import DaqError
from .channels import Channels
from .digital_waveform_convert import digital_waveform_convert


class DOChannels(Channels):

    def __init__(self, device_name):
        super().__init__(device_name)
        self._setup_virtual_task()
        self._setup_channels()

    def _setup_virtual_task(self):
        self.virtual_task = nidaqmx.Task()
        name_of_virtual_channel = self.device_name + "ao0"
        self.virtual_task.ao_channels.add_ao_voltage_chan(name_of_virtual_channel)

    def _setup_channels(self):
        self.waveform = np.zeros(50, dtype=np.uint32)
        name_of_lines = self.device_name + "port0/line0:31"
        self.task.do_channels.add_do_chan(lines=name_of_lines)
        self.task.out_stream.regen_mode = RegenerationMode.ALLOW_REGENERATION
        self.writer = DigitalSingleChannelWriter(self.task.out_stream, auto_start=False)
        self.timing_configuration = 1000
        self.virtual_task.start()

    def set_digital_waveform(self, digital_waveform, sampling_rate):
        self.waveform = digital_waveform_convert(digital_waveform, sampling_rate)

    def start_task(self):
        self.writer.write_many_sample_port_uint32(self.waveform)
        self.task.start()

    def hang(self):
        self.writer.write_many_sample_port_uint32(np.zeros(50, dtype=np.uint32))
        self.task.stop()

    @property
    def timing_configuration(self):
        # timing configuration is a tuple as (sampling_rate, source, number_of_samples_per_channnel)
        return self._timing_configuration

    @timing_configuration.setter
    def timing_configuration(self, value):
        try:
            source = "/" + self.device_name + "ao/SampleClock"
            self.virtual_task.timing.cfg_samp_clk_timing(rate=value)
            self.task.timing.cfg_samp_clk_timing(rate=value,
                                                 source=source,
                                                 sample_mode=AcquisitionType.CONTINUOUS)
        except DaqError as error:
            print(error)
        self._timing_configuration = value
