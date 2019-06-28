import numpy as np
import nidaqmx
import os
import re
import time
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.constants import READ_ALL_AVAILABLE, AcquisitionType, TerminalConfiguration
from nidaqmx.errors import DaqError
from .save_ai_data import save_ai_data
from .channels import Channels


class AIChannels(Channels):

    def __init__(self, device_name):
        super().__init__(device_name)
        self.acquired_data = np.zeros(0, dtype=np.float64)
        self.is_active = False
        self.measurement_no = 1
        self.set_output_path("")

    def add_signal(self, complete_signal):
        self.complete_signal = complete_signal

    def rebuild_task(self, channels_config):
        self.task.close()
        self.task = nidaqmx.Task()
        self._setup_channels(channels_config)
        self.task.register_done_event(self._done_event)

    def _setup_channels(self, channels_config):  # channel_config is a dict of dict
        mode_mapping = {"RSE": TerminalConfiguration.RSE, "NRSE": TerminalConfiguration.NRSE,
                        "DIFFERENTIAL": TerminalConfiguration.DIFFERENTIAL}
        range_mapping = {"±10V": 10, "±5V": 5, "±2V": 2, "±1V": 1, "±0.5V": 0.5, "±0.2V": 0.2, "±0.1V": 0.1}
        active_flag = False
        for (channel_name, config) in channels_config.items():
            channel_name = self.device_name + channel_name
            if config["terminal_status"]:
                self.task.ai_channels.add_ai_voltage_chan(physical_channel=channel_name,
                                                          terminal_config=mode_mapping[config['terminal_mode']],
                                                          min_val=-1 * range_mapping[config['range']],
                                                          max_val=range_mapping[config['range']])
                active_flag = True
        if active_flag:
            self.reader = AnalogMultiChannelReader(self.task.in_stream)
            self.is_active = True

    def set_output_path(self, path):
        self.output_path = os.path.join(path, time.strftime("[%Y-%m-%d]", time.localtime()))
        self.load_existing_files()

    def load_existing_files(self):
        patt = "(ai_acquired_data_)([1-9][0-9]*)(.csv)"
        existing_no = 0
        if os.path.isdir(self.output_path):
            for item in os.listdir(self.output_path):
                match = re.search(patt, item)
                if match is not None:
                    existing_no = max(existing_no, int(match.group(2)))
        self.measurement_no = existing_no + 1

    def _done_event(self, *args):
        self.reader.read_many_sample(data=self.acquired_data, number_of_samples_per_channel=READ_ALL_AVAILABLE)
        self.task.stop()
        save_ai_data(acquired_data=self.acquired_data,
                     file_path=self.output_path,
                     sampling_rate=self.timing_configuration[0],
                     measurement_no=self.measurement_no)
        self.measurement_no = self.measurement_no + 1
        self.complete_signal.measurement_completed.emit()
        return 0

    def start_task(self):
        if self.is_active:
            self.task.start()

    def stop_task(self):
        if self.is_active:
            self.task.stop()

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
