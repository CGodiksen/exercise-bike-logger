import asyncio
import struct
import time

import bleak
from PyQt5 import QtWidgets, uic, QtCore

from settings import Settings

READ = struct.pack('BBBBB', 0xf0, 0xa2, 0x01, 0x01, 0x94)


class ConnectDialog(QtWidgets.QDialog):
    """Class representing the dialog window that allows the user to connect with the exercise bike."""
    def __init__(self, main_window, *args, **kwargs):
        super(ConnectDialog, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/connectdialog.ui", self)

        # Used to enable the "New workout" button when a connection is established.
        self.main_window = main_window

        # Setting up the model that handles the device list view.
        self.model = DeviceListModel()
        self.deviceListView.setModel(self.model)

        self.uuid = None
        self.settings = Settings()

        self.accepted.connect(self.ok)
        self.rejected.connect(lambda: self.model.devices.clear())
        self.updateButton.clicked.connect(self.model.update_nearby_devices)

    def ok(self):
        """Getting the writeable uuid using the chosen MAC address and saving the connection settings."""
        index = None
        try:
            index = self.deviceListView.selectedIndexes()[0]
        except IndexError as e:
            print(f"Connect dialog: {e}")

        if index:
            address = self.model.devices[index.row()]["address"]

            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.get_writeable_uuid(address, loop))

            # If the uuid is not none it means a viable exercise bike was chosen and we therefore save the settings.
            if self.uuid is not None:
                self.settings.address = address
                self.settings.characteristic_uuid = self.uuid
                self.settings.save_settings()

                # Ensuring that the "New workout" button is enabled now that a connection can be established.
                self.main_window.newWorkoutButton.setEnabled(True)

        self.model.devices.clear()

    async def get_writeable_uuid(self, address, loop):
        """
        Looping through the characteristics of the given device and saving the uuid if a writeable characteristic
        is found. In this context "writeable" is defined as returning the correct notification when a READ packet is
        written to the characteristic, meaning that the given device is a viable exercise bike.

        :param address: The MAC address of the BLE device that should be checked for writeable characteristics.
        :param loop: The event loop used to connect to the device.
        """
        try:
            async with bleak.BleakClient(address, loop=loop) as client:
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
            await self.get_writeable_uuid(address, loop)

    def notification_handler(self, sender, data):
        """
        Handling the notifications that are received from a characteristic. If the correct notification is received we
        know the users chosen device is a viable exercise bike and we therefore save the characteristic uuid.
        """
        # If the data has a length of 21 we know it is a response from the READ write operation.
        if len(data) == 21:
            self.uuid = sender


class DeviceListModel(QtCore.QAbstractListModel):
    """Class representing the list of devices shown in the connect dialog window."""
    def __init__(self):
        super(DeviceListModel, self).__init__()

        # The list that will contain a dictionary for each device.
        self.devices = []

    def data(self, QModelIndex, role=None):
        """
        Returns the data stored under the given role for the item referred to by the index.

        :param QModelIndex: The specific index of the model that we wish to extract data for.
        :param role: The specific data that we wish to extract.
        :return: The name and address of the device if the role is DisplayRole.
        """
        name = self.devices[QModelIndex.row()]["name"]
        address = self.devices[QModelIndex.row()]["address"]

        if role == QtCore.Qt.DisplayRole:
            return f"\n{name} - {address}\n"

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Simple function that returns the total rowcount of the internal model representation. Since we use a list this
        is simply the length of the list.
        """
        return len(self.devices)

    def update_nearby_devices(self):
        """Scans for nearby Bluetooth LE devices and adds each found device to the internal list model."""
        loop = asyncio.get_event_loop()
        devices = loop.run_until_complete(bleak.discover(2.5))

        self.devices.clear()
        for device in devices:
            self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
            self.devices.append({"name": device.name, "address": device.address})
            self.endInsertRows()
