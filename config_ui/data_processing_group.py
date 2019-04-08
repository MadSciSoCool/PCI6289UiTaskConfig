from PyQt5.QtWidgets import QGroupBox, QGridLayout, QCheckBox
from .input_widget import IntegerInputWidget


class DataProcessingGroup(QGroupBox):
    def __init__(self):
        super().__init__("Data Processing")
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.min_frequency = IntegerInputWidget(self, "MIN FREQUENCY", -1, "Hz", 0, 250000, 1)
        self.max_frequency = IntegerInputWidget(self, "MAX FREQUENCY", -1, "Hz", 0, 250000, 1)
        self.fft_start = IntegerInputWidget(self, "FFT START", -1, "ms", 0, 5000, 1)
        self.fft_end = IntegerInputWidget(self, "FFT END", -1, "ms", 0, 5000, 1)
        self.enable_plot = QCheckBox("ENABLE PLOT", self)
        self.dif_mode = QCheckBox("DIFFERENTIAL MODE", self)
        self.spliced = QCheckBox("SPLICED", self)
        layout.addWidget(self.min_frequency, 0, 0)
        layout.addWidget(self.max_frequency, 0, 1)
        layout.addWidget(self.fft_start, 0, 2)
        layout.addWidget(self.fft_end, 0, 3)
        layout.addWidget(self.enable_plot, 1, 0)
        layout.addWidget(self.dif_mode, 1, 1)
        layout.addWidget(self.spliced, 1, 2)
        self.min_frequency.communication.is_set.connect(self.check_validity)
        self.max_frequency.communication.is_set.connect(self.check_validity)
        self.setLayout(layout)
        self.show()

    def check_validity(self):
        if self.max_frequency.value <= self.min_frequency.value:
            high = self.min_frequency.value
            low = self.max_frequency.value
            self.min_frequency.set_value(low)
            self.max_frequency.set_value(high)

    def get_data_processing_settings(self):
        return (self.min_frequency.value, self.max_frequency.value, self.fft_start.value,
                self.fft_end.value, self.enable_plot.isChecked(), self.dif_mode.isChecked(), self.spliced.isChecked())

    def set_data_processing_settings(self, settings):
        min_frequency, max_frequency, fft_start, fft_end, enable_plot, dif_mode, spliced = settings
        self.min_frequency.set_value(min_frequency)
        self.max_frequency.set_value(max_frequency)
        self.fft_start.set_value(fft_start)
        self.fft_end.set_value(fft_end)
        self.enable_plot.setChecked(enable_plot)
        self.dif_mode.setChecked(dif_mode)
        self.spliced.setChecked(spliced)
