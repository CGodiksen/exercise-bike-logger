"""
Module containing a class and methods related to workout programs which are preset plans that precisely describe
when to increase and decrease the resistance level to offer a more varied workout experience.
"""


class WorkoutProgram:
    """
    This class has two uses. It can return a list of x-coordinates and a list of y-coordinates for a given level, time and
    program. These lists make it possible to accurately graph the workout program which is necessary in the configure dialog
    window where we want to show each workout program as an option and in the live workout window where we want to show the
    live progression over the program.

    Furthermore the class makes it possible to get a dictionary where keys are timestamps describing when the resistance
    level should be changed and the corresponding values are the new resistance level. These dictionaries can then be used
    in the bluetooth session to change the resistance level correctly throughout the session.
    """
    def __init__(self, level, duration):
        """
        Method called when a WorkoutProgram object is initialized.

        :param level: The base intensity level of the workout.
        :param duration: The total duration of the workout.
        """
        self.level = level
        self.duration = duration
