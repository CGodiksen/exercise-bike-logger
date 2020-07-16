import struct

import bleak

# Defining the data that can be written to the characteristic.
INIT_A0 = struct.pack('BBBBB', 0xf0, 0xa0, 0x02, 0x02, 0x94)
PING = struct.pack('BBBBB', 0xf0, 0xa0, 0x01, 0x01, 0x92)
PONG = struct.pack('BBBBB', 0xf0, 0xb0, 0x01, 0x01, 0xa2)
STATUS = struct.pack('BBBBB', 0xf0, 0xa1, 0x01, 0x01, 0x93)
INIT_A3 = struct.pack('BBBBBB', 0xf0, 0xa3, 0x01, 0x01, 0x01, 0x96)
INIT_A4 = struct.pack('BBBBBBBBBBBBBBB', 0xf0, 0xa4, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                      0x01, 0x01, 0xa0)
START = struct.pack('BBBBBB', 0xf0, 0xa5, 0x01, 0x01, 0x02, 0x99)
STOP = struct.pack('BBBBBB', 0xf0, 0xa5, 0x01, 0x01, 0x04, 0x9b)
READ = struct.pack('BBBBB', 0xf0, 0xa2, 0x01, 0x01, 0x94)


async def get_nearby_devices():
    """Finds nearby bluetooth low energy devices."""
    return await bleak.discover(5)


class Bluetooth:
    """
    Class that handles all bluetooth connectivity including finding nearby devices, connecting the the exercise bike,
    configuring the workout session and reading data from the exercise bike once the session has started.
    """
    def __init__(self, address, loop):
        # The characteristic that should be written to. # TODO Find a way to avoid this being hardcoded.
        self.CHARACTERISTIC_UUID = "***REMOVED***"

        self.address = address
        self.loop = loop

    async def connect_to_device(self):
        """
        Connecting to the device that is associated with the given MAC address. The resistance level of the workout
        session can be configured immediately after this method is called.
        """
        # A very specific protocol is followed to ensure that the connection with the exercise bike is initialized
        # correctly.
        async with bleak.BleakClient(self.address, loop=self.loop) as client:
            # Activating notifications on the characteristic that is written to.
            await client.start_notify(self.CHARACTERISTIC_UUID, self.notification_handler)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, PING)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, INIT_A0)

            for i in range(5):
                await client.write_gatt_char(self.CHARACTERISTIC_UUID, PING)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, INIT_A3)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, INIT_A4)

    async def set_level(self, level):
        """Setting the resistance level for the workout session."""
        async with bleak.BleakClient(self.address, loop=self.loop) as client:
            lvl = struct.pack('BBBBBB', 0xf0, 0xa6, 0x01, 0x01, level + 1, (0xf0 + 0xa6 + 3 + level) & 0xFF)
            client.write_gatt_char(self.CHARACTERISTIC_UUID, lvl)

    async def start_session(self):
        """Starting the workout session."""
        async with bleak.BleakClient(self.address, loop=self.loop) as client:
            await client.write_gatt_char(self.CHARACTERISTIC_UUID, START)

    async def read_data(self):
        """Reading the current data from the exercise bike. Should be called while the workout session is active."""
        async with bleak.BleakClient(self.address, loop=self.loop) as client:
            await client.write_gatt_char(self.CHARACTERISTIC_UUID, READ, response=True)

    @staticmethod
    def notification_handler(sender, data):
        """Handling the notifications that are received from a characteristic."""
        return data
