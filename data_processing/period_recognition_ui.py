from PyQt5.QtWidgets import QGroupBox, QHBoxLayout
from .input_widget import IntegerInputWidget


class PeriodRecognitionUI(QGroupBox):
    def __init__(self):
        super().__init__("Period Recognition")
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        resolution = IntegerInputWidget(self, "Resolution", 1000, "", 1, 100000, 1)
        threshold = IntegerInputWidget(self, "Threshold", 30, "%", 1, 100, 1)
        layout.addWidget(resolution)
        layout.addWidget(threshold)
        self.setLayout(layout)
        self.show()
