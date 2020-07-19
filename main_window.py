import asyncio
import time

from PyQt5 import QtWidgets, uic

import bluetooth_session


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("resources/mainwindow.ui", self)

        # for d in loop.run_until_complete(bluetooth.get_nearby_devices()):
        #     print(d)

        # TODO Find a way to avoid these being hardcoded.
        # The characteristic that should be written to.
        self.characteristic_uuid = "***REMOVED***"

        self.address = "***REMOVED***"
        self.loop = asyncio.get_event_loop()

        # Connecting buttons to their corresponding functionality.
        self.startWorkoutButton.clicked.connect(self.start_workout)

    def start_workout(self):
        # Using Epoch time as the filename to ensure that each workout session has an unique filename.
        bx70i = bluetooth_session.BluetoothSession(self.characteristic_uuid, self.address, self.loop,
                                                   f"{time.time():.0f}", 13, "00:00:01:00")
        self.loop.run_until_complete(bx70i.start_session())
