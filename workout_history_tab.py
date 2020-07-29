import json
import pyqtgraph as pg
from datetime import datetime

from PyQt5.QtCore import QPoint


class WorkoutHistoryTab:
    def __init__(self, main_window):
        self.main_window = main_window

        # When the selection is changed in the workout list view we update the display.
        self.main_window.workoutListView.selectionModel().selectionChanged.connect(self.update_display)

        # Selecting the most recent workout initially.
        self.main_window.workoutListView.setCurrentIndex(self.main_window.workoutListView.indexAt(QPoint(0, 0)))

    def update_display(self):
        """Updates the display on the workout history tab with the data from the currently selected item."""
        index = self.main_window.workoutListView.selectedIndexes()[0]

        if index:
            # Getting a list containing the data from the selected workout.
            workout = self.main_window.model.workouts[index.row()]

            # Setting the labels of the display to the corresponding data from the workout.
            self.main_window.dateLabel.setText(datetime.fromtimestamp(int(workout[0])).strftime('%d-%m-%Y %H:%M:%S'))
            self.main_window.programLabel.setText(workout[1])
            self.main_window.levelLabel.setText(workout[2])
            self.main_window.timeLabel.setText(workout[3])
            self.main_window.distanceLabel.setText(workout[4])
            self.main_window.caloriesLabel.setText(workout[5])
            self.main_window.avgSpeedLabel.setText(workout[6])
            self.main_window.avgRPMLabel.setText(workout[7])
            self.main_window.avgHeartRateLabel.setText(workout[8])
            self.main_window.avgWattLabel.setText(workout[9])
            self.main_window.maxSpeedLabel.setText(workout[10])
            self.main_window.maxRPMLabel.setText(workout[11])
            self.main_window.maxHeartRateLabel.setText(workout[12])
            self.main_window.maxWattLabel.setText(workout[13])

            self.update_graph(workout[0])

    def update_graph(self, filename):
        """
        Updating the graph with data from the given filename.

        :param filename: The Epoch time which uniquely identifies the specific file that we should pull the data from.
        """
        # Getting the data from the specified file.
        with open(f"data/workouts/{filename}.json", "r") as jsonfile:
            data = json.load(jsonfile)

        # Converting the timestamps into seconds and using them as the x-coordinate.
        x = self.convert_timestamps(data["time"])

        # Initializing the y-coordinates of the 5 different lines.
        y_speed = [float(i) for i in data["speed"]]
        y_rpm = [int(i) for i in data["rpm"]]
        y_heart_rate = [int(i) for i in data["heart_rate"]]
        y_watt = [float(i) for i in data["watt"]]
        y_level = [int(i) for i in data["level"]]

        self.main_window.workoutGraphWidget.clear()

        self.main_window.workoutGraphWidget.addLegend()

        # Plotting the lines in the graph.
        self.main_window.workoutGraphWidget.plot(x, y_speed, pen=pg.mkPen(color="#4b6bc8", width=2), name="Speed")
        self.main_window.workoutGraphWidget.plot(x, y_rpm, pen=pg.mkPen(color="#CD0000", width=2), name="RPM")
        self.main_window.workoutGraphWidget.plot(x, y_heart_rate, pen=pg.mkPen(color="#FFFF00", width=2),
                                                 name="Heart rate")
        self.main_window.workoutGraphWidget.plot(x, y_watt, pen=pg.mkPen(color="#008000", width=2), name="Watt")
        self.main_window.workoutGraphWidget.plot(x, y_level, pen=pg.mkPen(color="#800080", width=2), name="Level")

    @staticmethod
    def convert_timestamps(timestamps):
        """
        Converts a list of timestamps into a list of seconds so it can be used as the x-coordinates in a graph.

        :param timestamps: A list of timestamps where each timestamp has the format "HH:MM:SS".
        """
        seconds = []
        for timestamp in timestamps:
            # Adding the seconds from the timestamp.
            time_seconds = int(timestamp[6:])
            # Adding the minutes from the timestamp in seconds.
            time_seconds += int(timestamp[3:5]) * 60
            # Adding the hours from the timestamp in seconds.
            time_seconds += int(timestamp[:2]) * 3600

            seconds.append(time_seconds)

        return seconds
