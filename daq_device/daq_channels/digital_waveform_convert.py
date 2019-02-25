import numpy as np


def digital_waveform_convert(digital_waveform_configuration, sampling_rate):
    number_of_lines = len(digital_waveform_configuration)
    maximum_length = max([sum(i) for i in digital_waveform_configuration])
    total_points = int(sampling_rate * maximum_length / 1000)  # 1000 is for 1ms scale division
    sampling_period = 1000 / sampling_rate  # 1000 is for 1ms scale division
    uint32_waveform = np.empty(total_points, dtype=np.uint32)
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
    # add up raw waveform to a uint32 sequence
    for i in range(total_points):
        uint32_waveform[i] = 0
        for j in range(number_of_lines):
            if raw_waveform[i][j]:
                uint32_waveform = uint32_waveform + 2 ** j
    return (total_points, uint32_waveform)
