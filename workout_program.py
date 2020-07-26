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

    def program_1(self):
        """Setting the y-coordinates for program 1. This program keeps the level the same throughout."""
        self.y_coordinates = [self.level for i in range(0, self.duration)]

    def program_2(self):
        """
        Setting the y-coordinates for program 2. This program slowly increases the resistance level
        by a constant rate over the entire workout.

        Example: level = 10, duration = 10, change_rate = 2, y_coordinates = [10, 10, 11, 11, 12, 12, 13, 13, 14, 14]
        """
        level = self.level
        change_rate = round(self.duration / 5)
        for minute in self.x_coordinates:
            if minute % change_rate == 0 and minute != 0:
                level += 1
            self.y_coordinates.append(level)

    def program_3(self):
        """
        Setting the y-coordinates for program 3. This program increases the resistance level by a constant rate for the
        first half of the session and then decreases the level back to the initial resistance by the same rate.

        Example: level = 10, duration = 10, change_rate = 1, y_coordinates = [10, 11, 12, 13, 14, 14, 13, 12, 11, 10]
        """
        level = self.level
        first_half = self.x_coordinates[:len(self.x_coordinates)//2]
        second_half = self.x_coordinates[len(self.x_coordinates)//2:]
        change_rate = round(len(second_half) / 5)

        for minute in first_half:
            if minute % change_rate == 0 and minute != 0:
                level += 1
            self.y_coordinates.append(level)

        for minute in second_half:
            if minute % change_rate == 0 and minute != second_half[0]:
                level -= 1
            self.y_coordinates.append(level)

    def program_4(self):
        """
        Setting the y-coordinates for program 3. This program repeats 5 minute sections where the first 2 minutes are
        the initial level, the next two are two levels higher and the last minute is two levels higher again.

        Example: level = 10, duration = 10, y_coordinates = [10, 10, 12, 12, 14, 10, 10, 12, 12, 14]
        """
        level = self.level
        for minute in self.x_coordinates:
            if minute % 5 == 0:
                level = self.level
            if minute % 5 == 2:
                level += 2
            if minute % 5 == 4:
                level += 2
            self.y_coordinates.append(level)

    def program_5(self):
        """
        Setting the y-coordinates for program 4. This program starts with a warm-up and ends with a cool down, the
        rest is constant. The level increases by two over the first two minutes and decreases by two over the last two.

        Example: level = 10, duration = 10, y_coordinates = [10, 11, 12, 12, 12, 12, 12, 12, 11, 10]
        """
        self.y_coordinates.append(self.level)
        self.y_coordinates.append(self.level + 1)

        for _ in self.x_coordinates[2:-2]:
            self.y_coordinates.append(self.level + 2)

        self.y_coordinates.append(self.level + 1)
        self.y_coordinates.append(self.level)
