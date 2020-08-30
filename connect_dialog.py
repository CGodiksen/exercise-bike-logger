import asyncio
import struct
import time
import bleak

from worker import Worker
from PyQt5 import QtWidgets, uic, QtCore

READ = struct.pack('BBBBB', 0xf0, 0xa2, 0x01, 0x01, 0x94)


class ConnectDialog(QtWidgets.QDialog):
    """Class representing the dialog window that allows the user to connect with the exercise bike."""
    def __init__(self, *args, **kwargs):
        super(ConnectDialog, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/connectdialog.ui", self)

        # Setting up the model that handles the device list view.
        self.model = DeviceListModel()
        self.deviceListView.setModel(self.model)

        self.updateButton.clicked.connect(self.model.update_nearby_devices)

    async def get_writeable_uuid(self, mac_address, loop):
        try:
            async with bleak.BleakClient(mac_address, loop=loop) as client:
                services = await client.get_services()
                for key, value in services.characteristics.items():
                    try:
                        await client.start_notify(value.uuid, self.notification_handler)
                        time.sleep(0.5)
                        await client.write_gatt_char(value.uuid, READ)
                    except bleak.BleakError as e:
                        print(f"Bleak raised an exception: {e}")
        except bleak.BleakError as e:
            print(f"Bleak raised an exception: {e}")
            await self.get_writeable_uuid(mac_address, loop)

    @staticmethod
    def notification_handler(sender, data):
        """Handling the notifications that are received from a characteristic."""
        # If the data has a length of 21 we know it is a response from the READ write operation.
        if len(data) == 21:
            print(sender)


class DeviceListModel(QtCore.QAbstractListModel):
    """Class representing the list of devices shown in the connect dialog window."""
    def __init__(self):
        super(DeviceListModel, self).__init__()

        # The list that will contain a dictionary for each device.
        self.devices = []

        self.threadpool = QtCore.QThreadPool()

    def update_nearby_devices(self):
        loop = asyncio.get_event_loop()
        worker = Worker(loop.run_until_complete, self.get_devices())
        self.threadpool.start(worker)

    def data(self, QModelIndex, role=None):
        """
        Returns the data stored under the given role for the item referred to by the index.

        :param QModelIndex: The specific index of the model that we wish to extract data for.
        :param role: The specific data that we wish to extract.
        :return: The name and address of the device if the role is DisplayRole.
        """
        name = self.devices[QModelIndex.row()]["name"]
        mac_address = self.devices[QModelIndex.row()]["mac_address"]

        if role == QtCore.Qt.DisplayRole:
            return f"\n{name} - {mac_address}\n"

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Simple function that returns the total rowcount of the internal model representation. Since we use a list this
        is simply the length of the list.
        """
        return len(self.devices)

    async def get_devices(self):
        devices = await bleak.discover()
        for device in devices:
            self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
            self.devices.append({"name": device.name, "mac_address": device.address})
            self.endInsertRows()
