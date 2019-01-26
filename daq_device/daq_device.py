from .daq_channels.ai_channels import AIChannels
from .daq_channels.ao_channels import AOChannels
from .daq_channels.do_channels import DOChannels


class DaqDevice:

    def __init__(self, device_name):
        self.ai_channels = AIChannels(device_name=device_name)
        self.ao_channels = AOChannels(device_name=device_name)
        self.do_channels = DOChannels(device_name=device_name)

    def start_measurement(self):
        self.ai_channels.start_task()
        self.ao_channels.start_task()
        self.do_channels.start_task()

    def close(self):
        self.ai_channels.close()
        self.ao_channels.close()
        self.do_channels.close()

    @property
    def is_locked(self):
        return self._is_locked

    @property.getter
    def is_locked(self):
        if self.ai_channels.is_locked:
            return True
        elif self.ao_channels.is_locked:
            return True
        elif self.do_channels.is_locked:
            return True
        else:
            return False
