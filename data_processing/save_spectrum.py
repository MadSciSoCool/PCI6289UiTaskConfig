import numpy as np


def save_spectrum(file_path, *spectrums):
    output_data = []
    header = "Frequency"
    for spectrum in spectrums:
        rfft_freq, PSD_dbm, label = spectrum
        output_data.append(PSD_dbm)
        header = header + "," + label
    np.savetxt(file_path, delimiter=",", header=header, X=output_data.T)
