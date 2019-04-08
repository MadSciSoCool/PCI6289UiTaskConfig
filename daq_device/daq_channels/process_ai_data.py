import numpy as np
import matplotlib.pyplot as plt
import os


def process_ai_data(acquired_data, file_path, sampling_rate, period_time, min_frequency, max_frequency,
                    fft_start, fft_end, enable_plot, dif_mode, measurement_no, spliced):
    # in dif_mode (if dif_mode == True) the data processing script will do (2nd channel - 1st channel) and do fft on
    # this new signal
    file_path = os.path.join(file_path, "measurement" + str(measurement_no))
    try:
        os.mkdir(file_path)
    except FileExistsError:
        pass
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
    # handle dif_mode
    if dif_mode:
        if num_of_channels >= 2:
            acquired_data[0] = acquired_data[1] - acquired_data[0]
            np.delete(acquired_data, 1, axis=0)
            num_of_channels = num_of_channels - 1
    # convert time into number of points
    points_per_period = int(period_time * sampling_rate / 1000)
    fft_start_pos = int(fft_start * sampling_rate / 1000)
    fft_end_pos = int(fft_end * sampling_rate / 1000)
    delta_t = 1. / sampling_rate
    T = (fft_end - fft_start) / 1000.
    rfft_freq = np.fft.rfftfreq(fft_end_pos - fft_start_pos, delta_t)
    for i in range(num_of_channels):
        if spliced:
            spliced_data = np.array([])
        # turn the unit from V to dBm
        data_this_channel = acquired_data[i]
        period_no = 0
        spectrum_output_data = rfft_freq.copy()
        while len(data_this_channel) >= points_per_period:
            period_no = period_no + 1
            data_this_period = data_this_channel[fft_start_pos:fft_end_pos]
            if spliced:
                spliced_data = np.append(spliced_data, data_this_period)
            rfft_result = np.abs(np.fft.rfft(data_this_period))
            PSD = (delta_t ** 2) * np.square(rfft_result) / T
            PSD_dBm = 10 * np.log10(PSD * 1000)
            if enable_plot:
                plt.style.use('dark_background')
                plt.plot(rfft_freq, PSD_dBm, label="Power Spectrum Density", linewidth=0.4)
                if min_frequency >= 0:
                    plt.xlim(left=min_frequency)
                if max_frequency >= 0:
                    plt.xlim(right=max_frequency)
                plt.xlabel("Frequency/Hz")
                plt.ylabel("Power Spectrum Density/dBm")
                if i == 0 and dif_mode:
                    plt.savefig(os.path.join(file_path, "differential_period_" + str(period_no) + ".png"),
                                dpi=300)
                else:
                    plt.savefig(os.path.join(file_path, 'channel_' + str(i) + "_period_" + str(period_no) + '.png'),
                                dpi=300)
                plt.cla()
            spectrum_output_data = np.vstack((spectrum_output_data, PSD_dBm))
            data_this_channel = data_this_channel[points_per_period:]
        header = np.array(["Frequency/Hz"] + ["period" + str(i + 1) + "/dBm" for i in range(period_no)])
        if i == 0 and dif_mode:
            np.savetxt(os.path.join(file_path, "differential_ai_power_density_spectrum.csv"),
                       delimiter=",",
                       header=",".join(header),
                       X=spectrum_output_data.T)
        else:
            np.savetxt(os.path.join(file_path, "ai_power_density_spectrum_" + str(i) + ".csv"),
                       delimiter=",",
                       header=",".join(header),
                       X=spectrum_output_data.T)
        if spliced:
            spliced_len = len(spliced_data)
            spliced_T = spliced_len * sampling_rate
            spliced_rfft_freq = np.fft.rfftfreq(spliced_len, delta_t)
            spliced_rfft_result = np.abs(np.fft.rfft(spliced_data))
            spliced_PSD = (delta_t ** 2) * np.square(spliced_rfft_result) / spliced_T
            spliced_PSD_dBm = 10 * np.log10(spliced_PSD * 1000)
            header = np.array(["Frequency/Hz", "spliced_spectrum/dBm"])
            np.savetxt(os.path.join(file_path, "spliced_ai_power_density_spectrum_"+str(i)+".csv"),
                       delimiter=",",
                       header=",".join(header),
                       X=np.vstack((spliced_rfft_freq,spliced_PSD_dBm)).T)
