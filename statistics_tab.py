import datetime
import calendar

from dateutil import parser
from matplotlib.text import Text


class StatisticsTab:
    def __init__(self, main_window):
        self.main_window = main_window

        # Dictionary that will contain a key-value pair for each distinct statistic. If the statistic concerns a single
        # workout the value is a tuple with the format (statistic, date of workout).
        self.statistics = {}

        # List that will contain the search keys used to specify the "layer" of the interactive graph.
        self.search_keys = []

        # Dictionary that will contain the data that is used in the interactive graph.
        self.interactive_data = self.get_interactive_graph_data(self.main_window.model.workouts, self.search_keys)

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

        # When the back button is pressed we go back a single step in the interactive graph.
        self.main_window.backButton.clicked.connect(self.back)

        # When the data combobox is changed we update the graph.
        self.main_window.dataComboBox.currentIndexChanged.connect(self.update_graph)

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
        self.main_window.statisticsGraphWidget.canvas.ax.clear()

        data_name = self.main_window.dataComboBox.currentText().lower()

        x = [str(key) for key, value in self.interactive_data.items()]
        y = [value[data_name] for key, value in self.interactive_data.items()]

        self.main_window.statisticsGraphWidget.canvas.ax.bar(x, y, picker=True)

        for label in self.main_window.statisticsGraphWidget.canvas.ax.get_xticklabels():
            label.set_picker(True)

        self.main_window.statisticsGraphWidget.canvas.fig.canvas.mpl_connect('pick_event', self.on_pick)

        self.main_window.statisticsGraphWidget.canvas.ax.set_ylabel(data_name.capitalize(), color="white", fontsize=12)

        self.main_window.statisticsGraphWidget.canvas.draw()

    def back(self):
        """Going back a single step in the interactive graph by removing a search key from the list of search keys."""
        if len(self.search_keys) > 0:
            del self.search_keys[-1]
            self.interactive_data = self.get_interactive_graph_data(self.main_window.model.workouts, self.search_keys)
            self.update_graph()

    def on_pick(self, event):
        if isinstance(event.artist, Text):
            text = event.artist
            # Ensuring that we cannot go deeper than the layer of the interactive graph that show daily totals.
            if len(self.search_keys) < 2:
                self.search_keys.append(text.get_text())
                self.interactive_data = self.get_interactive_graph_data(self.main_window.model.workouts,
                                                                        self.search_keys)
                self.update_graph()

    def process_workouts(self):
        """Processes the internal workout list model to extract the needed statistics so they can be displayed."""
        workouts = self.main_window.model.workouts

        # Calculating each statistic one by one using the data, starting with the total amount of workouts.
        self.statistics["total_workouts"] = len(workouts)

        # Getting the total time in seconds and converting it to the format "DD day(s), HH:MM:SS".
        seconds = [self.main_window.timestamp_to_seconds(workout["duration"]) for workout in workouts]
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

    def get_interactive_graph_data(self, workouts, search_keys):
        """
        Goes through the workouts and extracts the data that will be used in the interactive graph. The search keys are
        used to find the data specific to the current configuration of the interactive graph.

        :param workouts: A list of dictionaries where each dictionary represents a workout.
        :param search_keys: The list of keys used to specify the current "layer" of the interactive graph. For example,
        search_keys = [2019, 8] means that we should return the daily data for august 2019.
        :return: A dictionary where each key is a time frame and the value is the totals within that time frame.
        For example, {2018: totals_2018, 2019: totals_2019, 2020: totals_2020}.
        """
        # Reversing the list of workouts so they are to the data in chronological order.
        workouts = workouts[::-1]

        data = {}

        # If there are no search keys then we are on the year layer of the interactive graph.
        if len(search_keys) == 0:
            for workout in workouts:
                date_time = parser.parse(workout["date_time"], dayfirst=True)

                # Creating a new data dict if the key does not exist meaning that it's the first workout of the year.
                data[date_time.year] = data.get(date_time.year,
                                                {"workouts": 0, "minutes": 0, "distance": 0, "calories": 0})

                # Adding the data from the workout to the total data for this year.
                self.add_data_to_totals(workout, data, date_time.year)

        # If there is one search key then we are on the month layer of the interactive graph.
        if len(search_keys) == 1:
            # Setting up the dictionary by creating a key-value pair for each month.
            for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                          "October", "November", "December"]:
                data[month] = {"workouts": 0, "minutes": 0, "distance": 0, "calories": 0}

            # Going through the workouts and adding the data to the totals if the year matches the search key.
            for workout in workouts:
                date_time = parser.parse(workout["date_time"], dayfirst=True)

                if date_time.year == int(search_keys[0]):
                    # Adding the data from the workout to the total data for this month.
                    self.add_data_to_totals(workout, data, date_time.strftime("%B"))

        # If there are two search keys then we are one the day layer of the interactive graph.
        if len(search_keys) == 2:
            # Creating a dictionary used to convert a month string into the month number.
            month_num = {value: key for key, value in enumerate(calendar.month_name)}

            # Setting up the dictionary by creating a key-value pair for each day in the given month.
            for i in range(1, calendar.monthrange(year=int(search_keys[0]), month=month_num[search_keys[1]])[1] + 1):
                data[i] = {"workouts": 0, "minutes": 0, "distance": 0, "calories": 0}

            # Going through the workouts and adding the data to the totals if the year and month match the search keys.
            for workout in workouts:
                date_time = parser.parse(workout["date_time"], dayfirst=True)

                if date_time.year == int(search_keys[0]) and date_time.strftime("%B") == search_keys[1]:
                    # Adding the data from the workout to the total data for this day.
                    self.add_data_to_totals(workout, data, date_time.day)

        return data

    def add_data_to_totals(self, workout, dictionary, key):
        """Helper method used to add the data from the workout to the totals for the key of the dictionary."""
        dictionary[key]["workouts"] += 1
        dictionary[key]["minutes"] += self.main_window.timestamp_to_seconds(workout["duration"]) / 60
        dictionary[key]["distance"] += workout["total_distance"]
        dictionary[key]["calories"] += workout["total_calories"]
