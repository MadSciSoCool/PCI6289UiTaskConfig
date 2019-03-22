import numpy as np


def analog_waveform_convert(analog_waveform_settings, period, sampling_rate):
    number_of_channels = len(analog_waveform_settings)
    total_points = int(sampling_rate * period / 1000)  # 1000 is for 1ms scale division
    sampling_period = 1000 / sampling_rate
    waveform = np.empty([number_of_channels, total_points], dtype=np.float64)
    cursor_y = 0
    for channel_cfg in analog_waveform_settings.values():
        time_cfg = channel_cfg["time"]
        low = channel_cfg["low"]
        high = channel_cfg["high"]
        # generate the analog waveform
        flag = 0
        cursor_x = 0
        for time in time_cfg:
            for i in range(int(time / sampling_period)):
                waveform[cursor_y, cursor_x] = (high - low) * flag + low
                cursor_x = cursor_x + 1
            flag = 1 - flag
            for i in range(cursor_x, total_points):
                waveform[cursor_y, i] = low
        cursor_y = cursor_y + 1
    return waveform
    # remain to be fixed: if length > period
