from PyQt5 import QtWidgets, uic

from workout_list_model import WorkoutListModel
from workout_history_tab import WorkoutHistoryTab
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

        # Setting up the workout history tab.
        self.workout_history_tab = WorkoutHistoryTab(self)

        # Connecting the buttons with their respective functionality.
        self.configure_dialog = ConfigureDialog()
        self.newWorkoutButton.clicked.connect(self.configure_dialog.show)

        self.settings_dialog = SettingsDialog()
        self.settingsButton.clicked.connect(self.settings_dialog.show)
