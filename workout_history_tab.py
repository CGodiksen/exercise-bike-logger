import json
import pyqtgraph as pg
from datetime import datetime

from PyQt5.QtCore import QPoint


# TODO: Make it so the workout history is updated automatically when a new workout is done.
class WorkoutHistoryTab:
    def __init__(self, main_window):
        self.main_window = main_window

        # When the selection is changed in the workout list view we update the display.
        self.main_window.workoutListView.selectionModel().selectionChanged.connect(self.update_display)

        # Selecting the most recent workout initially.
        self.main_window.workoutListView.setCurrentIndex(self.main_window.workoutListView.indexAt(QPoint(0, 0)))

        # Updating the graph when the graph combo box is changed.
        self.main_window.graphComboBox.currentIndexChanged.connect(self.update_graph)

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

            self.update_graph()

    def update_graph(self):
        """Updating the graph with data from the current configuration."""
        # Retrieving the filename of the file containing the full data from the currently selected workout.
        filename = self.main_window.model.workouts[self.main_window.workoutListView.selectedIndexes()[0].row()][0]

        # Getting the specific data that should be plotted from the graph combo box.
        data_name = self.main_window.graphComboBox.currentText()

        # Getting the data from the specified file.
        with open(f"data/workouts/{filename}.json", "r") as jsonfile:
            data = json.load(jsonfile)

        # Converting the timestamps into minutes and using them as the x-coordinate.
        x = self.convert_timestamps(data["time"])

        # Initializing the y-coordinates.
        y = data[data_name.lower().replace(" ", "_")]

        self.main_window.workoutGraphWidget.clear()

        # Choosing the color of the line based on the index of the combo box to ensure each line is unique.
        colors = ["#4b6bc8", "#FFFF00", "#CD0000", "#008000", "#800080", "#FFA500", "#00FFD2"]
        line_color = colors[self.main_window.graphComboBox.currentIndex()]

        # Plotting the content in the graph, including the line and label names.
        self.main_window.workoutGraphWidget.plot(x, y, pen=pg.mkPen(color=line_color, width=2), name=data_name)

        label_style = {'color': '#808080', 'font-size': '14pt'}
        self.main_window.workoutGraphWidget.setLabel("bottom", "Minutes", **label_style)
        self.main_window.workoutGraphWidget.setLabel("left", data_name, **label_style)

    @staticmethod
    def convert_timestamps(timestamps):
        """
        Converts a list of timestamps into a list of minutes so it can be used as the x-coordinates in a graph.

        :param timestamps: A list of timestamps where each timestamp has the format "HH:MM:SS".
        """
        minutes = []
        for timestamp in timestamps:
            # Adding the seconds from the timestamp in minutes.
            time_minutes = int(timestamp[6:]) / 60
            # Adding the minutes from the timestamp.
            time_minutes += int(timestamp[3:5])
            # Adding the hours from the timestamp in minutes.
            time_minutes += int(timestamp[:2]) * 60

            minutes.append(time_minutes)

        return minutes
