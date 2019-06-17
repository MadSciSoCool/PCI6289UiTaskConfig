import os
from .data_processing_objects import Measurement
from .find_files import find_files


def data_process(output_path, mode, path, key, resolution, vpp_threshold, length_threshold, enable_differential,
                 dif1, dif2, is_spliced, output_mode, auto, left, right):
    print("Start Processing!")
    os.makedirs(output_path, exist_ok=True)
    if find_files(mode, path, key) is not None:
        for dir, file in find_files(mode, path, key).items():
            print("Now Processing file: " + file)
            subpath = os.path.join(output_path, dir)
            os.makedirs(subpath, exist_ok=True)
            measurement = Measurement(path=file, measurement_name=dir)
            measurement.select_periods(resolution, vpp_threshold, length_threshold)
            if enable_differential:
                measurement.add_differential_channel(dif1, dif2)
            measurement.process(is_spliced)
            measurement.output_data(output_mode, subpath)
            measurement.plot(output_mode, subpath, auto, left, right)
            measurement.log_to_txt(subpath)
    print("Processing Done!")
