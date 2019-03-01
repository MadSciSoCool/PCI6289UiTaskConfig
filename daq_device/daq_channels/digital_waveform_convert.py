import numpy as np


def digital_waveform_convert(digital_waveform_configuration, period, sampling_rate):
    number_of_lines = len(digital_waveform_configuration)
    maximum_length = max([sum(i) for i in digital_waveform_configuration])
    if maximum_length > period:
        print("The given waveform is longer than the period")
    total_points = int(sampling_rate * period / 1000)  # 1000 is for 1ms scale division
    if total_points < 50:
        return np.zeros(50, dtype=np.uint32)
    sampling_period = 1000 / sampling_rate  # 1000 is for 1ms scale division
    uint32_waveform = np.zeros(total_points, dtype=np.uint32)
    raw_waveform = np.empty([total_points, number_of_lines], dtype=bool)
    # generate a bool raw waveform for each line
    cursor_y = 0
    for cfg in digital_waveform_configuration:
        flag = False
        cursor_x = 0
        for time in cfg:
            for i in range(int(time / sampling_period)):
                raw_waveform[cursor_x, cursor_y] = flag
                cursor_x = cursor_x + 1
            flag = not flag
            for i in range(cursor_x, total_points):
                raw_waveform[i, cursor_y] = False
        cursor_y = cursor_y + 1
    # add up raw waveform to get a uint32 sequence
    for i in range(total_points):
        uint32_waveform[i] = 0
        for j in range(number_of_lines):
            if raw_waveform[i][j]:
                uint32_waveform[i] = uint32_waveform[i] + 2 ** j
    return uint32_waveform
