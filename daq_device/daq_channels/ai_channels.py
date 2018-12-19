
import nidaqmx

class AIChannels:

    def __init__(self, num_of_channels):
        if num_of_channels > 32:
            self.num_of_channels = 32
        else:
            self.num_of_channels = num_of_channels
        self.ai_task = nidaqmx.Task()

