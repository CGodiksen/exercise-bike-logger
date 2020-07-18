"""
Module that handles all bluetooth connectivity including finding nearby devices, connecting the the exercise bike,
configuring the workout session and reading data from the exercise bike once the session has started.
"""
import struct
import time

import bleak
import data_processing

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


# TODO: Make it so it keeps trying to connect if the device can't be found.
# TODO: Split this method into multiple methods.
async def start_session(level, duration, characteristic_uuid, address, loop):
    """
    Connecting to the device that is associated with the given MAC address, configuring the resistance level of the
    workout, starting the workout session and reading data from the bike every second until it is finished.

    :param level: The resistance level that is chosen for this specific workout.
    :param duration: The duration of the workout session in seconds.
    :param characteristic_uuid: The id of the characteristic that we wish to read from.
    :param address: The MAC address of the device we want to connect to.
    :param loop: The asyncio event loop that is used by the BleakClient.
    """
    # A very specific protocol is followed to ensure that the connection with the exercise bike is initialized
    # correctly.
    async with bleak.BleakClient(address, loop=loop) as client:
        # Activating notifications on the characteristic that is written to.
        await client.start_notify(characteristic_uuid, notification_handler)

        await client.write_gatt_char(characteristic_uuid, PING, response=True)

        await client.write_gatt_char(characteristic_uuid, INIT_A0, response=True)

        for i in range(5):
            await client.write_gatt_char(characteristic_uuid, PING, response=True)

        await client.write_gatt_char(characteristic_uuid, INIT_A3, response=True)

        await client.write_gatt_char(characteristic_uuid, INIT_A4, response=True)

        # Setting the resistance level for the workout session.
        lvl = struct.pack('BBBBBB', 0xf0, 0xa6, 0x01, 0x01, level + 1, (0xf0 + 0xa6 + 3 + level) & 0xFF)
        await client.write_gatt_char(characteristic_uuid, lvl, response=True)

        time.sleep(0.5)

        # Starting the workout session.
        await client.write_gatt_char(characteristic_uuid, START, response=True)

        time.sleep(0.5)

        # Reading the current data from the exercise bike. Should be called while the workout session is active.
        for i in range(duration):
            await client.write_gatt_char(characteristic_uuid, READ, response=True)
            time.sleep(1)

        # Stopping the session on the bike itself and deactivating notifications on the characteristic.
        await client.write_gatt_char(characteristic_uuid, STOP)
        await client.stop_notify(characteristic_uuid)


def notification_handler(sender, data):
    """Handling the notifications that are received from a characteristic."""
    # If the data has a length of 21 we know it is a response from the READ write operation.
    if len(data) == 21:
        data_processing.process_read_response(data)
