import sys
from PyQt5.QtWidgets import QApplication
from data_processing.data_processing_functions.data_process import data_process
from data_processing.data_processing_ui.data_processing_ui import DataProcessingUI

app = QApplication(sys.argv)
main_window = DataProcessingUI(data_process)
sys.exit(app.exec_())
