import asyncio
import sys
import time

from PyQt5 import QtWidgets

import bluetooth_session
from main_window import MainWindow


# TODO: Make a class with functions that can read from the csv files and calculate statistics.
def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # for d in loop.run_until_complete(bluetooth.get_nearby_devices()):
    #     print(d)

    # TODO Find a way to avoid these being hardcoded.
    # The characteristic that should be written to.
    characteristic_uuid = "***REMOVED***"
    address = "***REMOVED***"

    # Using Epoch time as the filename to ensure that each workout session has an unique filename.
    bx70i = bluetooth_session.BluetoothSession(characteristic_uuid, address, loop, f"{time.time():.0f}", 13, 1800)
    loop.run_until_complete(bx70i.start_session())
