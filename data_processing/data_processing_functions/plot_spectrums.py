import matplotlib.pyplot as plt


def plot_spectrums(file_path, auto, left, right, title, rfft_freq, spectrums, output_mode):
    plt.style.use("dark_background")
    plt.title(title)
    for spectrum in spectrums:
        if output_mode == "contrast_periods":
            plt.plot(rfft_freq, spectrum.data, label=spectrum.period, linewidth=0.3)
        elif output_mode == "contrast_channels":
            plt.plot(rfft_freq, spectrum.data, label=spectrum.channel, linewidth=0.3)
    if not auto:
        plt.xlim(left=left, right=right)
    plt.legend()
    plt.xlabel("Frequency/Hz")
    plt.ylabel("Power Spectrum Density/dBm")
    plt.savefig(file_path, dpi=300)
    plt.cla()
