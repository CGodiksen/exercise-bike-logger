"""
Module containing a class and methods related to workout programs which are preset plans that precisely describe
when to increase and decrease the resistance level to offer a more varied workout experience.
"""


class WorkoutProgram:
    """
    This class provides two instance attributes that can be used to graph a specific workout program as well as give
    information as to when the resistance level should be changed during the workout. When used in a graph the x-axis
    should be "time" in minutes and the y-axis should be "level".
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
        self.x_coordinates = [i for i in range(0, duration)]

        # The y-coordinates are initialized based on the specific program since the y-axis is "level".
        self.y_coordinates = []

        # Calling the correct method based on the given program.
        getattr(self, program.replace(" ", "_"))()

    def constant(self):
        """Setting the y-coordinates for the constant program. There are no level changes so we leave it empty."""
        self.y_coordinates = [self.level for i in range(0, self.duration)]

    def program_1(self):
        """
        Setting the y-coordinates for program 1. This program slowly increases the resistance level
        by a constant rate over the entire workout.
        """
        # Example: level = 10, duration = 10, change_rate = 2, y_coordinates = [10, 10, 11, 11, 12, 12, 13, 13, 14, 14]
        change_rate = round(self.duration / 5)
        for minute in self.x_coordinates:
            if minute % change_rate == 0:
                self.level += 1
            self.y_coordinates.append(self.level)

    def program_2(self):
        """
        Setting the y-coordinates for program 2. This program increases the resistance level by a constant rate for the
        first half of the session and then decreases the level back to the initial resistance by the same rate.
        """

    def program_3(self):
        """
        Setting the y-coordinates for program 3.
        """

    def program_4(self):
        """
        Setting the y-coordinates for program 4.
        """

    def program_5(self):
        """
        Setting the y-coordinates for program 5.
        """
