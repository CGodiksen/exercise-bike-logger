from PyQt5 import QtWidgets, uic

from workout_window import WorkoutWindow


class ConfigureDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(ConfigureDialog, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/configuredialog.ui", self)

        self.workout_window = None

        self.accepted.connect(self.ok)

    def ok(self):
        """Creating the workout window using the given configurations."""
        time = self.timeSpinBox.value()
        level = self.levelSpinBox.value()

        self.workout_window = WorkoutWindow(level, time)
        self.workout_window.show()
