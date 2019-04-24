from PyQt5.QtWidgets import QGroupBox, QGridLayout, QCheckBox, QLabel, QRadioButton
from .input_widget import IntegerInputWidget
from enum import Enum


class SpectrumOrganization(Enum):
    single_spectrum = 0
    contrast_periods = 1
    contrast_channels = 2


class PlotConfigUI(QGroupBox):
    def __init__(self):
        super().__init__("Plot Configurations")
        self.initUI()
        self.organization = SpectrumOrganization.single_spectrum

    def initUI(self):
        layout = QGridLayout()
        auto = QCheckBox("Auto", self)
        auto.setChecked(True)
        left = IntegerInputWidget(self, "X axis left", 0, "Hz", 0, 250000, 1)
        right = IntegerInputWidget(self, "X axis right", 0, "Hz", 0, 250000, 1)
        single_spectrum = QRadioButton("Single Spectrum", self)
        single_spectrum.setChecked(True)
        single_spectrum.clicked.connect(self.single_spectrum_clicked)
        contrast_periods = QRadioButton("Contrasting Periods", self)
        contrast_periods.clicked.connect(self.contrast_periods_clicked)
        contrast_channels = QRadioButton("Contrasting Channels", self)
        contrast_channels.clicked.connect(self.contrast_channels_clicked)
        layout.addWidget(QLabel("Spectrum Display Settings", self), 0, 0)
        layout.addWidget(auto, 1, 0)
        layout.addWidget(left, 1, 1)
        layout.addWidget(right, 1, 2)
        layout.addWidget(QLabel("Organize the spectrums by:"), 2, 0)
        layout.addWidget(single_spectrum, 3, 0)
        layout.addWidget(contrast_periods, 3, 1)
        layout.addWidget(contrast_channels, 3, 2)
        self.setLayout(layout)
        self.show()

    def single_spectrum_clicked(self):
        self.organization = SpectrumOrganization.single_spectrum

    def contrast_periods_clicked(self):
        self.organization = SpectrumOrganization.contrast_periods

    def contrast_channels_clicked(self):
        self.organization = SpectrumOrganization.contrast_channels

