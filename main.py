import sys
import breeze_resources

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream

from main_window import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)

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
