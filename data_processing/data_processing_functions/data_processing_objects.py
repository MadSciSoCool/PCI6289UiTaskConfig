import os
import time
import numpy as np
from enum import Enum
from .spectrum_analyze import spectrum_analyze, splice_data
from .noise_recognition import noise_recognition
from .periods_filter import periods_filter
from .save_spectrums import save_spectrums
from .plot_spectrums import plot_spectrums


class Channel:
    def __init__(self, measurement_name, channel_name, data):
        self.measeurement_name = measurement_name
        self.channel_name = channel_name
        self.data = data
        self.spectrums = []

    def process(self, sampling_period, is_spliced, processing_periods, single_period_length):
        if is_spliced:
            self.spectrums.append(spectrum_analyze(period="Joined",
                                                   channel=self.channel_name,
                                                   sampling_period=sampling_period,
                                                   data=splice_data(self.data, processing_periods)))
        else:
            i = 0
            for period in processing_periods:
                start, end = period
                data_this_period = self.data[start:end]
                length = end - start
                if length < single_period_length:
                    data_this_period = np.append(data_this_period, np.zeros(single_period_length - length))
                self.spectrums.append(spectrum_analyze(period="Period " + str(i),
                                                       channel=self.channel_name,
                                                       sampling_period=sampling_period,
                                                       data=data_this_period))
                i = i + 1


class ProcessingStatus(Enum):
    ERROR = -1
    DATA_READ_FROM_FILE = 1
    NO_AVAILABLE_PERIODS = 3
    PROCESSED = 2


class Measurement:
    def __init__(self, path, measurement_name):
        self.path = path
        self.read_from_file(path)
        self.measurement_name = measurement_name
        self.channels = []
        self.selected_periods = []
        if self.status == ProcessingStatus.DATA_READ_FROM_FILE:
            self.separate_channels()

    def read_from_file(self, path):
        try:
            self.data = np.loadtxt(path, delimiter=",", skiprows=1).T
            self.status = ProcessingStatus.DATA_READ_FROM_FILE
        except Exception:
            self.status = ProcessingStatus.ERROR

    def separate_channels(self):
        i = 0
        self.sampling_period = self.data[0][1] - self.data[0][0]
        self.sampling_rate = 1. / self.sampling_period
        for channel_data in self.data[1:]:
            self.channels.append(Channel(measurement_name=self.measurement_name,
                                         channel_name="Channel " + str(i),
                                         data=channel_data))
            i = i + 1

    def add_differential_channel(self, dif1, dif2):
        if dif1 < len(self.channels) and dif2 < len(self.channels):
            self.channels.append(Channel(measurement_name=self.measurement_name,
                                         channel_name="Differential Channel " + str(dif2) + "-" + str(dif1),
                                         data=self.channels[dif2].data - self.channels[dif1].data))

    def select_periods(self, resolution, vpp_threshold, length_threshold):
        self.selected_periods = noise_recognition(self.data, resolution, vpp_threshold)
        self.selected_periods = periods_filter(self.selected_periods, length_threshold)
        if len(self.selected_periods) == 0:
            self.status = ProcessingStatus.NO_AVAILABLE_PERIODS

    def process(self, is_spliced):
        if self.status == ProcessingStatus.DATA_READ_FROM_FILE:
            period_length = [period[1] - period[0] for period in self.selected_periods]
            single_period_length = max(period_length)
            total_length = sum(period_length)
            if is_spliced:
                self.rfft_freq = np.fft.rfftfreq(total_length, self.sampling_period)
                self.num_of_spectrums = 1
            else:
                self.rfft_freq = np.fft.rfftfreq(single_period_length, self.sampling_period)
                self.num_of_spectrums = len(self.selected_periods)
            for channel in self.channels:
                channel.process(sampling_period=self.sampling_period,
                                is_spliced=is_spliced,
                                processing_periods=self.selected_periods,
                                single_period_length=single_period_length)
            self.status = ProcessingStatus.PROCESSED

    def output_data(self, output_mode, output_path):
        if self.status == ProcessingStatus.PROCESSED:
            if output_mode == "single_spectrum" or "contrast_periods":
                for channel in self.channels:
                    save_spectrums(file_path=os.path.join(output_path, (channel.channel_name + ".csv")),
                                   rfft_freq=self.rfft_freq,
                                   spectrums=channel.spectrums,
                                   output_mode=output_mode)
            elif output_mode == "contrast_channels":
                i = 0
                for period in range(self.num_of_spectrums):
                    save_spectrums(file_path=os.path.join(output_path, ("Period " + str(i) + ".csv")),
                                   rfft_freq=self.rfft_freq,
                                   spectrums=[channel.spectrums[i] for channel in self.channels],
                                   output_mode=output_mode)
                    i = i + 1

    def plot(self, output_mode, output_path, auto, left, right):
        if self.status == ProcessingStatus.PROCESSED:
            if output_mode == "contrast_periods":
                for channel in self.channels:
                    plot_spectrums(file_path=os.path.join(output_path, (channel.channel_name + ".png")),
                                   auto=auto,
                                   left=left,
                                   right=right,
                                   title=channel.channel_name,
                                   rfft_freq=self.rfft_freq,
                                   spectrums=channel.spectrums,
                                   output_mode=output_mode)
            elif output_mode == "contrast_channels":
                i = 0
                for period in range(self.num_of_spectrums):
                    plot_spectrums(file_path=os.path.join(output_path, ("period_" + str(i) + ".png")),
                                   auto=auto,
                                   left=left,
                                   right=right,
                                   title="Period" + str(i),
                                   rfft_freq=self.rfft_freq,
                                   spectrums=[channel.spectrums[i] for channel in self.channels],
                                   output_mode=output_mode)
                    i = i + 1

    def log_to_txt(self, path):
        path = os.path.join(path, "log.txt")
        selected_periods_in_time = [(str(period[0] * self.sampling_period) + "s",
                                     str(period[1] * self.sampling_period) + "s")
                                    for period in self.selected_periods]
        if self.status == ProcessingStatus.NO_AVAILABLE_PERIODS:
            selected_periods_in_time = "No Available Periods"
        logtext = [self.measurement_name,
                   "Original File in:",
                   self.path,
                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                   "Processing Period =" + str(selected_periods_in_time),
                   "Sampling Period = " + str(self.sampling_period) + "s",
                   "Sampling Rate = " + str(int(self.sampling_rate)) + "Hz"]
        with open(path, "w") as file:
            file.writelines([line + "\n" for line in logtext])
