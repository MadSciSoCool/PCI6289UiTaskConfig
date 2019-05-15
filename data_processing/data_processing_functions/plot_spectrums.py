import matplotlib.pyplot as plt


def plot_spectrums(file_path, auto, left, right, title, rfft_freq, spectrums):
    plt.style.use("dark_background")
    plt.title(title)
    for spectrum in spectrums:
        plt.plot(rfft_freq, spectrum.data, label=spectrum.label, linewidth=0.3)
    if not auto:
        plt.xlim(left=left)
        plt.xlim(right=right)
    plt.legend()
    plt.xlabel("Frequency/Hz")
    plt.ylabel("Power Spectrum Density/dBm")
    plt.savefig(file_path, dpi=300)
    plt.cla()
