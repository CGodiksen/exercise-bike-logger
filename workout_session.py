import csv
import json
import os
import statistics
from pathlib import Path


class WorkoutSession:
    """
    This class describes a single workout session. Data from the exercise bike can be processed and saved. When the
    session is done the data can be saved to a file and further information can be extracted and saved separately.
    """

    def __init__(self, program, filename):
        """
        Method called when a WorkoutSession instance is initialized.

        :param program: The workout program containing the level, duration and level changes of the workout.
        :param filename: The CSV file in which the processed data should be saved.
        """
        self.program = program
        self.filename = filename

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
        Processing the data from the workout session, extracting information about the data and saving it to the
        "workouts.csv" file containing a single row for each workout session. Since this method is called when the
        session is over, we also serialize the object to a file to save the data for later use.
        """
        # Adding each element that should be in the row, starting with the Epoch time of the workout.
        new_row = [self.filename]

        # Adding the elements that can be extracted from the chosen workout program.
        new_row.append(self.program.program_name)
        new_row.append(self.program.level)

        # Adding the simple elements duration, distance and calories that are extracted by looking at single rows.
        new_row.append(self.time[-1])
        new_row.append(self.distance[-1])
        new_row.append(self.calories[-1])

        # Adding average speed, average rpm, average heart rate and average watt rounded to two decimals.
        new_row.append(round(statistics.mean(self.speed), 2))
        new_row.append(round(statistics.mean(self.rpm), 2))
        new_row.append(round(statistics.mean(self.heart_rate), 2))
        new_row.append(round(statistics.mean( self.watt), 2))

        # Adding max speed, max rpm, max heart rate and max watt.
        new_row.append(max(self.speed))
        new_row.append(max(self.rpm))
        new_row.append(max(self.heart_rate))
        new_row.append(max(self.watt))

        with open(f"data/workouts.csv", "a+", newline="") as csvfile:
            data_writer = csv.writer(csvfile)

            # If the file is empty then we start by adding a header.
            if os.stat(f"data/workouts.csv").st_size == 0:
                data_writer.writerow(["date", "program", "level", "duration", "distance", "calories", "avg_speed",
                                      "avg_rpm", "avg_heart_rate", "avg_watt", "max_speed", "max_rpm", "max_heart_rate",
                                      "max_watt"])

            data_writer.writerow(new_row)

        # Serializing the session to save it for later use.
        with open(f"data/workouts/{self.filename}.json", "w+", encoding='utf-8') as jsonfile:
            # Getting the instance as a dictionary and removing the attributes that we do not want to save.
            session_dict = self.__dict__
            del session_dict["program"]
            del session_dict["filename"]

            # Saving the remaining attributes to the json file.
            json.dump(self.__dict__, jsonfile, ensure_ascii=False)

    @staticmethod
    def __create_storage_setup():
        """Creates the needed storage setup if it does not already exist."""
        # Creating the "data/workouts" directories if they do not already exist.
        Path("data/workouts").mkdir(parents=True, exist_ok=True)
