import nidaqmx
from nidaqmx.constants import AcquisitionType


class Channels:
    def __init__(self, device_name):
        self.device_name = device_name
        self.task = nidaqmx.Task()
        self.is_locked = False

    def rebuild_task(self, channels_config):
        self.task.close()
        self.task = nidaqmx.Task()
        self._setup_channels(channels_config)
        self.task.register_done_event(self._done_event)

    def start_task(self, **kwargs):
        self.is_locked = True
        self._start(kwargs)

    def close(self):
        self.task.close()

    def _done_event(self, *args):
        self.is_locked = False
        return 0

    def _start(self, **kwargs):
        self.task.start()
