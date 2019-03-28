import numpy as np
import matplotlib.pyplot as plt
import os


def process_ai_data(acquired_data, file_path, sampling_rate, period_time, min_frequency, max_frequency,
                    fft_start, fft_end, enable_plot, measurement_no):
    file_path = os.path.join(file_path, "measurement" + str(measurement_no))
    os.mkdir(file_path)
    shape = acquired_data.shape
    num_of_channels = shape[0]
    num_of_samples = shape[1]
    # write the original data
    time_axis = np.array([i / sampling_rate for i in range(num_of_samples)])
    original_output_data = np.vstack((time_axis, acquired_data)).T
    header = ["time/s"] + ["ai" + str(i) + "/V" for i in range(num_of_channels)]
    np.savetxt(os.path.join(file_path, "ai_acquired_data.csv"),
               delimiter=",",
               header=",".join(header),
               X=original_output_data)
    # handle default start and end position
    if fft_start < 0:
        fft_start = 0
    if fft_end < 0:
        fft_end = period_time
    # convert time into number of points
    points_per_period = int(period_time * sampling_rate / 1000)
    fft_start_pos = int(fft_start * sampling_rate / 1000)
    fft_end_pos = int(fft_end * sampling_rate / 1000)
    delta_t = 1. / sampling_rate
    T = (fft_end - fft_start) / 1000.
    rfft_freq = np.fft.rfftfreq(fft_end_pos - fft_start_pos, delta_t)
    for i in range(num_of_channels):
        # turn the unit from V to dBm
        data_this_channel = acquired_data[i]
        period_no = 0
        spectrum_output_data = rfft_freq.copy()
        while len(data_this_channel) >= points_per_period:
            period_no = period_no + 1
            data_this_period = data_this_channel[fft_start_pos:fft_end_pos]
            rfft_result = np.abs(np.fft.rfft(data_this_period))
            PSD = (delta_t ** 2) * np.square(rfft_result) / T
            PSD_dBm = 10 * np.log10(PSD * 1000)
            if enable_plot:
                plt.plot(rfft_freq, PSD_dBm, label="Power Spectrum Density")
                if min_frequency >= 0:
                    plt.xlim(xmin=min_frequency)
                if max_frequency >= 0:
                    plt.xlim(xmax=max_frequency)
                plt.xlabel("Frequency/Hz")
                plt.ylabel("Power Spectrum Density/dBm")
                plt.savefig(os.path.join(file_path, 'channel_' + str(i) + "_period_" + str(period_no) + '.png'),
                            dpi=300)
                plt.cla()
            spectrum_output_data = np.vstack((spectrum_output_data, PSD_dBm))
            data_this_channel = data_this_channel[points_per_period:]
        header = np.array(["Frequency/Hz"] + ["period" + str(i + 1) + "/dBm" for i in range(period_no)])
        np.savetxt(os.path.join(file_path, "ai_power_density_spectrum_" + str(i) + ".csv"),
                   delimiter=",",
                   header=",".join(header),
                   X=spectrum_output_data.T)
