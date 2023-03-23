from PyQt6 import QtCore, QtGui, QtWidgets, uic # Importing PyQt6 before pyqtgraph so it uses the correct library
import pyqtgraph as pg
from datetime import datetime

#from dummydevice import Device
from remotedevice import Device

import os
import numpy as np
import signal

# Styling
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, device):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'main.ui'), self)
        
        # Variables
        self.device = device
        self.xdata = np.arange(10)
        self.y1data = np.zeros(10)
        self.y2data = np.zeros(10)
        self.starttime = None
        
        # Plots
        self.plot.showGrid(x=True,y=True,alpha=0.2)
        self.scatter1 = pg.ScatterPlotItem(size=10, brush=pg.mkBrush("#1f77b4"), pen=None)
        self.plot.addItem(self.scatter1)
        self.scatter2 = pg.ScatterPlotItem(size=12, brush=pg.mkBrush("#ff7f0e"), pen=None, symbol="x")
        self.plot.addItem(self.scatter2)
        self.updatePlot()

        # Data acquisition
        self.acquire_timer = QtCore.QTimer(self)
        self.acquire_timer.timeout.connect(self.acquire)
        self.acquire_timer.setSingleShot(True)
        
        # Interactivity
        self.startbutton.clicked.connect(self.acquire)
        self.newmeasurementbutton.clicked.connect(self.newmeasurement)
    
    def acquire(self):
        if self.starttime is None:
            # Start measurement
            self.starttime = datetime.now()
            self.startbutton.setEnabled(False)
            self.device.getData() # Omit first data since it contains old events
        
        remaining = self.duration.value() - (datetime.now() - self.starttime).total_seconds()
        self.infolabel.setText(f"Remaining: {remaining:.1f}")
        
        if remaining <= 0:
            # Stop measurement
            self.starttime = None
            self.startbutton.setEnabled(True)
            return
        
        # Acquire data
        self.y1data += self.device.getData()
        self.updatePlot()
        self.acquire_timer.start(150) # Poll after 150 ms
    
    def newmeasurement(self):
        self.y2data = self.y1data
        self.y1data = np.zeros(10)
        self.updatePlot()
    
    def updatePlot(self):
        self.scatter1.setData(self.xdata, self.y1data)
        self.scatter2.setData(self.xdata, self.y2data)
    
    
    def closeEvent(self, event):
        self.device.close()
        event.accept()
    

if __name__ == "__main__":
    # Enable quitting via Ctrl+C in command line
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # Start devices
    dev = Device()
    
    # Start app
    app = pg.mkQApp() # QtWidgets.QApplication(["exampleapp"])
    main_window = MainWindow(dev)
    main_window.show()
    app.exec()
