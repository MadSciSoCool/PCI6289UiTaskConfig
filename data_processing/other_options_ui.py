from PyQt5.QtWidgets import QCheckBox, QGroupBox, QGridLayout, QComboBox, QLabel
from PyQt5.QtCore import Qt

class OtherOptionsUI(QGroupBox):
    def __init__(self):
        super().__init__("Other Options")
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        differential = QCheckBox("Differential", self)
        channel_options = ["0", "1", "2", "3"]
        channel_1 = QComboBox(self)
        channel_1.addItems(channel_options)
        channel_2 = QComboBox(self)
        channel_2.addItems(channel_options)
        minus_sign = QLabel("-", self)
        minus_sign.setAlignment(Qt.AlignCenter)
        spliced = QCheckBox("Spliced", self)
        layout.addWidget(differential, 0, 0)
        layout.addWidget(channel_1, 0, 1)
        layout.addWidget(minus_sign, 0, 2)
        layout.addWidget(channel_2, 0, 3)
        layout.addWidget(spliced, 1, 0)
        self.setLayout(layout)
