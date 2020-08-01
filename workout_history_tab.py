import pyqtgraph as pg

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
            # Getting a dictionary containing the data from the selected workout.
            workout = self.main_window.model.workouts[index.row()]

            # Setting the labels of the display to the corresponding data from the workout.
            self.main_window.dateLabel.setText(workout["date_time"])
            self.main_window.programLabel.setText(workout["program_name"])
            self.main_window.levelLabel.setText(str(workout["program_level"]))
            self.main_window.timeLabel.setText(str(workout["total_duration"]))
            self.main_window.distanceLabel.setText(f"{workout['total_distance']} km")
            self.main_window.caloriesLabel.setText(str(workout["total_calories"]))
            self.main_window.avgSpeedLabel.setText(f"{workout['avg_speed']} km/h")
            self.main_window.avgRPMLabel.setText(str(workout["avg_rpm"]))
            self.main_window.avgHeartRateLabel.setText(str(workout["avg_heart_rate"]))
            self.main_window.avgWattLabel.setText(str(workout["avg_watt"]))
            self.main_window.maxSpeedLabel.setText(f"{workout['max_speed']} km/h")
            self.main_window.maxRPMLabel.setText(str(workout["max_rpm"]))
            self.main_window.maxHeartRateLabel.setText(str(workout["max_heart_rate"]))
            self.main_window.maxWattLabel.setText(str(workout["max_watt"]))

            self.update_graph()

    def update_graph(self):
        """Updating the graph with data from the current configuration."""
        index = self.main_window.workoutListView.selectedIndexes()[0]

        if index:
            # Getting a dictionary containing the data from the selected workout.
            workout = self.main_window.model.workouts[index.row()]

            # Getting the specific data that should be plotted from the graph combo box.
            data_name = self.main_window.workoutGraphComboBox.currentText()

            # Converting the timestamps into minutes and using them as the x-coordinate.
            x = [seconds / 60 for seconds in self.main_window.timestamps_to_seconds(workout["time"])]

            # Initializing the y-coordinates.
            y = workout[data_name.lower().replace(" ", "_")]

            self.main_window.workoutGraphWidget.clear()

            # Choosing the color of the line based on the index of the combo box to ensure each line is unique.
            colors = ["#4b6bc8", "#FFFF00", "#CD0000", "#008000", "#800080", "#FFA500", "#00FFD2"]
            line_color = colors[self.main_window.workoutGraphComboBox.currentIndex()]

            # Plotting the content in the graph, including the line and label names.
            self.main_window.workoutGraphWidget.plot(x, y, pen=pg.mkPen(color=line_color, width=2), name=data_name)

            label_style = {'color': '#808080', 'font-size': '14pt'}
            self.main_window.workoutGraphWidget.setLabel("bottom", "Minutes", **label_style)
            self.main_window.workoutGraphWidget.setLabel("left", data_name, **label_style)
