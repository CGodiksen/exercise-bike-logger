"""
Module containing classes and methods related to the settings dialog window and the settings in general. These settings
include the MAC address of the exercise bike and the UUID of the characteristic that should be used.

The "SettingsDialog" class defines the behavior of the dialog window that is opened when the "Settings" button is
clicked on the main window. The "Settings" class defines methods that can be used throughout the application to load and
save the above mentioned settings.
"""
import json
import os

from PyQt5 import QtWidgets, uic


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

        # Load the UI Page.
        uic.loadUi("resources/settingsdialog.ui", self)

        # Loading the settings and writing them to their respective line edits.
        self.settings = Settings()
        self.addressLineEdit.setText(self.settings.address)
        self.uuidLineEdit.setText(self.settings.characteristic_uuid)

        # Saving the text in the line edits to the settings file when the user presses the "OK" button.
        self.accepted.connect(self.ok)

        # Reverting any changes if the user presses the "Cancel" button.
        self.rejected.connect(self.cancel)

    def ok(self):
        """Saving the text in the line edits to the settings file."""
        self.settings.address = self.addressLineEdit.text()
        self.settings.characteristic_uuid = self.uuidLineEdit.text()
        self.settings.save_settings()

    def cancel(self):
        """Reverting the text in the line edits back to the initial text."""
        self.addressLineEdit.setText(self.settings.address)
        self.uuidLineEdit.setText(self.settings.characteristic_uuid)


class Settings:
    def __init__(self):
        # If the settings file does not already exist then create a new empty settings file.
        if "settings.json" not in os.listdir("resources"):
            self.create_file()

        self.address = ""
        self.characteristic_uuid = ""
        self.load_settings()

    def load_settings(self):
        """Loading the current settings from the settings file."""
        with open("resources/settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            self.address = settings["address"]
            self.characteristic_uuid = settings["characteristic uuid"]

    def save_settings(self):
        """Saving the current settings to the the settings file"""
        with open("resources/settings.json", "w") as settings_file:
            json.dump({"address": self.address, "characteristic uuid": self.characteristic_uuid}, settings_file)

    @staticmethod
    def create_file():
        """Creates an empty settings file."""
        with open("resources/settings.json", "w+") as settings_file:
            json.dump({"address": "", "characteristic uuid": ""}, settings_file)
