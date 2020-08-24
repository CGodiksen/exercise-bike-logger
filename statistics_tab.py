import datetime


class StatisticsTab:
    def __init__(self, main_window):
        self.main_window = main_window

        # Dictionary that will contain a key-value pair for each distinct statistic. If the statistic concerns a single
        # workout the value is a tuple with the format (statistic, date of workout).
        self.statistics = {}

        if len(self.main_window.model.workouts) != 0:
            self.process_workouts()
            self.update_display()

        # When a date is clicked we go to that specific workout in the workout history.
        self.main_window.longestWorkoutDateButton.clicked.connect(self.go_to_workout)
        self.main_window.longestDistanceDateButton.clicked.connect(self.go_to_workout)
        self.main_window.mostCaloriesBurnedDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highAvgSpeedDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highAvgRPMDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highAvgHeartRateDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highAvgWattDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highSpeedDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highRPMDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highHeartRateDateButton.clicked.connect(self.go_to_workout)
        self.main_window.highWattDateButton.clicked.connect(self.go_to_workout)

        self.update_graph()

    def go_to_workout(self):
        """Retrieves the date that was clicked and goes to that specific workout in the workout history."""
        clicked_date = self.main_window.sender().text()

        # Finding the workout list model index of the workout with the clicked date.
        dates = [workout["date_time"] for workout in self.main_window.model.workouts]
        date_index = dates.index(clicked_date)

        # Changing to the tab on the main window that has the workout history and going to the specific workout.
        self.main_window.mainWindowTab.setCurrentIndex(0)
        self.main_window.workoutListView.setCurrentIndex(self.main_window.model.createIndex(date_index, 0))

    def update_display(self):
        """Updates the labels in the statistics tab."""
        self.main_window.totalWorkoutsLabel.setText(str(self.statistics["total_workouts"]))
        self.main_window.totalTimeLabel.setText(self.statistics["total_time"])
        self.main_window.totalDistanceLabel.setText(f"{self.statistics['total_distance']} km")
        self.main_window.totalCaloriesLabel.setText(str(self.statistics["total_calories"]))

        self.main_window.longestWorkoutLabel.setText(self.statistics["longest_workout"][0])
        self.main_window.longestWorkoutDateButton.setText(self.statistics["longest_workout"][1])

        self.main_window.longestDistanceLabel.setText(f"{self.statistics['longest_distance'][0]} km")
        self.main_window.longestDistanceDateButton.setText(self.statistics["longest_distance"][1])

        self.main_window.mostCaloriesBurnedLabel.setText(self.statistics["most_calories_burned"][0])
        self.main_window.mostCaloriesBurnedDateButton.setText(self.statistics["most_calories_burned"][1])

        self.main_window.highAvgSpeedLabel.setText(f"{self.statistics['highest_average_speed'][0]} km/h")
        self.main_window.highAvgSpeedDateButton.setText(self.statistics["highest_average_speed"][1])

        self.main_window.highAvgRPMLabel.setText(self.statistics["highest_average_rpm"][0])
        self.main_window.highAvgRPMDateButton.setText(self.statistics["highest_average_rpm"][1])

        self.main_window.highAvgHeartRateLabel.setText(self.statistics["highest_average_heart_rate"][0])
        self.main_window.highAvgHeartRateDateButton.setText(self.statistics["highest_average_heart_rate"][1])

        self.main_window.highAvgWattLabel.setText(self.statistics["highest_average_watt"][0])
        self.main_window.highAvgWattDateButton.setText(self.statistics["highest_average_watt"][1])

        self.main_window.highSpeedLabel.setText(f"{self.statistics['highest_speed'][0]} km/h")
        self.main_window.highSpeedDateButton.setText(self.statistics["highest_speed"][1])

        self.main_window.highRPMLabel.setText(self.statistics["highest_rpm"][0])
        self.main_window.highRPMDateButton.setText(self.statistics["highest_rpm"][1])

        self.main_window.highHeartRateLabel.setText(self.statistics["highest_heart_rate"][0])
        self.main_window.highHeartRateDateButton.setText(self.statistics["highest_heart_rate"][1])

        self.main_window.highWattLabel.setText(self.statistics["highest_watt"][0])
        self.main_window.highWattDateButton.setText(self.statistics["highest_watt"][1])

    def update_graph(self):
        """Updates the graph in the statistics tab according to the chosen combo box configuration."""
        self.main_window.statisticsGraphWidget.setBackground("#31363b")

    def process_workouts(self):
        """Processes the internal workout list model to extract the needed statistics so they can be displayed."""
        workouts = self.main_window.model.workouts

        # Calculating each statistic one by one using the data, starting with the total amount of workouts.
        self.statistics["total_workouts"] = len(workouts)

        # Getting the total time in seconds and converting it to the format "DD day(s), HH:MM:SS".
        seconds = self.main_window.timestamps_to_seconds([workout["duration"] for workout in workouts])
        self.statistics["total_time"] = str(datetime.timedelta(seconds=sum(seconds)))

        self.statistics["total_distance"] = str(round(sum([workout["total_distance"] for workout in workouts]), 1))
        self.statistics["total_calories"] = str(sum([workout["total_calories"] for workout in workouts]))

        longest_workout = workouts[seconds.index(max(seconds))]
        self.statistics["longest_workout"] = (str(longest_workout["duration"]), longest_workout["date_time"])

        self.statistics["longest_distance"] = self.get_max_value_date(workouts, "total_distance")
        self.statistics["most_calories_burned"] = self.get_max_value_date(workouts, "total_calories")
        self.statistics["highest_average_speed"] = self.get_max_value_date(workouts, "avg_speed")
        self.statistics["highest_average_rpm"] = self.get_max_value_date(workouts, "avg_rpm")
        self.statistics["highest_average_heart_rate"] = self.get_max_value_date(workouts, "avg_heart_rate")
        self.statistics["highest_average_watt"] = self.get_max_value_date(workouts, "avg_watt")
        self.statistics["highest_speed"] = self.get_max_value_date(workouts, "max_speed")
        self.statistics["highest_rpm"] = self.get_max_value_date(workouts, "max_rpm")
        self.statistics["highest_heart_rate"] = self.get_max_value_date(workouts, "max_heart_rate")
        self.statistics["highest_watt"] = self.get_max_value_date(workouts, "max_watt")

    @staticmethod
    def get_max_value_date(workouts, key):
        """
        Finds the index of the workout with the maximum value for the given key.

        :param workouts: A list of dictionaries where each dictionary represents a workout.
        :param key: The specific attribute that we search for the maximum value for.
        :return: The maximum value and the date of the workout with the maximum value.
        """
        # Extracting the specific data from each workout in the workout list model.
        key_list = [workout[key] for workout in workouts]

        max_index = key_list.index(max(key_list))

        return str(workouts[max_index][key]), workouts[max_index]["date_time"]
