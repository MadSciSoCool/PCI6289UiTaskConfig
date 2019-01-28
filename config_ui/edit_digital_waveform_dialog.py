import sys
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QVBoxLayout, QHBoxLayout, QGroupBox, QDialogButtonBox
from PyQt5 import QtCore
from input_widget import DoubleInputWidget


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
        for i in range(num_of_lines):
            group_boxes.append(QGroupBox("Line" + str(i)))
            group_box_layouts.append(QHBoxLayout())
            group_boxes[i].setLayout(group_box_layouts[i])
            main_layout.addWidget(group_boxes[i])
            for j in range(num_of_settings):
                if j % 2 == 0:
                    name = "OFF TIME " + str(j // 2 + 1)
                    group_box_layouts[i].addWidget(DoubleInputWidget(self, name, 0, "ms"))
                else:
                    name = "ON TIME " + str(j // 2 + 1)
                    group_box_layouts[i].addWidget(DoubleInputWidget(self, name, 0, "ms"))


class EditDigitalWaveformDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # use a hbox layout
        main_layout = QHBoxLayout()

        # data input widgets on the left
        data_input_widget = DigitalWaveformInputWidget()
        main_layout.addWidget(data_input_widget)

        # button box on the right
        button_box = QDialogButtonBox(self)
        button_box.setOrientation(QtCore.Qt.Vertical)
        button_box.addButton(QDialogButtonBox.Ok)
        button_box.addButton(QDialogButtonBox.Cancel)
        main_layout.addWidget(button_box)

        self.setLayout(main_layout)
        self.setWindowTitle("Edit Digital Waveform")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = EditDigitalWaveformDialog()
    sys.exit(app.exec_())
