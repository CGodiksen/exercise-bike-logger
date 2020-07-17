import struct
import time

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


# TODO: Make it so it keeps trying to connect if the device can't be found.
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

    # TODO: Split this method into multiple methods.
    async def start_session(self, level, duration):
        """
        Connecting to the device that is associated with the given MAC address, configuring the resistance level of the
        workout, starting the workout session and reading data from the bike every second until it is finished.

        :param level: The resistance level that is chosen for this specific workout.
        :param duration: The duration of the workout session in seconds.
        """
        # A very specific protocol is followed to ensure that the connection with the exercise bike is initialized
        # correctly.
        async with bleak.BleakClient(self.address, loop=self.loop) as client:
            # Activating notifications on the characteristic that is written to.
            await client.start_notify(self.CHARACTERISTIC_UUID, self.notification_handler)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, PING, response=True)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, INIT_A0, response=True)

            for i in range(5):
                await client.write_gatt_char(self.CHARACTERISTIC_UUID, PING, response=True)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, INIT_A3, response=True)

            await client.write_gatt_char(self.CHARACTERISTIC_UUID, INIT_A4, response=True)

            # Setting the resistance level for the workout session.
            lvl = struct.pack('BBBBBB', 0xf0, 0xa6, 0x01, 0x01, level + 1, (0xf0 + 0xa6 + 3 + level) & 0xFF)
            await client.write_gatt_char(self.CHARACTERISTIC_UUID, lvl, response=True)

            time.sleep(0.5)

            # Starting the workout session.
            await client.write_gatt_char(self.CHARACTERISTIC_UUID, START, response=True)

            time.sleep(0.5)

            # Reading the current data from the exercise bike. Should be called while the workout session is active.
            for i in range(duration):
                await client.write_gatt_char(self.CHARACTERISTIC_UUID, READ, response=True)
                time.sleep(1)

            # Stopping the session on the bike itself and deactivating notifications on the characteristic.
            await client.write_gatt_char(self.CHARACTERISTIC_UUID, STOP)
            await client.stop_notify(self.CHARACTERISTIC_UUID)

    @staticmethod
    def notification_handler(sender, data):
        """Handling the notifications that are received from a characteristic."""
        if len(data) == 21:
            data = struct.unpack('BBBBBBBBBBBBBBBBBBBBB', data)

            # Doing necessary data postprocessing.
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
