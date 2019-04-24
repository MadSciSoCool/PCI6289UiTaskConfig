import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QWidget, QVBoxLayout
from .select_file_ui import SelectFileUI
from .period_recognition_ui import PeriodRecognitionUI
from .plot_config_ui import PlotConfigUI
from .other_options_ui import OtherOptionsUI
from .data_processing import data_processing


class DataProcessingUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.output_path = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Auto Data Processing Interface")

        # define menubar
        change_working_directory_act = QAction("Change Working Directory", self)
        change_working_directory_act.setShortcut("Ctrl+C")
        change_working_directory_act.setStatusTip("Change the saving directory")
        change_working_directory_act.triggered.connect(self.change_working_directory)

        start_processing_act = QAction("Start Processing", self)
        start_processing_act.setShortcut("Ctrl+S")
        start_processing_act.setStatusTip("Start data processing")
        start_processing_act.triggered.connect(self.start_processing)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(change_working_directory_act)

        # define central widgets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        # add widgets to central widget
        select_file_ui = SelectFileUI()
        central_layout.addWidget(select_file_ui)
        period_recognition_ui = PeriodRecognitionUI()
        central_layout.addWidget(period_recognition_ui)
        plot_config_ui = PlotConfigUI()
        central_layout.addWidget(plot_config_ui)
        other_options_ui = OtherOptionsUI()
        central_layout.addWidget(other_options_ui)
        self.show()

    def change_working_directory(self):
        try:
            self.output_path = QFileDialog.getExistingDirectory()
        except:
            pass

    def start_processing(self):
        data_processing()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DataProcessingUI()
    sys.exit(app.exec_())
