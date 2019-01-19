import numpy as np


def sine_wave(sample_rate, freq, amplitude, total_time):
    length = int(total_time * sample_rate)
    time_seq = np.arrange(0, length) * 2 * np.pi * freq / sample_rate
    voltage_seq = amplitude * np.sin(time_seq)
    return voltage_seq


def square_wave(sample_rate, freq, amplitude, total_time):
    number_of_periods = int(total_time * freq)
    number_of_points_per_half_period = int(sample_rate / (2 * freq))
    voltage_seq_per_period = np.hstack((amplitude * np.ones(number_of_points_per_half_period),
                                        -amplitude * np.ones(number_of_points_per_half_period)))
    voltage_seq = np.empty(0)
    for i in range(number_of_periods):
        voltage_seq = np.hstack(voltage_seq, voltage_seq_per_period)
    return voltage_seq
