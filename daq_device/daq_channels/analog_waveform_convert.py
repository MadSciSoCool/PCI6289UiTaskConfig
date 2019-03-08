import numpy as np


def analog_waveform_convert(analog_waveform_configuration, period, sampling_rate):
    number_of_channels = len(analog_waveform_configuration)
    maximum_length = max([sum(i) for i in analog_waveform_configuration])
    if maximum_length > period:
        print("The given waveform is longer than the period")
    total_points = int(sampling_rate * period / 1000)  # 1000 is for 1ms scale division
    if total_points < 50:
        return np.zeros((number_of_channels, 50), dtype=np.float64)
    sampling_period = 1000 / sampling_rate
    analog_waveform = np.empty([number_of_channels, total_points], dtype=np.float64)
    # generate the analog waveform
    cursor_y = 0
    for cfg in analog_waveform_configuration:
        flag = 0
        cursor_x = 0
        for time in cfg:
            for i in range(int(time / sampling_period)):
                analog_waveform[cursor_y, cursor_x] = -5 * flag
                cursor_x = cursor_x + 1
            flag = 1 - flag
            for i in range(cursor_x, total_points):
                analog_waveform[cursor_y, i] = 0
        cursor_y = cursor_y + 1
    return analog_waveform
