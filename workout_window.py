import asyncio
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThreadPool

import bluetooth_session
from worker import Worker
from settings_dialog import Settings


# TODO: Make it so you can manually change levels during the workout.
class WorkoutWindow(QtWidgets.QMainWindow):
    def __init__(self, level, duration, *args, **kwargs):
        super(WorkoutWindow, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/workoutwindow.ui", self)

        self.session = None

        self.level = level
        self.duration = duration

        # Setting up multi threading.
        self.threadpool = QThreadPool()

        # Loading the connection information from the settings.
        self.settings = Settings()
        self.address = self.settings.address
        self.characteristic_uuid = self.settings.characteristic_uuid

        # Connecting buttons to their corresponding functionality.
        self.startWorkoutButton.clicked.connect(self.start_workout)
        self.stopWorkoutButton.clicked.connect(self.stop_workout)

    def start_workout(self):
        """Setting up the BluetoothSession object and starting the session when the "Start workout" btn is pressed."""
        # Using Epoch time as the filename to ensure that each workout session has an unique filename.
        filename = f"{time.time():.0f}"

        loop = asyncio.get_event_loop()

        self.session = bluetooth_session.BluetoothSession(self.characteristic_uuid, self.address, filename,
                                                          self.level, self.duration, self.update_live_page)
        worker = Worker(loop.run_until_complete, self.session.run_session())
        self.threadpool.start(worker)

    def stop_workout(self):
        """Stopping the workout by setting the internal stop flag to True."""
        self.session.stop_flag = True

    def update_live_page(self, data):
        """
        Updating the display widgets on the live workout page with the newest data every second. This method is called
        every time we process a new data response from the exercise bike to ensure the newest data is displayed.

        :param data: The data that should be used to update the display widgets.
        """
        self.timeLabel.setText(data[0])
        self.speedNumber.display(data[1])
        self.rpmNumber.display(data[2])
        self.distanceNumber.display(data[3])
        self.caloriesNumber.display(data[4])
        self.heartRateNumber.display(data[5])
        self.wattNumber.display(data[6])
        self.levelSpinBox.setValue(int(data[7]))
