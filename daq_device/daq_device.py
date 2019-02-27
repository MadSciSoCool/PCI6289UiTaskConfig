from .daq_channels.ai_channels import AIChannels
# from .daq_channels.ao_channels import AOChannels
from .daq_channels.do_channels import DOChannels


class DaqDevice:

    def __init__(self, device_name):
        self.ai_channels = AIChannels(device_name=device_name)
        # self.ao_channels = AOChannels(device_name=device_name)
        self.do_channels = DOChannels(device_name=device_name)

    def start_task(self):
        self.ai_channels.start_task()
        self.do_channels.start_task()

    def stop(self):
        self.ai_channels.task.stop()
        self.do_channels.hang()
