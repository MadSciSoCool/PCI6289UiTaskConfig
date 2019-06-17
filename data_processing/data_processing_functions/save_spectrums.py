import numpy as np


def save_spectrums(file_path, rfft_freq, spectrums, output_mode):
    output_data = [rfft_freq]
    header = "Frequency/Hz"
    for spectrum in spectrums:
        output_data.append(spectrum.data)
        if output_mode == "contrast_periods" or "single_spectrum":
            header = header + "," + spectrum.period + "/dBm"
        elif output_mode == "contrast_channels":
            header = header + "," + spectrum.channel + "/dBm"
    output_data = np.array(output_data, dtype=np.float64)
    np.savetxt(file_path, delimiter=",", header=header, X=output_data.T)
