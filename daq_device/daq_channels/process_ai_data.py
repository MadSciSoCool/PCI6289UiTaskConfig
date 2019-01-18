import numpy as np
import matplotlib.pyplot as plt
import os


def process_ai_data(acquired_data, file_path='', sample_rate=1000):
    np.savetxt(os.path.join(file_path, 'ai_acquired_data.csv'), delimiter=',')
    shape = acquired_data.shape
    num_of_channels = shape[0]
    num_of_samples = shape[1]
    for i in range(num_of_channels):
        rfft_result = np.fft.rfft(acquired_data[i])
        rfft_freq = np.fft.rfftfreq(num_of_samples, 1. / sample_rate)
        plt.plot(rfft_freq, rfft_result.real, label="real part")
        plt.plot(rfft_freq, rfft_result.imag, label="imaginary part")
        plt.xlabel("Frequency/Hz")
        plt.ylabel("Amplitude/V*s")
        plt.legend(loc="upper right")
        plt.savefig('channel' + str(i) + '.png', dpi=300)
        plt.cla()
