import numpy as np
import os


def save_ai_data(acquired_data, file_path, measurement_no, sampling_rate):
    file_path = os.path.join(file_path, "measurement" + str(measurement_no))
    try:
        os.mkdir(file_path)
    except FileExistsError:
        pass
    shape = acquired_data.shape
    num_of_channels = shape[0]
    num_of_samples = shape[1]
    # write the original data
    time_axis = np.array([i / sampling_rate for i in range(num_of_samples)])
    original_output_data = np.vstack((time_axis, acquired_data)).T
    header = ["time/s"] + ["ai" + str(i) + "/V" for i in range(num_of_channels)]
    np.savetxt(os.path.join(file_path, "ai_acquired_data.csv"),
               delimiter=",",
               header=",".join(header),
               X=original_output_data)
