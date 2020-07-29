import csv
import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class WorkoutListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(WorkoutListModel, self).__init__()

        self.workouts = []

    def data(self, QModelIndex, role=None):
        """
        Returns the data stored under the given role for the item referred to by the index.

        :param QModelIndex: The specific index of the model that we wish to extract data for.
        :param role: The specific data that we wish to extract.
        :return: The name of the subreddit if the role is DisplayRole.
        """
        date = datetime.datetime.fromtimestamp(int(self.workouts[QModelIndex.row()][0])).strftime('%d-%m-%Y %H:%M:%S')
        program = self.workouts[QModelIndex.row()][1]
        level = self.workouts[QModelIndex.row()][2]
        time = self.workouts[QModelIndex.row()][3]
        distance = self.workouts[QModelIndex.row()][4]

        if role == Qt.DisplayRole:
            return f"{date} - {program} - Level {level}\nDuration: {time} - Distance: {distance} km"

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Simple function that returns the total rowcount of the internal model representation. Since we use a list this
        is simply the length of the list.
        """
        return len(self.workouts)

    def load_workouts(self):
        """Loading the workouts from the workouts.csv file into the internal model."""
        with open("data/workouts.csv", "r") as csvfile:
            workout_reader = csv.reader(csvfile)

            # Skipping the header.
            next(workout_reader, None)

            for row in workout_reader:
                self.workouts.append(row)

            # Reversing the list so the most recent workout is first.
            self.workouts.reverse()
