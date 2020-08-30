import json
import os

from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class WorkoutListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(WorkoutListModel, self).__init__()

        # The list that will contain a dictionary for each workout with a key-value pair for each attribute.
        self.workouts = []

    def data(self, QModelIndex, role=None):
        """
        Returns the data stored under the given role for the item referred to by the index.

        :param QModelIndex: The specific index of the model that we wish to extract data for.
        :param role: The specific data that we wish to extract.
        :return: A formatted string showing the date, program and level of the workout if the role is DisplayRole.
        """
        date = self.workouts[QModelIndex.row()]["date_time"]
        program = self.workouts[QModelIndex.row()]["program_name"]
        level = self.workouts[QModelIndex.row()]["program_level"]

        if role == Qt.DisplayRole:
            return f"\n {date} - {program} - Level {level}\n"

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Simple function that returns the total rowcount of the internal model representation. Since we use a list this
        is simply the length of the list.
        """
        return len(self.workouts)

    def load_workouts(self):
        """Loading the workouts from the json files in the "workouts" folder into the internal model."""
        self.workouts.clear()

        for filename in os.listdir("data/workouts"):
            with open(f"data/workouts/{filename}", "r") as jsonfile:
                self.workouts.append(json.load(jsonfile))

        # Reversing the list so the most recent workout is first.
        self.workouts.reverse()
