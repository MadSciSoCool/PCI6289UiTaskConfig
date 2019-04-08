import numpy as np
import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.constants import READ_ALL_AVAILABLE, AcquisitionType, TerminalConfiguration
from nidaqmx.errors import DaqError
from .process_ai_data import process_ai_data
from .channels import Channels


class AIChannels(Channels):

    def __init__(self, device_name):
        super().__init__(device_name)
        self.acquired_data = np.zeros(0, dtype=np.float64)
        self.is_active = False
        self.path = ""
        self.period_time = 1000
        self.max_frequency = -1
        self.min_frequency = -1
        self.fft_start = -1
        self.fft_end = -1
        self.measurement_no = 1
        self.enable_plot = False

    def rebuild_task(self, channels_config):
        self.task.close()
        self.task = nidaqmx.Task()
        self._setup_channels(channels_config)
        self.task.register_done_event(self._done_event)

    def _setup_channels(self, channels_config):  # channel_config is a dict of dict
        mapping = {"RSE": TerminalConfiguration.RSE, "NRSE": TerminalConfiguration.NRSE,
                   "DIFFERENTIAL": TerminalConfiguration.DIFFERENTIAL}
        active_flag = False
        for (channel_name, config) in channels_config.items():
            channel_name = self.device_name + channel_name
            if config["terminal_status"]:
                self.task.ai_channels.add_ai_voltage_chan(physical_channel=channel_name,
                                                          terminal_config=mapping[config['terminal_mode']],
                                                          min_val=config['min_value'],
                                                          max_val=config['max_value'])
                active_flag = True
        if active_flag:
            self.reader = AnalogMultiChannelReader(self.task.in_stream)
            self.is_active = True

    def set_data_processing_par(self, path, period_time, min_frequency, max_frequency, fft_start, fft_end, enable_plot,
                                dif_mode, spliced):
        self.path = path
        self.period_time = period_time
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.fft_start = fft_start
        self.fft_end = fft_end
        self.enable_plot = enable_plot
        self.dif_mode = dif_mode
        self.spliced = spliced

    def _done_event(self, *args):
        self.reader.read_many_sample(data=self.acquired_data, number_of_samples_per_channel=READ_ALL_AVAILABLE)
        self.task.stop()
        process_ai_data(acquired_data=self.acquired_data,
                        file_path=self.path,
                        period_time=self.period_time,
                        sampling_rate=self.timing_configuration[0],
                        max_frequency=self.max_frequency,
                        min_frequency=self.min_frequency,
                        fft_start=self.fft_start,
                        fft_end=self.fft_end,
                        enable_plot=self.enable_plot,
                        measurement_no=self.measurement_no,
                        dif_mode=self.dif_mode,
                        spliced=self.spliced)
        self.measurement_no = self.measurement_no + 1
        return 0

    def start_task(self):
        if self.is_active:
            self.task.start()

    @property
    def timing_configuration(self):
        # timing configuration is a tuple as (sampling_rate, number_of_samples_per_channnel)
        return self._timing_configuration

    @timing_configuration.setter
    def timing_configuration(self, value):
        rate, samps_per_chan = value
        if self.is_active:
            try:
                self.task.timing.cfg_samp_clk_timing(rate=rate,
                                                     sample_mode=AcquisitionType.FINITE,
                                                     samps_per_chan=samps_per_chan)
                number_of_channels = self.task.number_of_channels
            except DaqError as error:
                print(error)
            self.acquired_data = np.zeros([number_of_channels, samps_per_chan], dtype=np.float64)
        self._timing_configuration = value
