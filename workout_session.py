import json
import statistics
from datetime import datetime
from pathlib import Path


class WorkoutSession:
    """
    This class describes a single workout session. Data from the exercise bike can be processed and saved. When the
    session is done the data can be saved to a file and further information can be extracted and saved separately.
    """

    def __init__(self, program, unix_time):
        """
        Method called when a WorkoutSession instance is initialized.

        :param program: The workout program containing the level, duration and level changes of the workout.
        :param unix_time: The name of the json file in which the processed data should be saved.
        """
        self.program = program
        self.unix_time = unix_time

        # Initializing the instance attributes that are going to be saved to the json file.
        self.date_time = datetime.fromtimestamp(int(self.unix_time)).strftime('%d-%m-%Y %H:%M:%S')
        self.program_name = program.program_name
        self.program_level = program.level
        self.total_duration = program.duration
        self.total_distance = None
        self.total_calories = None
        self.avg_speed = None
        self.avg_rpm = None
        self.avg_heart_rate = None
        self.avg_watt = None
        self.max_speed = None
        self.max_rpm = None
        self.max_heart_rate = None
        self.max_watt = None
        self.time = []
        self.speed = []
        self.rpm = []
        self.distance = []
        self.calories = []
        self.heart_rate = []
        self.watt = []
        self.level = []

        self.__create_storage_setup()

    def process_read_response(self, data, display_updater):
        """
        Processing the response from the READ write operation and saving the processed data to the instance.

        :param data: The data package that contains information about the current state of the workout session.
        :param display_updater: The function that updates the display widgets on the live workout page.
        """

        # Doing necessary data preprocessing.
        data = [element - 1 for element in data]

        # Adding each element of data from the READ response to the corresponding instance attributes.
        self.time.append(f"{data[3]:02d}:{data[4]:02d}:{data[5]:02d}")

        self.speed.append(round(((100 * (data[6]) + data[7]) / 10.0), 1))

        self.rpm.append((100 * (data[8]) + data[9]))

        self.distance.append(round(((100 * (data[10]) + data[11]) / 10.0), 1))

        self.calories.append((100 * (data[12]) + data[13]))

        self.heart_rate.append((100 * (data[14]) + data[15]))

        self.watt.append(round(((100 * (data[16]) + data[17]) / 10.0), 1))

        self.level.append(data[18])

        # Updating the display widgets on the live workout page.
        display_updater(self.time[-1], self.speed[-1], self.rpm[-1], self.distance[-1], self.calories[-1],
                        self.heart_rate[-1], self.watt[-1])

    def process_workout_session(self):
        """
        Processing the data from the workout session, extracting information about the data and saving it to an unique
        json file.
        """
        # Adding the simple elements total distance and calories that are extracted by looking at the last element.
        self.total_distance = self.distance[-1]
        self.total_calories = self.calories[-1]

        # Adding average speed, average rpm, average heart rate and average watt rounded to two decimals.
        self.avg_speed = round(statistics.mean(self.speed), 2)
        self.avg_rpm = round(statistics.mean(self.rpm), 2)
        self.avg_heart_rate = round(statistics.mean(self.heart_rate), 2)
        self.avg_watt = round(statistics.mean( self.watt), 2)

        # Adding max speed, max rpm, max heart rate and max watt.
        self.max_speed = max(self.speed)
        self.max_rpm = max(self.rpm)
        self.max_heart_rate = max(self.heart_rate)
        self.max_watt = max(self.watt)

        # Serializing the session to save it for later use.
        with open(f"data/workouts/{self.unix_time}.json", "w+", encoding='utf-8') as jsonfile:
            # Getting the instance as a dictionary and removing the attributes that we do not want to save.
            session_dict = self.__dict__
            del session_dict["program"]
            del session_dict["unix_time"]

            # Saving the remaining attributes to the json file.
            json.dump(self.__dict__, jsonfile, ensure_ascii=False)

    @staticmethod
    def __create_storage_setup():
        """Creates the needed storage setup if it does not already exist."""
        # Creating the "data/workouts" directories if they do not already exist.
        Path("data/workouts").mkdir(parents=True, exist_ok=True)
