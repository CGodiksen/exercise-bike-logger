import json
import os


class Settings:
    """
    The "Settings" class defines methods that can be used throughout the application to load and
    save the connection settings. This includes the MAC address of the connected device and the uuid of the
    characteristic that is used to gather data from the exercise bike.
    """
    def __init__(self):
        # If the settings file does not already exist then create a new empty settings file.
        if "settings.json" not in os.listdir("../resources"):
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
