
import nidaqmx
from nidaqmx.stream_writers import DigitalMultiChannelWriter

class DOChannels:

    def __init__(self, num_of_channels):
        if num_of_channels > 32:
            self.num_of_channels = 32
        else:
            self.num_of_channels = num_of_channels
        self.do_task = nidaqmx.Task()
        self.do_task.do_channels.add_do_chan()

    def select_clock_source(self):
        pass

    def load_do_wave_form(self, file_path):
        pass

    def start_writting(self):
        pass



