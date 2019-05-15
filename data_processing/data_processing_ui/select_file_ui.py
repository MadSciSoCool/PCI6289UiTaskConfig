from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from enum import Enum


class Status(Enum):
    NOT_SET = -1
    FILE = 0
    DIR = 1


class SelectFileUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.key = "ai_acquired_data.csv"
        self.file_dir = ""
        self.status = Status.NOT_SET

    def initUI(self):
        layout = QGridLayout()
        self.file_dir_display = QLineEdit(self)
        self.file_dir_display.setFocusPolicy(Qt.NoFocus)
        self.key_name = QLineEdit()
        self.key_name.setText("ai_acquired_data.csv")
        self.key_name.textChanged.connect(self.key_changed)
        select_file = QPushButton("Select File", self)
        select_file.clicked.connect(self.select_file)
        select_dir = QPushButton("Select Dir", self)
        select_dir.clicked.connect(self.select_dir)
        layout.addWidget(QLabel("File/Directory to be processed:", self), 0, 0)
        layout.addWidget(self.file_dir_display, 1, 0)
        layout.addWidget(select_file, 1, 1)
        layout.addWidget(select_dir, 1, 2)
        layout.addWidget(QLabel("Process if file name matches:", self), 2, 0)
        layout.addWidget(self.key_name, 3, 0)
        self.setLayout(layout)
        self.show()

    def select_file(self):
        try:
            path, suffix = QFileDialog.getOpenFileName()
            if path != "":
                self.file_dir = path
                self.file_dir_display.setText(self.file_dir)
                self.status = Status.FILE
        except:
            pass

    def select_dir(self):
        try:
            file_dir = QFileDialog.getExistingDirectory()
            if file_dir != "":
                self.file_dir = file_dir
                self.file_dir_display.setText(self.file_dir)
                self.status = Status.DIR
        except:
            pass

    def key_changed(self):
        self.key = self.key_name.text()
