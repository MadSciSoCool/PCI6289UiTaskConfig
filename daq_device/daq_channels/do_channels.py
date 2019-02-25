import nidaqmx
from nidaqmx.constants import LineGrouping, AcquisitionType
from nidaqmx.stream_writers import DigitalMultiChannelWriter
from nidaqmx.errors import DaqError
from nidaqmx.constants import AcquisitionType
from .channels import Channels
from .digital_waveform_convert import digital_waveform_convert


class DOChannels(Channels):

    def __init__(self, device_name):
        super().__init__(device_name)

    def _setup_channels(self):
        number_of_lines = 6
        name_of_lines = self.device_name + "port0/line0:" + str(number_of_lines - 1)
        self.task.do_channels.add_do_chan(line=name_of_lines, line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        self.writer = DigitalMultiChannelWriter(self.task.out_stream)
        self.virtual_task = nidaqmx.Task()
        name_of_virtual_channel = self.device_name + "ao0"
        self.virtual_task.ao_channels.add_ao_voltage_chan(name_of_virtual_channel)

    def set_digital_waveform(self, digital_waveform):
        self.samps_per_chan, self.waveform = digital_waveform_convert(digital_waveform)

    def _start(self, **kwargs):
        self.task.start()
        self.writer.write_many_sample_port_uint32(self.waveform)

    @property
    def timing_configuration(self):
        # timing configuration is a tuple as (sampling_rate, source, number_of_samples_per_channnel)
        return self._timing_configuration

    @timing_configuration.setter
    def timing_configuration(self, value):
        try:
            source = self.device_name+"ao/SampleClock"
            self.virtual_task.timing.cfg_samp_clk_timing(rate = value)
            self.task.timing.cfg_samp_clk_timing(rate=value,
                                                 source=source,
                                                 sample_mode=AcquisitionType.FINITE,
                                                 samps_per_chan=self.samps_per_chan)
        except DaqError as error:
            print(error)
        self._timing_configuration = value
