from PyQt5.QtWidgets import QLabel, QPushButton, QInputDialog, QWidget, QVBoxLayout


class DoubleInputWidget(QWidget):
    def __init__(self, object, value_name, default_value, dimension):
        super().__init__()

        # use vbox layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

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

        self.change.clicked.connect(self.clicked_event)

    def clicked_event(self):
        value, ok_pressed = QInputDialog.getDouble(self.object, self.value_name, "please input value:")
        if ok_pressed:
            self.text.setText(str(value) + self.dimension)
