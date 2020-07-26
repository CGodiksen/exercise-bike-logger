import struct
import time
import asyncio

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


# TODO: Make it so it keeps trying to connect if the device can't be found.
class BluetoothSession:
    """
    Class that handles all bluetooth connectivity for a workout session including, connecting the the exercise bike,
    configuring the workout session and reading data from the exercise bike once the session has started.

    One BluetoothSession object represents one workout session.
    """

    def __init__(self, characteristic_uuid, address, filename, program, display_updater):
        """
        Method called when the Bluetooth object is initialized.

        :param characteristic_uuid: The characteristic that should be written to.
        :param address: The MAC address of the device that we want to connect with.
        :param program: The workout program containing the level, duration and level changes of the workout.
        :param filename: The CSV file in which the data should be saved.
        :param display_updater: The function that updates the display widgets on the live workout page. This is called
        every time the data from a READ write response is processed.
        """
        self.characteristic_uuid = characteristic_uuid
        self.address = address
        self.program = program
        self.filename = filename
        self.display_updater = display_updater

        # Flag that is set to True when the workout session is complete.
        self.stop_flag = False

        self.client = None
        self.current_minute = 0
        self.current_level = self.program.level

    async def run_session(self):
        """
        Connecting to the device that is associated with the given MAC address, configuring the resistance level of the
        workout, starting the workout session and reading data from the bike every second until it is finished.
        """
        try:
            loop = asyncio.get_event_loop()
            async with bleak.BleakClient(self.address, loop=loop) as self.client:
                await self.initialize_session()

                await self.set_level(self.program.level)
                time.sleep(0.5)

                # Starting the workout session.
                await self.client.write_gatt_char(self.characteristic_uuid, START)
                time.sleep(0.5)

                while not self.stop_flag:
                    # Reading the current data from the exercise bike.
                    await self.client.write_gatt_char(self.characteristic_uuid, READ)

                    # Stopping the session if the session is out of time.
                    if self.current_minute == self.program.duration:
                        self.stop_flag = True

                    # Changing the resistance level if the chosen workout program specifies it.
                    if self.current_minute < self.program.duration:
                        new_level = self.program.y_coordinates[self.current_minute]
                        if self.current_level != new_level:
                            await self.set_level(new_level)
                            self.current_level = new_level

                    time.sleep(1)

                await self.stop_session()
        except bleak.BleakError as e:
            print(f"Bleak raised an exception: {e}")

    async def initialize_session(self):
        """Running the specific initialization protocol used to connect to the exercise bike."""
        # Activating notifications on the characteristic that is written to.
        await self.client.start_notify(self.characteristic_uuid, self.notification_handler)

        await self.client.write_gatt_char(self.characteristic_uuid, PING)

        await self.client.write_gatt_char(self.characteristic_uuid, INIT_A0)

        for i in range(5):
            await self.client.write_gatt_char(self.characteristic_uuid, PING)

        await self.client.write_gatt_char(self.characteristic_uuid, INIT_A3)

        await self.client.write_gatt_char(self.characteristic_uuid, INIT_A4)

    async def set_level(self, level):
        """Setting the resistance level for the workout session."""
        lvl = struct.pack('BBBBBB', 0xf0, 0xa6, 0x01, 0x01, level + 1, (0xf0 + 0xa6 + 3 + level) & 0xFF)
        await self.client.write_gatt_char(self.characteristic_uuid, lvl)

    async def stop_session(self):
        """Closing the bluetooth connect and running the data postprocessing."""
        # Stopping the session on the bike itself and deactivating notifications on the characteristic.
        await self.client.write_gatt_char(self.characteristic_uuid, STOP)
        await self.client.stop_notify(self.characteristic_uuid)

        # Processing the entire workout session to extract further data.
        data_processing.process_workout_session(self.filename)

    def notification_handler(self, sender, data):
        """Handling the notifications that are received from a characteristic."""
        # If the data has a length of 21 we know it is a response from the READ write operation.
        if len(data) == 21:
            data = struct.unpack('BBBBBBBBBBBBBBBBBBBBB', data)

            # Extracting the current time in minutes from the data so it can be used to run certain checks.
            self.current_minute = ((data[3] - 1) * 60) + (data[4] - 1)

            # Processing the data into a readable format, saving it to the given file and updating the live displays.
            data_processing.process_read_response(data, self.filename, self.display_updater)
