import sys
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QVBoxLayout, QHBoxLayout, QGroupBox, QDialogButtonBox
from PyQt5 import QtCore, QtWidgets
from config_ui.input_widget import IntegerInputWidget


class DigitalWaveformInputWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        num_of_lines = 6
        num_of_settings = 6
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        group_boxes = []
        group_box_layouts = []
        self.input_widgets = [[] for i in range(num_of_lines)]
        for i in range(num_of_lines):
            group_boxes.append(QGroupBox("Line" + str(i)))
            group_box_layouts.append(QHBoxLayout())
            group_boxes[i].setLayout(group_box_layouts[i])
            main_layout.addWidget(group_boxes[i])
            for j in range(num_of_settings):
                if j % 2 == 0:
                    name = "OFF TIME " + str(j // 2 + 1)
                else:
                    name = "ON TIME " + str(j // 2 + 1)
                self.input_widgets[i].append(IntegerInputWidget(self, name, 0, "ms", 0, 1000, 1))
                group_box_layouts[i].addWidget(self.input_widgets[i][j])

    def get_digital_waveform(self):
        num_of_lines = 6
        num_of_settings = 6
        digital_waveform = [[] for i in range(num_of_lines)]
        for i in range(num_of_lines):
            for j in range(num_of_settings):
                digital_waveform[i].append(self.input_widgets[i][j].value)
        return digital_waveform


class EditDigitalWaveformDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # use a hbox layout
        main_layout = QHBoxLayout()

        # data input widgets on the left
        self.data_input_widget = DigitalWaveformInputWidget()
        side_widget = QWidget()
        main_layout.addWidget(self.data_input_widget)
        main_layout.addWidget(side_widget)

        side_layout = QVBoxLayout()
        side_widget.setLayout(side_layout)
        # button box on the right
        button_box = QDialogButtonBox(self)
        button_box.setOrientation(QtCore.Qt.Vertical)
        button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        button_box.clicked.connect(self.accept)
        button_box.rejected.connect(self.reject)

        side_layout.addWidget(button_box)
        self.period_time = IntegerInputWidget(self, "PERIOD TIME", 500, "ms", 0, 5000, 1)
        side_layout.addWidget(self.period_time)

        self.setLayout(main_layout)
        self.setWindowTitle("Edit Digital Waveform")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = EditDigitalWaveformDialog()
    sys.exit(app.exec_())
