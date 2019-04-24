import numpy as np


def single_spectrum_analyze(data, sampling_rate, label, *selected_periods):
    selected_data = np.array([])
    number_of_samples = 0
    for period in selected_periods:
        start, end = period
        number_of_samples = number_of_samples + end - start
        selected_data = np.append(selected_data, data[start:end])
    delta_t = 1. / sampling_rate
    T = number_of_samples / sampling_rate
    rfft_freq = np.fft.rfftfreq(number_of_samples, delta_t)
    rfft_result = np.abs(np.fft.rfft(selected_data))
    PSD = (delta_t ** 2) * np.square(rfft_result) / T
    PSD_dBm = 10 * np.log10(PSD * 1000)
    return rfft_freq, PSD_dBm, label
