import asyncio
import time
import pyqtgraph as pg

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThreadPool

import bluetooth_session
from worker import Worker
from settings_dialog import Settings


class WorkoutWindow(QtWidgets.QMainWindow):
    def __init__(self, program, *args, **kwargs):
        """
        Method called when a live workout window is initialized.

        :param program: The workout program containing the level, duration and level changes of the workout.
        """
        super(WorkoutWindow, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/workoutwindow.ui", self)

        self.session = None

        self.program = program

        # Performing cosmetic changes to the coordinate lists to make the visualization clearer and plotting them.
        x, y = self.program.prettify_line()
        self.graphWidget.plot(x, y, pen=pg.mkPen(color="#4b6bc8"))

        # Initializing the point that highlights where the user currently is in the workout program.
        self.highlight_point = self.graphWidget.plot([0], [self.program.level], symbol="o", symbolSize=13)

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
                                                          self.program, self.update_live_page)
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

        # Extracting the minutes from the timestamp and using it to plot the live progression of the program.
        self.update_highlight_point(int(data[0][3:-3]))

    def update_highlight_point(self, current_minute):
        """
        Updating the point that highlights the specific section of the program where the user currently is.

        :param current_minute: The current time in minutes.
        """
        # Highlighting the current section if the workout is underway.
        if current_minute < self.program.duration:
            x_highlight = [self.program.x_coordinates[current_minute]]
            y_highlight = [self.program.y_coordinates[current_minute]]
            self.highlight_point.setData(x_highlight, y_highlight)
