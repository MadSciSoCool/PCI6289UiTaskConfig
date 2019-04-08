from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QComboBox, QCheckBox
from .input_widget import NoTitleDoubleInputWidget, NoTitleIntegerInputWidget


class AnalogInputGroup(QGroupBox):
    def __init__(self):
        super().__init__("Analog Input")
        self.initUI()

    def initUI(self):
        ai_layout = QGridLayout()
        self.setLayout(ai_layout)
        titles = ["", "Terminal Mode", "Max Value", "Min Value", "Channel Status"]
        self.channels_name = ["ai0", "ai1", "ai2", "ai3"]
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
            self.terminal_status[this_channel] = QCheckBox("ENABLE", self)
            ai_layout.addWidget(self.terminal_mode[this_channel], i + 1, 1)
            ai_layout.addWidget(self.max_value[this_channel], i + 1, 2)
            ai_layout.addWidget(self.min_value[this_channel], i + 1, 3)
            ai_layout.addWidget(self.terminal_status[this_channel], i + 1, 4)
        ai_layout.addWidget(QLabel("Sampling Rate", self), len(self.channels_name) + 1, 0)
        ai_layout.addWidget(QLabel("Samples Per Channel", self), len(self.channels_name) + 1, 2)
        self.sampling_rate = NoTitleIntegerInputWidget(self, 50000, "Hz", 0, 500000, 100)
        self.samples_per_channel = NoTitleIntegerInputWidget(self, 500000, "", 0, 500000, 100)
        ai_layout.addWidget(self.sampling_rate, len(self.channels_name) + 1, 1)
        ai_layout.addWidget(self.samples_per_channel, len(self.channels_name) + 1, 3)

    def get_ai_cfg(self):
        cfg = dict()
        for name in self.channels_name:
            this_cfg = dict()
            this_cfg["terminal_mode"] = self.terminal_mode[name].value
            this_cfg["max_value"] = self.max_value[name].value
            this_cfg["min_value"] = self.min_value[name].value
            this_cfg["terminal_status"] = self.terminal_status[name].isChecked()
            cfg[name] = this_cfg
        return cfg

    def get_ai_timing_cfg(self):
        sampling_rate = self.sampling_rate.value
        samples_per_channel = self.samples_per_channel.value
        return (sampling_rate, samples_per_channel)

    def set_ai_cfg(self, cfg):
        for key, value in cfg.items():
            self.terminal_mode[key].set_value(value["terminal_mode"])
            self.max_value[key].set_value(value["max_value"])
            self.min_value[key].set_value(value["min_value"])
            self.terminal_status[key].setChecked(value["terminal_status"])

    def set_ai_timing_cfg(self, cfg):
        sampling_rate, samples_per_channel = cfg
        self.sampling_rate.set_value(sampling_rate)
        self.samples_per_channel.set_value(samples_per_channel)


class AIComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItem("RSE")
        self.addItem("NRSE")
        self.addItem("DIFFERENTIAL")
        self.value = "RSE"
        self.activated[str].connect(self.mode_change)

    def mode_change(self, text):
        self.value = text

    def set_value(self, value):
        self.value = value
        self.setCurrentText(value)
