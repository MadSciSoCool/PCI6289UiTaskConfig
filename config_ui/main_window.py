from enum import Enum
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QPushButton,
                             QApplication, QAction, QComboBox, QLabel, QCheckBox, QFileDialog)
from config_ui.input_widget import NoTitleDoubleInputWidget, NoTitleIntegerInputWidget
from config_ui.edit_digital_waveform_dialog import EditDigitalWaveformDialog


class Status(Enum):
    is_started = 0
    is_paused = 1
    is_closed = 2
    is_modified = 3


class MainWindow(QMainWindow):
    def __init__(self, daq_device):
        super().__init__()
        self.daq_device = daq_device
        self.status = Status.is_closed
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NIDAQ PCI-6289 Task Configuration Interface")

        change_working_directory_act = QAction('Change Working Directory', self)
        change_working_directory_act.setShortcut('Ctrl+C')
        change_working_directory_act.setStatusTip("Change the directory of saving and loading files")
        change_working_directory_act.triggered.connect(self.change_working_directory)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")
        file_menu.addAction(change_working_directory_act)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        # The Main Window is separated into 3 parts, AI widget, AO widget and DI widget
        # The AO widget is temporarily not used
        self.ai_group = AnalogInputGroup(self.daq_device)
        # ao_group = AnalogOutputGroup()
        self.do_group = DigitalOutputGroup()

        central_layout.addWidget(self.ai_group)
        # central_layout.addWidget(ao_group)
        central_layout.addWidget(self.do_group)

        start_button = QPushButton("Start Measurement", self)
        start_button.clicked.connect(self.start_task)
        stop_button = QPushButton("Stop Measurement", self)
        stop_button.clicked.connect(self.stop_task)

        central_layout.addWidget(start_button)
        central_layout.addWidget(stop_button)

        self.do_group.edit_digital_waveform_dialog.accepted.connect(self.digital_output_accepted_event)

        self.show()

    def change_working_directory(self):
        self.path = QFileDialog.getExistingDirectory()

    def start_task(self):
        if self.status == Status.is_closed or self.status == Status.is_modified:
            self.ai_group.set_ai_channels()
            self.daq_device.start_task()
            self.status = Status.is_started
        elif self.status == Status.is_paused:
            self.daq_device.start_task()
            self.status = Status.is_started

    def stop_task(self):
        if self.status == Status.is_started:
            self.daq_device.stop_task()
            self.status = Status.is_paused

    def digital_output_accepted_event(self):
        self.daq_device.stop_task()
        self.do_group.edit_digital_waveform_dialog.hide()
        digital_sampling_rate = 1000
        self.daq_device.do_channels.set_digital_waveform(
            self.do_group.edit_digital_waveform_dialog.data_input_widget.get_digital_waveform(),
            self.do_group.edit_digital_waveform_dialog.period_time.value, digital_sampling_rate)
        self.daq_device.do_channels.timing_configuration = digital_sampling_rate
        self.status = Status.is_modified


class AnalogInputGroup(QGroupBox):
    def __init__(self, daq_device):
        super().__init__("Analog Input")
        self.daq_device = daq_device
        self.initUI()

    def initUI(self):
        ai_layout = QGridLayout()
        self.setLayout(ai_layout)
        titles = ["", "Terminal Mode", "Max Value", "Min Value", "Channel Status"]
        self.channels_name = ["Channel 1", "Channel 2", "Channel 3", "Channel 4"]
        self.terminal_mode = dict()
        self.max_value = dict()
        self.min_value = dict()
        self.terminal_status = dict()
        for i in range(len(titles)):
            ai_layout.addWidget(QLabel(titles[i], self), 0, i)
        for i in range(len(self.channels_name)):
            this_channel = self.channels_name[i]
            ai_layout.addWidget(QLabel(this_channel, self), i + 1, 0)
            self.terminal_mode[this_channel] = AIComboBox()
            self.max_value[this_channel] = NoTitleDoubleInputWidget(self, 5, "V", 0, 5, 2)
            self.min_value[this_channel] = NoTitleDoubleInputWidget(self, -5, "V", -5, 0, 2)
            self.terminal_status[this_channel] = TerminalStatusCheckbox()
            ai_layout.addWidget(self.terminal_mode[this_channel], i + 1, 1)
            ai_layout.addWidget(self.max_value[this_channel], i + 1, 2)
            ai_layout.addWidget(self.min_value[this_channel], i + 1, 3)
            ai_layout.addWidget(self.terminal_status[this_channel], i + 1, 4)
        ai_layout.addWidget(QLabel("Sampling Rate", self), len(self.channels_name) + 1, 0)
        ai_layout.addWidget(QLabel("Samples Per Channel", self), len(self.channels_name) + 1, 2)
        self.sampling_rate = NoTitleIntegerInputWidget(self, 1000, "Hz", 0, 500000, 100)
        self.samples_per_channel = NoTitleIntegerInputWidget(self, 10000, "", 0, 100000, 100)
        ai_layout.addWidget(self.sampling_rate, len(self.channels_name) + 1, 1)
        ai_layout.addWidget(self.samples_per_channel, len(self.channels_name) + 1, 3)

    def get_ai_cfg(self):
        channels = ["ai0", "ai1", "ai2", "ai3"]
        cfg = dict()
        for i in range(len(channels)):
            this_channel = channels[i]
            this_name = self.channels_name[i]
            this_cfg = dict()
            this_cfg["terminal_mode"] = self.terminal_mode[this_name].value
            this_cfg["max_value"] = self.max_value[this_name].value
            this_cfg["min_value"] = self.min_value[this_name].value
            this_cfg["terminal_status"] = self.terminal_status[this_name].value
            cfg[this_channel] = this_cfg
        return cfg

    def get_ai_timing_cfg(self):
        sampling_rate = self.sampling_rate.value
        samples_per_channel = self.samples_per_channel.value
        return (sampling_rate, samples_per_channel)

    def set_ai_channels(self):
        self.daq_device.ai_channels.rebuild_task(self.get_ai_cfg())
        self.daq_device.ai_channels.timing_configuration = self.get_ai_timing_cfg()


