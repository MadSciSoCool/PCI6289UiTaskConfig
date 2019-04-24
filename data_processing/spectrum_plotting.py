import matplotlib as plt


def plot_spectrum(file_path, left, right, title, *spectrums):
    plt.style.use("dark background")
    plt.title(title)
    for spectrum in spectrums:
        rfft_freq, PSD_dbm, label = spectrum
        plt.plot(rfft_freq, PSD_dbm, label=label, linewidth = 0.3)
    if left >= 0:
            plt.xlim(left=left)
    if right >= 0:
            plt.xlim(right=right)
    plt.legend()
    plt.xlabel("Frequency/Hz")
    plt.ylabel("Power Spectrum Density/dBm")
    plt.savefig(file_path, dpi=300)
    plt.cla()
