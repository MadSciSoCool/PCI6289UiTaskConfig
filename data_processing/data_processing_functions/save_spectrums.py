import numpy as np


def save_spectrums(file_path, rfft_freq, spectrums):
    output_data = [rfft_freq]
    header = "Frequency/Hz"
    for spectrum in spectrums:
        output_data.append(spectrum.data)
        header = header + "," + spectrum.label
    output_data = np.array(output_data, dtype=np.float64)
    np.savetxt(file_path, delimiter=",", header=header, X=output_data.T)
