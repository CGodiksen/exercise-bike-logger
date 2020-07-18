"""
Module containing helper functions for processing the data from the exercise bike and processing that data to extract
further information about the workout session. Two CSV files are manipulated in this module, the unique CSV file for
the specific workout and the CSV file containing a row for each workout.
"""
import csv
import struct
import os
from pathlib import Path


def create_storage_setup():
    """Creates the needed storage setup if it does not already exist."""
    # Creating the "data/workouts" directories if they do not already exist.
    Path("data/workouts").mkdir(parents=True, exist_ok=True)


def process_read_response(data, filename):
    """
    Processing the response from the READ write operation and saving the processed data to a csv file.

    :param data: The data package that contains information about the current state of the workout session.
    :param filename: The filename of the CSV file where the processed data should be saved.
    """
    create_storage_setup()

    data = struct.unpack('BBBBBBBBBBBBBBBBBBBBB', data)

    # Doing necessary data preprocessing.
    data = [element - 1 for element in data]

    row = [f"{data[2]:02d}:{data[3]:02d}:{data[4]:02d}:{data[5]:02d}"]

    speed = ((100 * (data[6]) + data[7]) / 10.0)
    row.append(f"{speed:3.1f}")

    rpm = (100 * (data[8]) + data[9])
    row.append(f"{rpm}")

    distance = ((100 * (data[10]) + data[11]) / 10.0)
    row.append(f"{distance:3.1f}")

    calories = (100 * (data[12]) + data[13])
    row.append(f"{calories}")

    hr = (100 * (data[14]) + data[15])
    row.append(f"{hr}")

    power = ((100 * (data[16]) + data[17]) / 10.0)
    row.append(f"{power:3.1f}")

    lvl = data[18]
    row.append(f"{lvl}")

    with open(f"data/workouts/{filename}.csv", "a+", newline="") as csvfile:
        data_writer = csv.writer(csvfile)

        # If the file is empty then we start by adding a header.
        if os.stat(f"data/workouts/{filename}.csv").st_size == 0:
            data_writer.writerow(["time", "speed", "rpm", "distance", "calories", "heart_rate", "watt", "level"])

        data_writer.writerow(row)
