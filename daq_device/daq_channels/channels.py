import nidaqmx
from .ai_channels import AIChannels


class Channels:
    def __init__(self, device_name):
        self.device_name = device_name
        self.task = nidaqmx.Task()
        self.is_locked = False
        self.task.register_done_event(self.done_callback)

    def rebuild_task(self, channels_config, **kwargs):
        self.task.close()
        self.task = nidaqmx.Task()
        self._setup_channels(channels_config)
        self._setup_task(**kwargs)
        if type(self) == AIChannels:
            self._allocate()
        self.task.register_done_event(self._done_callback)

    def start_task(self):
        self.is_locked = True
        self.task.start()
        self.task.wait_until_done(timeout=20.0)
        self.task.stop()

    def _done_event(self, *args):
        self.is_locked = False

    def set_sample_rate(self, rate, source=''):
        try:
            self.task.timing.cfg_samp_clk_timing(rate=rate, source=source)
        except nidaqmx.errors.DaqError:
            print('Invalid sampling rate/source')
