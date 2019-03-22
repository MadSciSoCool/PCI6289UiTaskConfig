from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QPushButton
from .input_widget import IntegerInputWidget
from .edit_analog_waveform_dialog import EditAnalogWaveformDialog
from .edit_digital_waveform_dialog import EditDigitalWaveformDialog


class OutputSettingsGroup(QGroupBox):
    def __init__(self):
        super().__init__("General Output Settings")
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.output_period = IntegerInputWidget(self, "PERIOD TIME", 1000, "ms", 0, 5000, 1)
        self.sampling_rate = IntegerInputWidget(self, "SAMPLING RATE", 1000, "Hz", 100, 10000, 100)
        layout.addWidget(self.output_period)
        layout.addWidget(self.sampling_rate)
        self.setLayout(layout)
        self.show()

    def get_output_settings(self):
        return self.output_period.value, self.sampling_rate.value

    def set_output_settings(self, settings):
        output_period, sampling_rate = settings
        self.output_period.set_value(output_period)
        self.sampling_rate.set_value(sampling_rate)


class AnalogOutputGroup(QGroupBox):
    def __init__(self):
        super().__init__("Analog Output")
        self.edit_analog_waveform_dialog = EditAnalogWaveformDialog()
        self.initUI()

    def initUI(self):
        do_layout = QHBoxLayout()
        self.setLayout(do_layout)
        edit_button = QPushButton("Edit Analog Waveform")
        do_layout.addWidget(edit_button)
        edit_button.clicked.connect(self.edit_analog_waveform)

    def edit_analog_waveform(self):
        self.edit_analog_waveform_dialog.show()

    def get_analog_waveform(self):
        num_of_channels = 2
        num_of_settings = 6
        waveform = dict()
        for i in range(num_of_channels):
            name = "channel" + str(i)
            waveform[name] = dict()
            waveform[name]["time"] = []
            for j in range(num_of_settings):
                waveform[name]["time"].append(
                    self.edit_analog_waveform_dialog.data_input_widget.time_input_widgets[i][j].value)
            waveform[name]["low"] = self.edit_analog_waveform_dialog.data_input_widget.level_input_widgets[i][0].value
            waveform[name]["high"] = self.edit_analog_waveform_dialog.data_input_widget.level_input_widgets[i][1].value
        return waveform

    def set_analog_waveform(self, waveform):
        num_of_channels = 2
        num_of_settings = 6
        for i in range(num_of_channels):
            value = list(waveform.values())[i]
            for j in range(num_of_settings):
                self.edit_analog_waveform_dialog.data_input_widget.time_input_widgets[i][j].set_value(value["time"][j])
            self.edit_analog_waveform_dialog.data_input_widget.level_input_widgets[i][0].set_value(value["low"])
            self.edit_analog_waveform_dialog.data_input_widget.level_input_widgets[i][1].set_value(value["high"])


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

    def get_digital_waveform(self):
        num_of_lines = 6
        num_of_settings = 6
        waveform = [[] for i in range(num_of_lines)]
        for i in range(num_of_lines):
            for j in range(num_of_settings):
                waveform[i].append(self.edit_digital_waveform_dialog.data_input_widget.input_widgets[i][j].value)
        return waveform

    def set_digital_waveform(self, waveform):
        num_of_lines = 6
        num_of_settings = 6
        for i in range(num_of_lines):
            for j in range(num_of_settings):
                self.edit_digital_waveform_dialog.data_input_widget.input_widgets[i][j].set_value(waveform[i][j])
