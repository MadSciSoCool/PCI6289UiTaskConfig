from PyQt5.QtWidgets import QCheckBox, QGroupBox, QGridLayout, QComboBox, QLabel
from PyQt5.QtCore import Qt

class OtherOptionsUI(QGroupBox):
    def __init__(self):
        super().__init__("Other Options")
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.differential = QCheckBox("Differential", self)
        channel_options = ["0", "1", "2", "3"]
        self.channel_1 = QComboBox(self)
        self.channel_1.addItems(channel_options)
        self.channel_2 = QComboBox(self)
        self.channel_2.addItems(channel_options)
        minus_sign = QLabel("-", self)
        minus_sign.setAlignment(Qt.AlignCenter)
        self.spliced = QCheckBox("Spliced", self)
        layout.addWidget(self.differential, 0, 0)
        layout.addWidget(self.channel_1, 0, 1)
        layout.addWidget(minus_sign, 0, 2)
        layout.addWidget(self.channel_2, 0, 3)
        layout.addWidget(self.spliced, 1, 0)
        self.setLayout(layout)
