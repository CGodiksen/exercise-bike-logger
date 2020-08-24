import datetime

from dateutil import parser
from matplotlib.patches import Rectangle
from matplotlib.text import Text


class StatisticsTab:
    def __init__(self, main_window):
        self.main_window = main_window

        # Dictionary that will contain a key-value pair for each distinct statistic. If the statistic concerns a single
        # workout the value is a tuple with the format (statistic, date of workout).
        self.statistics = {}

        # Dictionary that will contain the data that is used in the interactive graph.
        self.interactive_data = {}

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
        y = [value["data"][data_name] for key, value in self.interactive_data.items()]

        bars = self.main_window.statisticsGraphWidget.canvas.ax.bar(x, y, picker=True)
        self.label_bars(bars)

        for label in self.main_window.statisticsGraphWidget.canvas.ax.get_xticklabels():
            label.set_picker(True)

        cid = self.main_window.statisticsGraphWidget.canvas.fig.canvas.mpl_connect('pick_event', self.on_pick)

        self.main_window.statisticsGraphWidget.canvas.ax.set_ylabel(data_name.capitalize(), color="white", fontsize=12)

        self.main_window.statisticsGraphWidget.canvas.draw()

    @staticmethod
    def on_pick(event):
        if isinstance(event.artist, Rectangle):
            patch = event.artist
            print('onpick1 patch:', patch.get_path())
        elif isinstance(event.artist, Text):
            text = event.artist
            print('onpick1 text:', text.get_text())

    def label_bars(self, bars):
        """Attach a text label above each bar, displaying its height."""
        for bar in bars:
            height = bar.get_height()
            self.main_window.statisticsGraphWidget.canvas.ax.annotate('{}'.format(height),
                                                                      xy=(bar.get_x() + bar.get_width() / 2, height),
                                                                      xytext=(0, 3),  # 3 points vertical offset
                                                                      textcoords="offset points",
                                                                      ha='center', va='bottom', color="white")

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

        self.interactive_data = self.get_interactive_graph_data(workouts)

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

    def get_interactive_graph_data(self, workouts):
        """
        Creates the dictionary that is used as the data in the interactive graph on the statistics page. The dictionary
        will have multiple layers with the outermost layer containing data for each year, the layer after that
        containing data for each month in each year and the innermost layer containing data for each day in each month.

        This means the data for a workout that took place on aug 15th 2019 is contained within a august key which is
        contained within a 2019 key. The dictionary is designed this way to mirror the design of the interactive graph.

        The value for each year key on the year layer is a dict with the format {"data": data_dict, "months":
        months_dict}, the value for each month key is a dict with the format {"data": data_dict, "days": days_dict} and
        the value for each day key is just data_dict. This means that each key will have the data related to that period
        of time. For example 2019 will have how many workouts there were in 2019, the total time of those workouts,
        the total distance and the total calories. This also means that the data from aug 15th 2019 can be accessed by
        data[2019]["months"][8]["days"][15].
        """
        # Reversing the list of workouts so they are to the data in chronological order.
        workouts = workouts[::-1]
        data = {}

        previous_year = None
        previous_month = None
        previous_day = None

        for workout in workouts:
            date_time = parser.parse(workout["date_time"], dayfirst=True)

            # Creating a new entry if the entry does not exist. For example, if it is the first workout of 2020.
            if previous_year != date_time.year:
                data[date_time.year] = {"data": {"workouts": 0,
                                                 "time": 0,
                                                 "distance": 0,
                                                 "calories": 0}, "months": {}}

            # Adding the data from the workout to the total data for this year.
            year_data = data[date_time.year]["data"]
            year_data["workouts"] += 1
            year_data["time"] += self.main_window.timestamp_to_seconds(workout["duration"])
            year_data["distance"] += workout["total_distance"]
            year_data["calories"] += workout["total_calories"]

            # Creating a new entry if the entry does not exist. For example, if it is the first workout of january.
            if previous_year != date_time.year or previous_month != date_time.month:
                data[date_time.year]["months"][date_time.month] = {"data": {"workouts": 0,
                                                                            "time": 0,
                                                                            "distance": 0,
                                                                            "calories": 0}, "days": {}}

            # Adding the data from the workout to the total data for this month.
            month_data = data[date_time.year]["months"][date_time.month]["data"]
            month_data["workouts"] += 1
            month_data["time"] += self.main_window.timestamp_to_seconds(workout["duration"])
            month_data["distance"] += workout["total_distance"]
            month_data["calories"] += workout["total_calories"]

            # Creating a new entry if the entry does not exist. For example, if it is the first workout of january 1st.
            if previous_year != date_time.year or previous_month != date_time.month or previous_day != date_time.day:
                data[date_time.year]["months"][date_time.month]["days"][date_time.day] = {"workouts": 0,
                                                                                          "time": 0,
                                                                                          "distance": 0,
                                                                                          "calories": 0}

            # Adding the data from the workout to the total data for this day.
            day_data = data[date_time.year]["months"][date_time.month]["days"][date_time.day]
            day_data["workouts"] += 1
            day_data["time"] += self.main_window.timestamp_to_seconds(workout["duration"])
            day_data["distance"] += workout["total_distance"]
            day_data["calories"] += workout["total_calories"]

            previous_year = date_time.year
            previous_month = date_time.month
            previous_day = date_time.day

        return data
