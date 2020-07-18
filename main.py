import asyncio
import sys

from PyQt5 import QtWidgets

import bluetooth
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

    loop.run_until_complete(bluetooth.start_session(12, 5, characteristic_uuid, address, loop))
