from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QWidget, QVBoxLayout
from .select_file_ui import SelectFileUI
from .period_recognition_ui import PeriodRecognitionUI
from .plot_config_ui import PlotConfigUI
from .other_options_ui import OtherOptionsUI


class DataProcessingUI(QMainWindow):
    def __init__(self, data_process_method):
        super().__init__()
        self.output_path = "data_processing_output"
        self.initUI()
        self.data_process_method = data_process_method

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
        file_menu = menubar.addMenu("Menu")
        file_menu.addAction(change_working_directory_act)
        file_menu.addAction(start_processing_act)

        # define central widgets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        # add widgets to central widget
        self.select_file_ui = SelectFileUI()
        central_layout.addWidget(self.select_file_ui)
        self.period_recognition_ui = PeriodRecognitionUI()
        central_layout.addWidget(self.period_recognition_ui)
        self.plot_config_ui = PlotConfigUI()
        central_layout.addWidget(self.plot_config_ui)
        self.other_options_ui = OtherOptionsUI()
        central_layout.addWidget(self.other_options_ui)
        self.show()

    def change_working_directory(self):
        try:
            self.output_path = QFileDialog.getExistingDirectory()
        except:
            pass

    def start_processing(self):
        self.data_process_method(output_path=self.output_path,
                                 mode=self.select_file_ui.status.value,
                                 path=self.select_file_ui.file_dir,
                                 key=self.select_file_ui.key,
                                 resolution=self.period_recognition_ui.resolution.value,
                                 vpp_threshold=self.period_recognition_ui.vpp_threshold.value / 100.,
                                 length_threshold=self.period_recognition_ui.length_threshold.value / 100.,
                                 enable_differential=self.other_options_ui.differential.isChecked(),
                                 dif1=int(self.other_options_ui.channel_1.currentText()),
                                 dif2=int(self.other_options_ui.channel_2.currentText()),
                                 is_spliced=self.other_options_ui.spliced.isChecked(),
                                 output_mode=self.plot_config_ui.organization,
                                 auto=self.plot_config_ui.auto.isChecked(),
                                 left=self.plot_config_ui.left.value,
                                 right=self.plot_config_ui.right.value)
