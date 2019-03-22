import pickle
import os
from enum import Enum
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, QAction, QFileDialog)
from .analog_input_group import AnalogInputGroup
from .output_group import OutputSettingsGroup, AnalogOutputGroup, DigitalOutputGroup
from .data_processing_group import DataProcessingGroup


class Status(Enum):
    is_closed = -1
    is_started = 0
    is_paused = 1


"""
    is_closed: the task is not yet started or setup
    is_started: the task has already started and nothing is modified, can be stopped
    is_paused: the task is temporarily stopped, can be started again
"""


class MainWindow(QMainWindow):
    def __init__(self, daq_device):
        super().__init__()
        self.daq_device = daq_device
        self.path = ""
        self.status = Status.is_closed
        self.waveform_is_modified = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NIDAQ PCI-6289 Task Configuration Interface")

        change_working_directory_act = QAction("Change Working Directory", self)
        change_working_directory_act.setShortcut("Ctrl+C")
        change_working_directory_act.setStatusTip("Change the directory of saving and loading files")
        change_working_directory_act.triggered.connect(self.change_working_directory)

        export_settings_act = QAction("Export Settings", self)
        export_settings_act.setShortcut("Ctrl+E")
        export_settings_act.setStatusTip("Export the current settings")
        export_settings_act.triggered.connect(self.export_settings)

        import_settings_act = QAction("Import Settings", self)
        import_settings_act.setShortcut("Ctrl+I")
        import_settings_act.setStatusTip("Import from an existing settings file")
        import_settings_act.triggered.connect(self.import_settings)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(change_working_directory_act)
        file_menu.addAction(export_settings_act)
        file_menu.addAction(import_settings_act)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)

        # The Main Window is separated into 5 parts:
        # AI widget, Output Settings, AO widget, DO widget and Data Processing
        self.ai_group = AnalogInputGroup()
        self.output_settings = OutputSettingsGroup()
        self.ao_group = AnalogOutputGroup()
        self.do_group = DigitalOutputGroup()
        self.data_processing = DataProcessingGroup()
        # add the widgets to the main window layout
        central_layout.addWidget(self.ai_group)
        central_layout.addWidget(self.output_settings)
        central_layout.addWidget(self.ao_group)
        central_layout.addWidget(self.do_group)
        central_layout.addWidget(self.data_processing)
        # define the buttons on the bottom
        start_button = QPushButton("Start Measurement", self)
        stop_button = QPushButton("Stop Measurement", self)
        central_layout.addWidget(start_button)
        central_layout.addWidget(stop_button)
        # connenct all kinds of signals to their slot
        start_button.clicked.connect(self.start_task_event)
        stop_button.clicked.connect(self.stop_task_event)
        self.do_group.edit_digital_waveform_dialog.accepted.connect(self.digital_output_accepted_event)
        self.ao_group.edit_analog_waveform_dialog.accepted.connect(self.analog_output_accepted_event)
        self.show()

    # rewrite the closing event to properly stop all tasks
    def closeEvent(self, *args, **kwargs):
        self.daq_device.close()

    # define the menu events
    def change_working_directory(self):
        self.path = QFileDialog.getExistingDirectory()

    def export_settings(self):
        settings = dict()
        settings["ai"] = self.ai_group.get_ai_cfg()
        settings["ai_timing"] = self.ai_group.get_ai_timing_cfg()
        settings["output"] = self.output_settings.get_output_settings()
        settings["ao"] = self.ao_group.get_analog_waveform()
        settings["do"] = self.do_group.get_digital_waveform()
        settings["data"] = self.data_processing.get_data_processing_settings()
        path, suffix = QFileDialog.getSaveFileName(filter="*.pkl")
        with open(path, "wb") as object:
            pickle.dump(settings, object)

    def import_settings(self):
        path, suffix = QFileDialog.getOpenFileName(filter="*.pkl")
        with open(path, "rb") as object:
            try:
                settings = pickle.load(object)
                self.ai_group.set_ai_cfg(settings["ai"])
                self.ai_group.set_ai_timing_cfg(settings["ai_timing"])
                self.output_settings.set_output_settings(settings["output"])
                self.ao_group.set_analog_waveform(settings["ao"])
                self.do_group.set_digital_waveform(settings["do"])
                self.data_processing.set_data_processing_settings(settings["data"])
            except Exception as error:
                print(error)

    # define the widgets events
    def start_task_event(self):
        # change the data processing settings
        min_frequency, max_frequency = self.data_processing.get_data_processing_settings()
        output_period, sampling_rate = self.output_settings.get_output_settings()
        self.daq_device.ai_channels.set_data_processing_par(self.path,
                                                            min_frequency,
                                                            max_frequency)
        # if the output waveform is modified, first change the waveform
        if self.waveform_is_modified:
            self.daq_device.do_channels.set_digital_waveform(self.do_group.get_digital_waveform(),
                                                             output_period,
                                                             sampling_rate)
            self.daq_device.ao_channels.set_analog_waveform(self.ao_group.get_analog_waveform(),
                                                            output_period,
                                                            sampling_rate)
            self.waveform_is_modified = False
        if self.status == Status.is_closed:
            self.set_ai_channels()
            self.daq_device.set_output_sampling_rate(sampling_rate)
            self.daq_device.start_task()
            self.status = Status.is_started
        elif self.status == Status.is_paused:
            self.daq_device.start_task()
            self.status = Status.is_started

    def stop_task_event(self):
        if self.status == Status.is_started:
            self.daq_device.stop_task()
            self.status = Status.is_paused

    def digital_output_accepted_event(self):
        self.do_group.edit_digital_waveform_dialog.hide()
        self.waveform_is_modified = True

    def analog_output_accepted_event(self):
        self.ao_group.edit_analog_waveform_dialog.hide()
        self.waveform_is_modified = True

    # to set up the analog input channels
    def set_ai_channels(self):
        self.daq_device.ai_channels.rebuild_task(self.ai_group.get_ai_cfg())
        self.daq_device.ai_channels.timing_configuration = self.ai_group.get_ai_timing_cfg()
