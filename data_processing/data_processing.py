import numpy as np
from .find_files import find_files
from .noise_recognition import noise_recognition

def data_processing(file_mode, file_path, key_name):
    files = find_files(file_mode, file_path, key_name)
    for dir, file in files:
        try:
            data = np.loadtxt(file, delimiter=",", skiprows=1)
        except Exception as e:
            print(e)
        selected_periods = noise_recognition(data)
