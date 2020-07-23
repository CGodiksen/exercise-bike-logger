from PyQt5 import QtWidgets, uic


class ConnectDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(ConnectDialog, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("resources/connectdialog.ui", self)
