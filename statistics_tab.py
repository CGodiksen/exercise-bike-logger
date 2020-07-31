import csv
import datetime


class StatisticsTab:
    def __init__(self, main_window):
        self.main_window = main_window

        # Dictionary that will contain a key-value pair for each distinct statistic. If the statistic concerns a single
        # workout the value is a tuple with the format (statistic, date of workout).
        self.statistics = {}

        self.process_workouts()
        self.update_display()

    def update_display(self):
        """Updates the labels in the statistics tab."""
        self.main_window.totalWorkoutsLabel.setText(self.statistics["total_workouts"])
        self.main_window.totalTimeLabel.setText(self.statistics["total_time"])
        self.main_window.totalDistanceLabel.setText(self.statistics["total_distance"])
        self.main_window.totalCaloriesLabel.setText(self.statistics["total_calories"])

        self.main_window.longestWorkoutLabel.setText(self.statistics["longest_workout"][0])
        self.main_window.longestWorkoutDateLabel.setText(self.statistics["longest_workout"][1])

        self.main_window.longestDistanceLabel.setText(self.statistics["longest_distance"][0])
        self.main_window.longestDistanceDateLabel.setText(self.statistics["longest_distance"][1])

        self.main_window.mostCaloriesBurnedLabel.setText(self.statistics["most_calories_burned"][0])
        self.main_window.mostCaloriesBurnedDateLabel.setText(self.statistics["most_calories_burned"][1])

        self.main_window.highAvgSpeedLabel.setText(self.statistics["highest_average_speed"][0])
        self.main_window.highAvgSpeedDateLabel.setText(self.statistics["highest_average_speed"][1])

        self.main_window.highAvgRPMLabel.setText(self.statistics["highest_average_rpm"][0])
        self.main_window.highAvgRPMDateLabel.setText(self.statistics["highest_average_rpm"][1])

        self.main_window.highAvgHeartRateLabel.setText(self.statistics["highest_average_heart_rate"][0])
        self.main_window.highAvgHeartRateDateLabel.setText(self.statistics["highest_average_heart_rate"][1])

        self.main_window.highAvgWattLabel.setText(self.statistics["highest_average_watt"][0])
        self.main_window.highAvgWattDateLabel.setText(self.statistics["highest_average_watt"][1])

        self.main_window.highSpeedLabel.setText(self.statistics["highest_speed"][0])
        self.main_window.highSpeedDateLabel.setText(self.statistics["highest_speed"][1])

        self.main_window.highRPMLabel.setText(self.statistics["highest_rpm"][0])
        self.main_window.highRPMDateLabel.setText(self.statistics["highest_rpm"][1])

        self.main_window.highHeartRateLabel.setText(self.statistics["highest_heart_rate"][0])
        self.main_window.highHeartRateDateLabel.setText(self.statistics["highest_heart_rate"][1])

        self.main_window.highWattLabel.setText(self.statistics["highest_watt"][0])
        self.main_window.highWattDateLabel.setText(self.statistics["highest_watt"][1])

    def update_graph(self):
        """Updates the graph in the statistics tab according to the chosen combo box configuration."""

    def process_workouts(self):
        """Processes the workouts.csv file to extract the needed statistics so they can be displayed."""
        # Converting the data in the csv file into a dictionary with a key-value pair for each column in the file.
        with open("data/workouts.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]

        # Calculating each statistic one by one using the data, starting with the total amount of workouts.
        self.statistics["total_workouts"] = str(len(data["date"]))

        # Getting the total time in seconds and converting it to the format "DD day, HH:MM:SS".
        seconds = self.main_window.timestamps_to_seconds(data["duration"])
        self.statistics["total_time"] = str(datetime.timedelta(seconds=sum(seconds)))

        self.statistics["total_distance"] = str(sum([float(i) for i in data["distance"]]))
        self.statistics["total_calories"] = str(sum([int(i) for i in data["calories"]]))

        longest_workout_index = seconds.index(max(seconds))
        date = datetime.datetime.fromtimestamp(int(data["date"][longest_workout_index])).strftime('%d-%m-%Y %H:%M:%S')
        self.statistics["longest_workout"] = (str(data["duration"][longest_workout_index]), date)

        self.statistics["longest_distance"] = (self.get_max_value_date(data, "distance"))
        self.statistics["most_calories_burned"] = (self.get_max_value_date(data, "calories"))
        self.statistics["highest_average_speed"] = (self.get_max_value_date(data, "avg_speed"))
        self.statistics["highest_average_rpm"] = (self.get_max_value_date(data, "avg_rpm"))
        self.statistics["highest_average_heart_rate"] = (self.get_max_value_date(data, "avg_heart_rate"))
        self.statistics["highest_average_watt"] = (self.get_max_value_date(data, "avg_watt"))
        self.statistics["highest_speed"] = (self.get_max_value_date(data, "max_speed"))
        self.statistics["highest_rpm"] = (self.get_max_value_date(data, "max_rpm"))
        self.statistics["highest_heart_rate"] = (self.get_max_value_date(data, "max_heart_rate"))
        self.statistics["highest_watt"] = (self.get_max_value_date(data, "max_watt"))

    @staticmethod
    def get_max_value_date(data, key):
        """
        Finds the index of the maximum value in the list for the given key and returns the max value and the date of
        the max value.

        :param data: Dictionary with key-value pairs where each value is a list.
        :param key: Key name of the key-value pair that we want to find the max value and date for.
        """
        # Since the given dictionary contains lists of strings we convert the elements to float first.
        key_list = [float(i) for i in data[key]]

        max_index = key_list.index(max(key_list))

        date = datetime.datetime.fromtimestamp(int(data["date"][max_index])).strftime('%d-%m-%Y %H:%M:%S')
        return str(data[key][max_index]), date
