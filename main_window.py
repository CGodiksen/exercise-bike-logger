from workout_window import WorkoutWindow

from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("resources/mainwindow.ui", self)

        # Setting up the live workout window that is opened when the "New workout" button is pressed.
        self.workout_window = WorkoutWindow()
        self.newWorkoutButton.clicked.connect(self.workout_window.show)
