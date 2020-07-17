import asyncio
import sys
import time

from PyQt5 import QtWidgets
from main_window import MainWindow
import bluetooth


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # for d in loop.run_until_complete(bluetooth.get_nearby_devices()):
    #     print(d)

    bluetooth_connection = bluetooth.Bluetooth("***REMOVED***", loop)
    loop.run_until_complete(bluetooth_connection.start_session(12, 5))
