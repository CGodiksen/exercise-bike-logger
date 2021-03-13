from pathlib import Path

from PyQt5 import QtWidgets, uic, QtCore

from src.settings import Settings
from src.workout_list_model import WorkoutListModel
from src.workout_history_tab import WorkoutHistoryTab
from src.statistics_tab import StatisticsTab
from src.connect_dialog import ConnectDialog
from src.configure_dialog import ConfigureDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/mainwindow.ui", self)

        self.__create_storage_setup()

        self.settings = Settings()
        # If the connection settings are empty, we disable the "New workout" button until a connection is established.
        if self.settings.address == "" or self.settings.characteristic_uuid == "":
            self.newWorkoutButton.setEnabled(False)

        # Setting up the model that handles the workout list view.
        self.model = WorkoutListModel()
        self.model.load_workouts()
        self.workoutListView.setModel(self.model)

        # Setting up the two tabs on the main window.
        self.workout_history_tab = WorkoutHistoryTab(self)
        self.statistics_tab = StatisticsTab(self)

        # Connecting the buttons with their respective functionality.
        self.configure_dialog = ConfigureDialog(self)
        self.newWorkoutButton.clicked.connect(self.configure_dialog.show)

        # self.settings_dialog = SettingsDialog()
        # self.settingsButton.clicked.connect(self.settings_dialog.show)
        self.connect_dialog = ConnectDialog(self)
        self.connectButton.clicked.connect(self.connect_dialog.show)

    def update_window(self):
        """
        Updates the workout history tab and the statistics tab with the current data. This should be called when a
        new workout is finished.
        """
        # Updating the workout list view on the workout history tab.
        self.model.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.model.load_workouts()
        self.model.endInsertRows()

        # Updating the display on the statistics tab with the current data.
        self.statistics_tab.process_workouts()
        self.statistics_tab.update_display()

        # Updating the interactive graph with the current data.
        self.statistics_tab.interactive_data = self.statistics_tab.get_interactive_graph_data(
            self.model.workouts, self.statistics_tab.search_keys)
        self.statistics_tab.update_graph()

    @staticmethod
    def timestamp_to_seconds(timestamp):
        """Converts a timestamp with the format "HH:MM:SS" into the equivalent amount of seconds. """
        # Adding the seconds from the timestamp.
        seconds = int(timestamp[6:])
        # Adding the minutes from the timestamp in seconds.
        seconds += int(timestamp[3:5]) * 60
        # Adding the hours from the timestamp in seconds.
        seconds += int(timestamp[:2]) * 3600

        return seconds

    @staticmethod
    def __create_storage_setup():
        """Creates the needed storage setup if it does not already exist."""
        # Creating the "data/workouts" directories if they do not already exist.
        Path("data/workouts").mkdir(parents=True, exist_ok=True)
