import nidaqmx
from nidaqmx.constants import AcquisitionType


class Channels:
    def __init__(self, device_name):
        self.device_name = device_name
        self.task = nidaqmx.Task()

    def start_task(self):
        self.task.start()

    def close(self):
        self.task.close()

    def hang(self):
        self.task.stop()

    def _done_event(self, *args):
        return 0
