from PyQt5 import QtWidgets, uic

from settings_dialog import SettingsDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi("resources/mainwindow.ui", self)

        # Connecting the buttons with their respective functionality.
        self.settings_dialog = SettingsDialog()
        self.settingsButton.clicked.connect(self.settings_dialog.show)
