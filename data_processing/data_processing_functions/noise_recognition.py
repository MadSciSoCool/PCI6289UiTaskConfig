import numpy as np


def ppm(data):
    return np.max(data) - np.min(data)


def noise_recognition(acquired_data, resolution, threshold):
    rows, columns = acquired_data.shape
    selected_periods = []
    for i in range(1, rows):
        selected_periods_this_channel = []
        this_channel = acquired_data[i]
        ppms = np.array([])
        while len(this_channel) > resolution:
            ppms = np.append(ppms, ppm(this_channel[:resolution]))
            this_channel = this_channel[resolution:]
        max = np.max(ppms)
        this_threshold = max * threshold
        pos = 0
        iter_ppms = iter(ppms)
        last_marker = False
        while True:
            try:
                this_ppm = next(iter_ppms)
                this_marker = this_ppm < this_threshold
                if this_marker != last_marker:
                    selected_periods_this_channel.append(pos)
                last_marker = this_marker
                pos = pos + resolution
            except StopIteration:
                if this_ppm < this_threshold:
                    selected_periods_this_channel.append(columns)
                break
        selected_periods.append(selected_periods_this_channel)
    return [[(selected_periods[i][2 * j], selected_periods[i][2 * j + 1]) for j in range(len(selected_periods[i]) // 2)]
            for i in range(len(selected_periods))]


if __name__ == "__main__":
    file_path = r"C:\Users\LYClab\Desktop\2015-4-15\measurement2\ai_acquired_data.csv"
    data = np.loadtxt(file_path, delimiter=",")
    print(noise_recognition(acquired_data=data.T, resolution=2000, threshold=0.3))
