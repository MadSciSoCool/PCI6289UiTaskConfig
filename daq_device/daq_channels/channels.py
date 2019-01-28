import nidaqmx
from nidaqmx.constants import AcquisitionType


class Channels:
    def __init__(self, device_name):
        self.device_name = device_name
        self.task = nidaqmx.Task()
        self.is_on = False
        self.is_locked = False

    def rebuild_task(self, channels_config):
        self.task.close()
        self.task = nidaqmx.Task()
        self._setup_channels(channels_config)
        self.task.register_done_event(self._done_event)

    def start_task(self):
        if self.is_on:
            self.is_locked = True
            self._start()

    def close(self):
        self.task.close()

    def _done_event(self, *args):
        self.is_locked = False
        return 0

    def _start(self):
        self.task.start()
