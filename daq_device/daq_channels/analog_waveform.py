import numpy as np


def sine_wave(sample_rate, freq, amplitude, total_time):
    length = int(total_time * sample_rate)
    time_seq = np.arange(0, length) * 2 * np.pi * freq / sample_rate
    voltage_seq = amplitude * np.sin(time_seq)
    return voltage_seq


def square_wave(sample_rate, freq, amplitude, total_time):
    length = int(total_time * sample_rate)
    number_of_points_per_half_period = int(sample_rate / (2 * freq))
    voltage_seq_per_period = np.hstack((amplitude * np.ones(number_of_points_per_half_period),
                                        -amplitude * np.ones(number_of_points_per_half_period)))
    voltage_seq = np.empty(0)
    while np.size(voltage_seq) < length:
        voltage_seq = np.hstack((voltage_seq, voltage_seq_per_period))
    return voltage_seq


def analog_waveform(channels_config, sample_rate):
    waveform = []
    for channel_name, config in channels_config.items():
        if config[type] == 'sine':
            this_waveform = sine_wave(sample_rate=sample_rate,
                                      freq=config['freq'],
                                      amplitude=config['amplitude'],
                                      total_time=config['total_time'])
        elif config[type] == 'square':
            this_waveform = square_wave(sample_rate=sample_rate,
                                        freq=config['freq'],
                                        amplitude=config['amplitude'],
                                        total_time=config['total_time'])
        waveform.append(this_waveform)
    return np.array(waveform)
