import pyqtgraph as pg

from PyQt5 import QtWidgets, uic

from workout_program import WorkoutProgram
from workout_window import WorkoutWindow


class ConfigureDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(ConfigureDialog, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/configuredialog.ui", self)

        self.workout_window = None
        self.program = None

        # Plotting the initial workout program.
        self.plot_program()

        # Every time one of the options get changed we update the program plot to reflect the change.
        self.levelSpinBox.valueChanged.connect(self.plot_program)
        self.timeSpinBox.valueChanged.connect(self.plot_program)
        self.programComboBox.currentIndexChanged.connect(self.plot_program)

        self.accepted.connect(self.ok)

    def ok(self):
        """Creating the workout window using the given configurations."""
        self.workout_window = WorkoutWindow(self.program)
        self.workout_window.show()

    def plot_program(self):
        """Plotting the workout program in the graphWidget to visualize the program for the user."""
        self.program = WorkoutProgram(self.levelSpinBox.value(), self.timeSpinBox.value(),
                                      self.programComboBox.currentText())
        self.graphWidget.clear()

        # Performing cosmetic changes to the coordinate lists to make the visualization clearer.
        x, y = self.program.prettify_line()

        self.graphWidget.plot(x, y, pen=pg.mkPen(color="#4b6bc8"))
