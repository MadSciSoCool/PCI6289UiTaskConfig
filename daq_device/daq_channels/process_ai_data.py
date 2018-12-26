import numpy as np
import matplotlib as plt
import os


def process_ai_data(acquired_data, file_path=''):
    np.savetxt(os.path.join(file_path, 'ai_acquired_data.csv'), delimiter=',')
    shape = acquired_data.shape
    for i in range(shape[0]):
        rfft_result = np.fft.rfft(acquired_data[i])


