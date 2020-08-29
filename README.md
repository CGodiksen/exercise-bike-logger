# Exercise bike assistant
Desktop application for iConsole compatible exercise bikes, created using PyQT. Connects with the exercise bike through Bluetooth and lets the user start a new workout and see live data while the workout is ongoing. When a workout is finished it is automatically logged and added to the workout history, which shows every workout session completed through the application. Statistics related to the workout history as a whole can also be seen to give a more comprehensive look at the progression of the users workouts.

## Design
The project is designed using an object-oriented approach where program execution starts from the **main.py** file. The main UI is implemented in the **resources/mainwindow.ui** file and UI functionality related to the main window is implemented in the **main_window.py** file. The latter connects all elements of the main window UI with their corresponding functions. This design pattern of having a python file for each UI file is used for each window in the UI. This includes the aforementioned main window, the settings dialog window, the dialog window used to configure a new workout and the window showing live data during a workout. Note that the multiple tabs in the main window are implemented using a python file for each tab.

The workout history tab is built around a list of every workout completed through the application. This list is implemented in the **workout_list_model.py** file. Note that this class inherits from **QAbstractListModel** which means that we can use it directly as the internal model for the QListView that is used in the UI. The most interesting element of the statistics tab is the interactive matplotlib graph that shows yearly, monthly and daily totals. To use a matplotlib graph in a QT UI, it is necessary to define a custom widget which supports matplotlib, which is done in the **mplwidget.py** file. 

When the "New workout" button is clicked the user is prompted to configure the time, resistance level and program of the workout. The individual workout programs are implemented in the **workout_program.py** file. When the "Start workout" button on the live workout page is clicked, a bluetooth session instance, defined in **bluetooth_session.py**, is created. This instance is responsible for connecting to the bike and continuously gathering data from the bike throughout the session. The workout session itself is represented by a WorkoutSession instance implemented in the **workout_session.py** file. This instance is responsible for saving the data while the workout in ongoing, processing the data after the workout and saving the processed data to a json file.

## Requirements
A conventional requirements file is included which means that all dependencies can be installed by navigating to the project directory and typing the following in your cmd:
```
$ pip install -r requirements.txt
```
