import numpy as np
from scipy.signal.windows import flattop, blackman


class Spectrum:
    def __init__(self, period, channel, data):
        self.period = period
        self.channel = channel
        self.data = data


def splice_data(data, selected_periods):
    selected_data = np.array([])
    for period in selected_periods:
        start, end = period
        selected_data = np.append(selected_data, data[start:end])
    return selected_data


def spectrum_analyze(period, channel, sampling_period, data):
    num_of_samps = len(data)
    window = np.hanning(num_of_samps)
    T = num_of_samps * sampling_period
    rfft_result = np.abs(np.fft.rfft(data * window))
    PSD = (sampling_period ** 2) * np.square(rfft_result) / T
    PSD_dBm = 10 * np.log10(PSD * 1000)
    return Spectrum(period, channel, PSD_dBm)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    file = r"C:\Users\LYClab\Desktop\2019-5-24\measurement6\ai_acquired_data.csv"
    savepath = r"C:\Users\LYClab\Desktop\2019-5-24\measurement6\spectrum.csv"
    data = np.loadtxt(file, delimiter=",", skiprows=1).T
    rate = 1. / (2 * (10 ** -5))
    data = data[1]
    spectrum = spectrum_analyze("1", "2", rate, data).data
    freq = np.fft.rfftfreq(len(data), 2 * (10 ** -5))
    output = np.array([freq, spectrum])
    np.savetxt(savepath, delimiter=",", X=output.T)
    plt.plot(freq, spectrum)
    plt.xlim(right=100, left=0)
    plt.show()
    plt.cla()
