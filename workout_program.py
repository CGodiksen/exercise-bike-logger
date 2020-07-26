"""
Module containing a class and methods related to workout programs which are preset plans that precisely describe
when to increase and decrease the resistance level to offer a more varied workout experience.
"""


class WorkoutProgram:
    """
    This class has two uses. It can return a list of x-coordinates and a list of y-coordinates for a given level, time
    and program. These lists make it possible to accurately graph the workout program which is necessary in the
    configure dialog window where we want to show each workout program as an option and in the live workout window where
    we want to show the live progression over the program.

    Furthermore the class makes it possible to get a dictionary where keys are timestamps describing when the resistance
    level should be changed and the corresponding values are the new resistance level. These dictionaries can then be
    used in the bluetooth session to change the resistance level correctly throughout the session.
    """
    def __init__(self, level, duration, program):
        """
        Method called when a WorkoutProgram object is initialized.

        :param level: The base intensity level of the workout.
        :param duration: The total duration of the workout in minutes.
        :param program: The chosen workout program.
        """
        self.level = level
        self.duration = duration
        self.program = program

        # Initializing the x-coordinates as a sequence of numbers up to the given duration since the x-axis is "time".
        self.x_coordinates = [i for i in range(1, duration + 1)]

        # The y-coordinates are initialized based on the specific program since the y-axis is "level".
        self.y_coordinates = []

        # This dictionary will contain a key-value pair for each time the resistance level should be changed where the
        # key is when the change should happen and the corresponding value is the new level.
        self.level_changes = {}

        # Calling the correct method based on the given program.
        getattr(self, program.replace(" ", "_"))()

    def constant(self):
        """Setting the y-coordinates for the constant program. There are no level changes so we leave it empty."""
        self.y_coordinates = [self.level for i in range(0, self.duration)]

    def program_1(self):
        """
        Setting the y-coordinates and level changes for program 1. This program slowly increases the resistance level
        over the entire workout.
        """

    def program_2(self):
        """
        Setting the y-coordinates and level changes for program 2.
        """

    def program_3(self):
        """
        Setting the y-coordinates and level changes for program 3.
        """

    def program_4(self):
        """
        Setting the y-coordinates and level changes for program 4.
        """

    def program_5(self):
        """
        Setting the y-coordinates and level changes for program 5.
        """
