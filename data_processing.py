"""
Module containing helper functions for processing the data from the exercise bike and processing that data to extract
further information about the workout session. Two CSV files are manipulated in this module, the unique CSV file for
the specific workout and the CSV file containing a row for each workout.
"""
import struct


def process_read_response(data):
    """Processing the response from the READ write operation and saving the processed data to a csv file."""
    data = struct.unpack('BBBBBBBBBBBBBBBBBBBBB', data)

    # Doing necessary data preprocessing.
    data = [element - 1 for element in data]

    print(data)

    print(f"Time: {data[2]:02d}:{data[3]:02d}:{data[4]:02d}:{data[5]:02d}")

    speed = ((100 * (data[6]) + data[7]) / 10.0)
    print(f"Speed: {speed:3.1f} km/h")

    rpm = (100 * (data[8]) + data[9])
    print(f"RPM: {rpm:3d}")

    distance = ((100 * (data[10]) + data[11]) / 10.0)
    print(f"Distance: {distance:3.1f} km")

    calories = (100 * (data[12]) + data[13])
    print(f"Calories: {calories:3d} kcal")

    hr = (100 * (data[14]) + data[15])
    print(f"Heart rate: {hr:3d}")

    power = ((100 * (data[16]) + data[17]) / 10.0)
    print(f"Power: {power:3.1f} W")

    lvl = data[18]
    print(f"Level: {lvl}\n")
