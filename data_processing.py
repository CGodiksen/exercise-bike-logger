"""
Module containing helper functions for processing the data from the exercise bike and processing that data to extract
further information about the workout session. Two CSV files are manipulated in this module, the unique CSV file for
the specific workout and the CSV file containing a row for each workout.
"""
import csv
import struct
import os
import datetime
import statistics
from pathlib import Path


def create_storage_setup():
    """Creates the needed storage setup if it does not already exist."""
    # Creating the "data/workouts" directories if they do not already exist.
    Path("data/workouts").mkdir(parents=True, exist_ok=True)


def process_read_response(data, filename, duration, display_updater):
    """
    Processing the response from the READ write operation and saving the processed data to a csv file.

    :param data: The data package that contains information about the current state of the workout session.
    :param filename: The CSV file in which the processed data should be saved.
    :param duration: The total duration of the workout session.
    :param display_updater: The function that updates the display widgets on the live workout page.

    :return: True if the time in the data is equal to the total duration of the workout session, meaning that the
    session is complete. Otherwise returns False. This is used to stop the session at the correct time.
    """
    create_storage_setup()

    data = struct.unpack('BBBBBBBBBBBBBBBBBBBBB', data)

    # Doing necessary data preprocessing.
    data = [element - 1 for element in data]

    # Adding each element of data from the READ response to a single list, starting with the time.
    new_row = [f"{data[3]:02d}:{data[4]:02d}:{data[5]:02d}"]

    speed = ((100 * (data[6]) + data[7]) / 10.0)
    new_row.append(f"{speed:3.1f}")

    rpm = (100 * (data[8]) + data[9])
    new_row.append(f"{rpm}")

    distance = ((100 * (data[10]) + data[11]) / 10.0)
    new_row.append(f"{distance:3.1f}")

    calories = (100 * (data[12]) + data[13])
    new_row.append(f"{calories}")

    heart_rate = (100 * (data[14]) + data[15])
    new_row.append(f"{heart_rate}")

    watt = ((100 * (data[16]) + data[17]) / 10.0)
    new_row.append(f"{watt:3.1f}")

    lvl = data[18]
    new_row.append(f"{lvl}")

    with open(f"data/workouts/{filename}.csv", "a+", newline="") as csvfile:
        data_writer = csv.writer(csvfile)

        # If the file is empty then we start by adding a header.
        if os.stat(f"data/workouts/{filename}.csv").st_size == 0:
            data_writer.writerow(["time", "speed", "rpm", "distance", "calories", "heart_rate", "watt", "level"])

        data_writer.writerow(new_row)

    # Updating the display widgets on the live workout page.
    display_updater(new_row)

    return True if f"{data[3]:02d}:{data[4]:02d}:{data[5]:02d}" == duration else False


def process_workout_session(filename):
    """
    Processing the data from a single workout session, extracting information about the data and saving it to the
    "workouts.csv" file containing a single row for each workout session.

    :param filename: The CSV file containing the data that should be processed.
    """
    with open(f"data/workouts/{filename}.csv", newline="") as csvfile:
        data_reader = csv.DictReader(csvfile)

        # Extracting the csv data into a dictionary containing a key-value pairing for each column.
        data = {}
        for row in data_reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    # Adding each element that should be in the row, starting with the date of the workout.
    new_row = [datetime.datetime.fromtimestamp(int(filename)).strftime('%d-%m-%Y %H:%M:%S')]

    # Adding the simple elements duration, distance, calories and level that are extracted by looking at single rows.
    new_row.append(data["time"][-1])
    new_row.append(data["distance"][-1])
    new_row.append(data["calories"][-1])
    new_row.append(data["level"][0])

    # Adding average speed, average rpm, average heart rate and average watt rounded to two decimals.
    new_row.append(round(statistics.mean(list(map(float, data["speed"]))), 2))
    new_row.append(round(statistics.mean(list(map(int, data["rpm"]))), 2))
    new_row.append(round(statistics.mean(list(map(int, data["heart_rate"]))), 2))
    new_row.append(round(statistics.mean(list(map(float, data["watt"]))), 2))

    # Adding max speed, max rpm, max heart rate and max watt.
    new_row.append(max(list(map(float, data["speed"]))))
    new_row.append(max(list(map(int, data["rpm"]))))
    new_row.append(max(list(map(int, data["heart_rate"]))))
    new_row.append(max(list(map(float, data["watt"]))))

    with open(f"data/workouts.csv", "a+", newline="") as csvfile:
        data_writer = csv.writer(csvfile)

        # If the file is empty then we start by adding a header.
        if os.stat(f"data/workouts.csv").st_size == 0:
            data_writer.writerow(["date", "duration", "distance", "calories", "level", "avg_speed", "avg_rpm",
                                  "avg_heart_rate", "avg_watt", "max_speed", "max_rpm", "max_heart_rate", "max_watt"])

        data_writer.writerow(new_row)
