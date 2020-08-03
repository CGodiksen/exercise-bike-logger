import os
import sys
import qdarkstyle

from PyQt5 import QtWidgets

from main_window import MainWindow


def main():
    # Set the environment variable to use a specific wrapper.
    # It can be set to PyQt, PyQt5, PySide or PySide2 (not implemented yet).
    os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'

    # Import from pyqtgraph instead of doing it directly.
    # Note that PyQtGraph always uses PyQt4 API.
    from pyqtgraph.Qt import QtGui

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()

    # Setup stylesheet.
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api=os.environ['PYQTGRAPH_QT_LIB']))

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
