import numpy as np


class Spectrum:
    def __init__(self, label, data):
        self.label = label
        self.data = data

def splice_data(data, selected_periods):
    selected_data = np.array([])
    for period in selected_periods:
        start, end = period
        selected_data = np.append(selected_data, data[start:end])
    return selected_data

def spectrum_analyze(label, sampling_rate, data):
    delta_t = 1. / sampling_rate
    T = len(data) / sampling_rate
    rfft_result = np.abs(np.fft.rfft(data))
    PSD = (delta_t ** 2) * np.square(rfft_result) / T
    PSD_dBm = 10 * np.log10(PSD * 1000)
    return Spectrum(label, PSD_dBm)
