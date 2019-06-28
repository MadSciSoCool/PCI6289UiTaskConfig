import sys
from config_ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication, QMessageBox


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
