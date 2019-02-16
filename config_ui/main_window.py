import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QPushButton,
                             QApplication, QMenuBar, QComboBox, QLabel, QCheckBox)
from input_widget import NoTitleDoubleInputWidget, NoTitleIntegerInputWidget
from edit_digital_waveform_dialog import EditDigitalWaveformDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NIDAQ PCI-6289 Task Configuration Interface")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        ai_group = AnalogInputGroup()
        ao_group = AnalogOutputGroup()
        do_group = DigitalOutputGroup()

        central_layout.addWidget(ai_group)
        central_layout.addWidget(ao_group)
        central_layout.addWidget(do_group)

        start_button = QPushButton("Start Measurement", self)
        central_layout.addWidget(start_button)

        self.show()


# The Main Window is separated into 3 parts, AI widget, AO widget and DI widget

class AnalogInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("Analog Input")
        self.initUI()

    def initUI(self):
        ai_layout = QGridLayout()
        self.setLayout(ai_layout)
        titles = ["", "Terminal Mode", "Max Value", "Min Value", "Channel Status"]
        channels = ["Channel 1", "Channel 2", "Channel 3", "Channel 4"]
        self.terminal_mode = {}
        self.max_value = {}
        self.min_value = {}
        self.terminal_status = {}
        for i in range(len(titles)):
            ai_layout.addWidget(QLabel(titles[i], self), 0, i)
        for i in range(len(channels)):
            this_channel = channels[i]
            ai_layout.addWidget(QLabel(this_channel, self), i + 1, 0)
            self.terminal_mode[this_channel] = AIComboBox()
            self.max_value[this_channel] = NoTitleDoubleInputWidget(self, 5, "V", 0, 5, 2)
            self.min_value[this_channel] = NoTitleDoubleInputWidget(self, -5, "V", -5, 0, 2)
            self.terminal_status[this_channel] = TerminalStatusCheckbox()
            ai_layout.addWidget(self.terminal_mode[this_channel], i + 1, 1)
            ai_layout.addWidget(self.max_value[this_channel], i + 1, 2)
            ai_layout.addWidget(self.min_value[this_channel], i + 1, 3)
            ai_layout.addWidget(self.terminal_status[this_channel], i + 1, 4)
        ai_layout.addWidget(QLabel("Sampling Rate", self), len(channels) + 1, 0)
        ai_layout.addWidget(QLabel("Samples Per Channel", self), len(channels) + 1, 2)
        self.sampling_rate = NoTitleIntegerInputWidget(self, 1000, "Hz", 0, 500000, 100)
        self.samples_per_channel = NoTitleIntegerInputWidget(self, 10000, "", 0, 100000, 100)
        ai_layout.addWidget(self.sampling_rate, len(channels) + 1, 1)
        ai_layout.addWidget(self.samples_per_channel, len(channels) + 1, 3)


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
            self.waveform[this_channel] = AIComboBox()
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


class DigitalOutputGroup(QGroupBox):
    def __init__(self):
        super().__init__("Digital Output")
        self.initUI()

    def initUI(self):
        do_layout = QHBoxLayout()
        self.setLayout(do_layout)
        edit_button = QPushButton("Edit Digital Waveform")
        do_layout.addWidget(edit_button)
        edit_button.clicked.connect(self.edit_digital_waveform)

    def edit_digital_waveform(self):
        self.edit_digital_waveform_dialog = EditDigitalWaveformDialog()
        self.edit_digital_waveform_dialog.accepted.connect(self.accepted_event)

    def accepted_event(self):
        pass


class AIComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItem("RSE")
        self.addItem("NRSE")
        self.addItem("DIFFERENTIAL")
        self.terminal_mode = "RSE"
        self.activated[str].connect(self.save_mode)

    def save_mode(self, text):
        self.terminal_mode = text


class AOComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItem("SINE")
        self.addItem("SQUARE")
        self.terminal_mode = "SINE"
        self.activated[str].connect(self.save_mode)

    def save_mode(self, text):
        self.terminal_mode = text


class TerminalStatusCheckbox(QCheckBox):
    def __init__(self):
        super().__init__("Enabled")
        self.stateChanged.connect(self.state_change)

    def state_change(self):
        self.is_enabled = self.isChecked()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = MainWindow()
    sys.exit(app.exec_())
