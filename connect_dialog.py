"""
Module containing classes and methods pertaining to the Connect dialog window which shows a list of nearby devices
and allows the user to select the exercise bike that should be connected to. This dialog window is oponed when the user
clicks the "New workout" button on the main window.

The class "ConnectDialog" defines the behavior of the UI while the class "DeviceModel" defines the behavior of the
list model used in the QListView.
"""
import asyncio

import bleak
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QThreadPool, QTimer, Qt

from worker import Worker


class ConnectDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(ConnectDialog, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("resources/connectdialog.ui", self)

        self.model = DeviceModel()
        self.deviceListView.setModel(self.model)

        # Setting up multi threading on a timer which is used to continuously get the nearby devices.
        self.threadpool = QThreadPool()
        self.loop = asyncio.get_event_loop()
        self.worker = Worker(self.loop.run_until_complete, self.update_devices())
        self.threadpool.start(self.worker)

    async def update_devices(self):
        """Finds nearby bluetooth low energy devices."""
        print("hello")
        self.model.devices = await bleak.discover()
        print(self.devices)
        self.layoutChanged.emit()


class DeviceModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(DeviceModel, self).__init__()
        self.devices = []

    def data(self, QModelIndex, role=None):
        """
        Returns the data stored under the given role for the item referred to by the index.
        :param QModelIndex: The specific index of the model that we wish to extract data for.
        :param role: The specific data that we wish to extract.
        :return: The name of the device if the role is DisplayRole.
        """
        print(self.devices[QModelIndex.row()])
        device = self.devices[QModelIndex.row()]

        # TODO: Maybe insert the signal strength.
        if role == Qt.DisplayRole:
            return f"{device.name}: {device.address}"

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Simple function that returns the total rowcount of the internal model representation. Since we use a list this
        is simply the length of the list.
        """
        return len(self.devices)
