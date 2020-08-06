import asyncio
import time
import pyqtgraph as pg

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThreadPool

import bluetooth_session
from worker import Worker
from settings_dialog import Settings
from workout_session import WorkoutSession


class WorkoutWindow(QtWidgets.QMainWindow):
    def __init__(self, program, main_window, *args, **kwargs):
        """
        Method called when a live workout window is initialized.

        :param program: The workout program containing the level, duration and level changes of the workout.
        :param main_window: The main window instance which is used to update the main window when the workout is done.
        """
        super(WorkoutWindow, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/workoutwindow.ui", self)

        self.session = None

        self.program = program
        self.main_window = main_window

        # Performing cosmetic changes to the coordinate lists to make the visualization clearer and plotting them.
        x, y = self.program.prettify_line()
        self.graphWidget.plot(x, y, pen=pg.mkPen(color="#4b6bc8", width=3))

        self.graphWidget.setBackground("#31363b")

        # Initializing the point that highlights where the user currently is in the workout program.
        self.highlight_point = self.graphWidget.plot([0], [self.program.level], symbol="o", symbolSize=20)

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

        workout_session = WorkoutSession(self.program, filename, self.main_window)
        self.session = bluetooth_session.BluetoothSession(self.characteristic_uuid, self.address,
                                                          workout_session, self.update_live_page)

        worker = Worker(loop.run_until_complete, self.session.run_session())
        self.threadpool.start(worker)

    def stop_workout(self):
        """Stopping the workout prematurely by setting the internal stop flag to True."""
        self.session.stop_flag = True

    def update_live_page(self, timestamp, speed, rpm, distance, calories, heart_rate, watt):
        """
        Updating the display widgets on the live workout page with the newest data every second. This method is called
        every time we process a new data response from the exercise bike to ensure the newest data is displayed.

        :param timestamp: The current time in the format HH:MM:SS.
        :param speed: The current speed in km/h.
        :param rpm: The current RPM.
        :param distance: The current distance in km.
        :param calories: The current calories.
        :param heart_rate: The current heart rate.
        :param watt: The current power in watt.
        """
        self.timeLabel.setText(timestamp)
        self.speedNumber.display(speed)
        self.rpmNumber.display(rpm)
        self.distanceNumber.display(distance)
        self.caloriesNumber.display(calories)
        self.heartRateNumber.display(heart_rate)
        self.wattNumber.display(watt)

        # Extracting the minutes from the timestamp and using it to plot the live progression of the program.
        self.update_highlight_point(int(timestamp[3:-3]))

    def update_highlight_point(self, current_minute):
        """
        Updating the point that highlights the specific section of the program where the user currently is.

        :param current_minute: The current time in minutes.
        """
        # Highlighting the current section if the workout is underway.
        if current_minute < self.program.duration:
            x_highlight = [current_minute]
            y_highlight = [self.program.levels[current_minute]]
            self.highlight_point.setData(x_highlight, y_highlight)
