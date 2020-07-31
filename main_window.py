from PyQt5 import QtWidgets, uic

from workout_list_model import WorkoutListModel
from workout_history_tab import WorkoutHistoryTab
from statistics_tab import StatisticsTab
from settings_dialog import SettingsDialog
from configure_dialog import ConfigureDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/mainwindow.ui", self)

        # Setting up the model that handles the workout list view.
        self.model = WorkoutListModel()
        self.model.load_workouts()
        self.workoutListView.setModel(self.model)

        # Setting up the two tabs on the main window.
        self.workout_history_tab = WorkoutHistoryTab(self)
        self.statistics_tab = StatisticsTab(self)

        # Connecting the buttons with their respective functionality.
        self.configure_dialog = ConfigureDialog()
        self.newWorkoutButton.clicked.connect(self.configure_dialog.show)

        self.settings_dialog = SettingsDialog()
        self.settingsButton.clicked.connect(self.settings_dialog.show)

    @staticmethod
    def timestamps_to_seconds(timestamps):
        """
        Converts a list of timestamps into a list of seconds.

        :param timestamps: A list of timestamps where each timestamp has the format "HH:MM:SS".
        """
        seconds = []
        for timestamp in timestamps:
            # Adding the seconds from the timestamp.
            time_minutes = int(timestamp[6:])
            # Adding the seconds from the timestamp in seconds.
            time_minutes += int(timestamp[3:5]) * 60
            # Adding the hours from the timestamp in seconds.
            time_minutes += int(timestamp[:2]) * 3600

            seconds.append(time_minutes)

        return seconds
