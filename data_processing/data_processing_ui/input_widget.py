from PyQt5.QtWidgets import QLabel, QPushButton, QInputDialog, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject


class Communication(QObject):
    is_set = pyqtSignal()


class IntegerInputWidget(QWidget):
    def __init__(self, object, value_name, default_value, dimension, minimum, maximum, step):
        super().__init__()

        # use vbox layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # get parameters from input
        self.minimum = minimum
        self.maximum = maximum
        self.step = step
        self.communication = Communication()
        self.object = object
        self.dimension = dimension
        self.value_name = value_name
        default_text = str(default_value) + dimension

        # consists of 3 widgets
        self.label = QLabel(value_name, object)
        self.text = QLabel(default_text, object)
        self.change = QPushButton("Change", object)

        # set layout
        vbox.addWidget(self.label)
        vbox.addWidget(self.text)
        vbox.addWidget(self.change)

        self.value = default_value

        self.change.clicked.connect(self.clicked_event)

    def set_value(self, value):
        self.value = value
        self.text.setText(str(value) + self.dimension)

    def clicked_event(self):
        value, ok_pressed = QInputDialog.getInt(self.object,
                                                self.value_name,
                                                "please input an integer:",
                                                self.value,
                                                self.minimum,
                                                self.maximum,
                                                self.step)
        if ok_pressed:
            self.text.setText(str(value) + self.dimension)
            self.value = value
            self.communication.is_set.emit()

