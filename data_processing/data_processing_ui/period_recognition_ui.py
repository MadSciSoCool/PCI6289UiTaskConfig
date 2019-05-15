from PyQt5.QtWidgets import QGroupBox, QHBoxLayout
from .input_widget import IntegerInputWidget


class PeriodRecognitionUI(QGroupBox):
    def __init__(self):
        super().__init__("Period Recognition")
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.resolution = IntegerInputWidget(self, "Resolution", 1000, "", 1, 100000, 1)
        self.vpp_threshold = IntegerInputWidget(self, "Vpp Threshold", 30, "%", 1, 100, 1)
        self.length_threshold = IntegerInputWidget(self, "Length Threshold", 30, "%", 1, 100, 1)
        layout.addWidget(self.resolution)
        layout.addWidget(self.vpp_threshold)
        layout.addWidget(self.length_threshold)
        self.setLayout(layout)
        self.show()
