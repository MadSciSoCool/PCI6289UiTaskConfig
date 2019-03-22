from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QDialogButtonBox
from PyQt5 import QtCore, QtWidgets
from config_ui.input_widget import IntegerInputWidget, DoubleInputWidget


class AnalogWaveformInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        num_of_channels = 2
        num_of_settings = 6
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        group_boxes = []
        group_box_layouts = []
        self.time_input_widgets = [[] for i in range(num_of_channels)]
        self.level_input_widgets = [[] for i in range(num_of_channels)]
        for i in range(num_of_channels):
            group_boxes.append(QGroupBox("Channel " + str(i)))
            group_box_layouts.append(QHBoxLayout())
            group_boxes[i].setLayout(group_box_layouts[i])
            main_layout.addWidget(group_boxes[i])
            for j in range(num_of_settings):
                if j % 2 == 0:
                    name = "OFF TIME " + str(j // 2 + 1)
                else:
                    name = "ON TIME " + str(j // 2 + 1)
                self.time_input_widgets[i].append(IntegerInputWidget(self, name, 0, "ms", 0, 2000, 1))
                group_box_layouts[i].addWidget(self.time_input_widgets[i][j])
            self.level_input_widgets[i].append(DoubleInputWidget(self, "LOW", 0, "V", -20, 20, 2))
            self.level_input_widgets[i].append(DoubleInputWidget(self, "HIGH", 5, "V", -20, 20, 2))
            group_box_layouts[i].addWidget(self.level_input_widgets[i][0])
            group_box_layouts[i].addWidget(self.level_input_widgets[i][1])


class EditAnalogWaveformDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # use a hbox layout
        main_layout = QHBoxLayout()
        # data input widgets on the left
        self.data_input_widget = AnalogWaveformInputWidget()
        # button box on the right
        button_box = QDialogButtonBox(self)
        button_box.setOrientation(QtCore.Qt.Vertical)
        button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        button_box.clicked.connect(self.accept)
        button_box.rejected.connect(self.reject)
        # set the layout
        main_layout.addWidget(self.data_input_widget)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        # set the window title
        self.setWindowTitle("Edit Analog Waveform")
