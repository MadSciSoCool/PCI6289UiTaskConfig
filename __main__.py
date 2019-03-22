import sys
from config_ui.main_window import MainWindow
from daq_device.daq_device import DaqDevice
from PyQt5.QtWidgets import QApplication

daq_device = DaqDevice(device_name="Dev1/")
app = QApplication(sys.argv)
main_window = MainWindow(daq_device)
sys.exit(app.exec_())
