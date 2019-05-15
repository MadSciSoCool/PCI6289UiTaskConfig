from PyQt5.QtWidgets import QGroupBox, QGridLayout, QCheckBox, QLabel, QRadioButton
from .input_widget import IntegerInputWidget


class PlotConfigUI(QGroupBox):
    def __init__(self):
        super().__init__("Plot Configurations")
        self.initUI()
        self.organization = "single_spectrum"

    def initUI(self):
        layout = QGridLayout()
        self.auto = QCheckBox("Auto", self)
        self.auto.setChecked(True)
        self.left = IntegerInputWidget(self, "X axis left", 0, "Hz", 0, 250000, 1)
        self.right = IntegerInputWidget(self, "X axis right", 0, "Hz", 0, 250000, 1)
        self.left.communication.is_set.connect(self.check_validity)
        self.right.communication.is_set.connect(self.check_validity)
        single_spectrum = QRadioButton("Single Spectrum", self)
        single_spectrum.setChecked(True)
        single_spectrum.clicked.connect(self.single_spectrum_clicked)
        contrast_periods = QRadioButton("Contrasting Periods", self)
        contrast_periods.clicked.connect(self.contrast_periods_clicked)
        contrast_channels = QRadioButton("Contrasting Channels", self)
        contrast_channels.clicked.connect(self.contrast_channels_clicked)
        layout.addWidget(QLabel("Spectrum Display Settings", self), 0, 0)
        layout.addWidget(self.auto, 1, 0)
        layout.addWidget(self.left, 1, 1)
        layout.addWidget(self.right, 1, 2)
        layout.addWidget(QLabel("Organize the spectrums by:"), 2, 0)
        layout.addWidget(single_spectrum, 3, 0)
        layout.addWidget(contrast_periods, 3, 1)
        layout.addWidget(contrast_channels, 3, 2)
        self.setLayout(layout)
        self.show()

    def single_spectrum_clicked(self):
        self.organization = "single_spectrum"

    def contrast_periods_clicked(self):
        self.organization = "contrast_periods"

    def contrast_channels_clicked(self):
        self.organization = "contrast_channels"

    def check_validity(self):
        if self.right.value <= self.left.value:
            high = self.left.value
            low = self.right.value
            self.left.set_value(low)
            self.right.set_value(high)

