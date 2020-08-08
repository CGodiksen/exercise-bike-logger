from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib

# Ensure using PyQt5 backend.
matplotlib.use('QT5Agg')


class MplCanvas(Canvas):
    """
    Matplotlib canvas used to create figure.
    """
    def __init__(self):
        self.fig = Figure(facecolor="#31363b")
        self.ax = self.fig.add_subplot(111)
        self.fig.set_tight_layout(True)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class MplWidget(QtWidgets.QWidget):
    """
    Matplotlib widget that is used in the GUI to display a matplotlib graph.
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
