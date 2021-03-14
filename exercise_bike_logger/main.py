import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWinExtras import QtWin

from exercise_bike_logger.main_window import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("../resources/stationarybicycle.ico"))

    # Changing the app id so our custom window icon is shown on the toolbar.
    QtWin.setCurrentProcessExplicitAppUserModelID('exercise_bike_logger.v1.0')

    main_window = MainWindow()

    # Set stylesheet.
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