class DigitalOutputGroup(QGroupBox):
    def __init__(self):
        super().__init__("Digital Output")
        self.edit_digital_waveform_dialog = EditDigitalWaveformDialog()
        self.initUI()

    def initUI(self):
        do_layout = QHBoxLayout()
        self.setLayout(do_layout)
        edit_button = QPushButton("Edit Digital Waveform")
        do_layout.addWidget(edit_button)
        edit_button.clicked.connect(self.edit_digital_waveform)

    def edit_digital_waveform(self):
        self.edit_digital_waveform_dialog.show()

class AIComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItem("RSE")
        self.addItem("NRSE")
        self.addItem("DIFFERENTIAL")
        self.value = "RSE"
        self.activated[str].connect(self.save_mode)

    def save_mode(self, text):
        self.value = text


class TerminalStatusCheckbox(QCheckBox):
    def __init__(self):
        super().__init__("Enabled")
        self.value = False
        self.stateChanged.connect(self.state_change)

    def state_change(self):
        self.value = self.isChecked()


"""
class AOComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItem("SINE")
        self.addItem("SQUARE")
        self.value = "SINE"
        self.activated[str].connect(self.save_mode)

    def save_mode(self, text):
        self.value = text
"""

"""
class AnalogOutputGroup(QGroupBox):
    def __init__(self):
        super().__init__("Analog Output")
        self.initUI()

    def initUI(self):
        ao_layout = QGridLayout()
        self.setLayout(ao_layout)
        titles = ["", "Waveform", "Frequency", "Amplitude", "Channel Status"]
        channels = ["Channel 1", "Channel 2", "Channel 3", "Channel 4"]
        self.waveform = {}
        self.frequency = {}
        self.amplitude = {}
        self.terminal_status = {}
        for i in range(len(titles)):
            ao_layout.addWidget(QLabel(titles[i], self), 0, i)
        for i in range(len(channels)):
            this_channel = channels[i]
            ao_layout.addWidget(QLabel(this_channel, self), i + 1, 0)
            self.waveform[this_channel] = AOComboBox()
            self.frequency[this_channel] = NoTitleIntegerInputWidget(self, 100, "Hz", 0, 1000, 1)
            self.amplitude[this_channel] = NoTitleDoubleInputWidget(self, 5, "V", 0, 5, 2)
            self.terminal_status[this_channel] = TerminalStatusCheckbox()
            ao_layout.addWidget(self.waveform[this_channel], i + 1, 1)
            ao_layout.addWidget(self.frequency[this_channel], i + 1, 2)
            ao_layout.addWidget(self.amplitude[this_channel], i + 1, 3)
            ao_layout.addWidget(self.terminal_status[this_channel], i + 1, 4)
        ao_layout.addWidget(QLabel("Sampling Rate", self), len(channels) + 1, 0)
        ao_layout.addWidget(QLabel("Total Time", self), len(channels) + 1, 2)
        self.sampling_rate = NoTitleIntegerInputWidget(self, 1000, "Hz", 0, 10000, 100)
        self.total_time = NoTitleDoubleInputWidget(self, 10, "s", 0, 10, 1)
        ao_layout.addWidget(self.sampling_rate, len(channels) + 1, 1)
        ao_layout.addWidget(self.total_time, len(channels) + 1, 3)
"""
