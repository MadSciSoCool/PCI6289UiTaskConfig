import numpy as np
import matplotlib.pyplot as plt
import os


def process_ai_data(acquired_data, file_path='', sampling_rate=1000):
    shape = acquired_data.shape
    num_of_channels = shape[0]
    num_of_samples = shape[1]
    time_axis = np.array([i / sampling_rate for i in range(num_of_samples)])
    output_data = np.vstack((time_axis, acquired_data)).T
    np.savetxt(os.path.join(file_path, 'ai_acquired_data.csv'), delimiter=',', X=output_data)
    delta_t = 1 / sampling_rate
    T = num_of_samples / sampling_rate
    for i in range(num_of_channels):
        # turn the unit from V to dBm
        rfft_result = np.abs(np.fft.rfft(acquired_data[i]))
        PSD = (delta_t ** 2) * np.square(rfft_result) / T
        PSD_dBm = 10 * np.log10(PSD * 1000)
        rfft_freq = np.fft.rfftfreq(num_of_samples, 1. / sampling_rate)
        plt.plot(rfft_freq, PSD_dBm, label="Power Spectrum Density")
        plt.xlabel("Frequency/Hz")
        plt.ylabel("Power Spectrum Density/dBm")
        plt.savefig('channel' + str(i) + '.png', dpi=300)
        plt.cla()
        np.savetxt(os.path.join(file_path, 'ai_power_density_spectrum.csv'),
                   delimiter=',',
                   X=np.vstack((rfft_freq, PSD_dBm)).T)
