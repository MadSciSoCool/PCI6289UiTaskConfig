from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QComboBox, QCheckBox
from .input_widget import NoTitleIntegerInputWidget


class AnalogInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("Analog Input")
        self.initUI()

    def initUI(self):
        ai_layout = QGridLayout()
        self.setLayout(ai_layout)
        titles = ["", "Terminal Mode", "Range", "Channel Status"]
        modes = ["RSE", "NRSE", "DIFFERENTIAL"]
        ranges = ["±10V", "±5V", "±2V", "±1V", "±0.5V", "±0.2V", "±0.1V"]
        self.channels_name = ["ai0", "ai1", "ai2", "ai3"]
        self.terminal_mode = dict()
        self.range = dict()
        self.terminal_status = dict()
        for i in range(len(titles)):
            ai_layout.addWidget(QLabel(titles[i], self), 0, i)
        for i in range(len(self.channels_name)):
            this_channel = self.channels_name[i]
            ai_layout.addWidget(QLabel(this_channel, self), i + 1, 0)
            self.terminal_mode[this_channel] = QComboBox(self)
            self.terminal_mode[this_channel].addItems(modes)
            self.range[this_channel] = QComboBox(self)
            self.range[this_channel].addItems(ranges)
            self.terminal_status[this_channel] = QCheckBox("ENABLE", self)
            ai_layout.addWidget(self.terminal_mode[this_channel], i + 1, 1)
            ai_layout.addWidget(self.range[this_channel], i + 1, 2)
            ai_layout.addWidget(self.terminal_status[this_channel], i + 1, 3)
        ai_layout.addWidget(QLabel("Sampling Rate", self), len(self.channels_name) + 1, 0)
        ai_layout.addWidget(QLabel("Samples Per Channel", self), len(self.channels_name) + 1, 2)
        self.sampling_rate = NoTitleIntegerInputWidget(self, 50000, "Hz", 0, 500000, 100)
        self.samples_per_channel = NoTitleIntegerInputWidget(self, 500000, "", 0, 5000000, 100)
        ai_layout.addWidget(self.sampling_rate, len(self.channels_name) + 1, 1)
        ai_layout.addWidget(self.samples_per_channel, len(self.channels_name) + 1, 3)

    def get_ai_cfg(self):
        cfg = dict()
        for name in self.channels_name:
            this_cfg = dict()
            this_cfg["terminal_mode"] = self.terminal_mode[name].currentText()
            this_cfg["range"] = self.range[name].currentText()
            this_cfg["terminal_status"] = self.terminal_status[name].isChecked()
            cfg[name] = this_cfg
        return cfg

    def get_ai_timing_cfg(self):
        sampling_rate = self.sampling_rate.value
        samples_per_channel = self.samples_per_channel.value
        return (sampling_rate, samples_per_channel)

    def set_ai_cfg(self, cfg):
        for key, value in cfg.items():
            self.terminal_mode[key].setCurrentText(value["terminal_mode"])
            self.range[key].setCurrentText(value["range"])
            self.terminal_status[key].setChecked(value["terminal_status"])

    def set_ai_timing_cfg(self, cfg):
        sampling_rate, samples_per_channel = cfg
        self.sampling_rate.set_value(sampling_rate)
        self.samples_per_channel.set_value(samples_per_channel)
