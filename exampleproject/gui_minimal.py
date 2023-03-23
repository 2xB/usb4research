from PyQt6 import QtCore, QtGui, QtWidgets, uic # Importing PyQt6 before pyqtgraph so it uses the correct library
import pyqtgraph as pg

import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'main.ui'), self)
        
        self.startbutton.clicked.connect(self.startbuttonclicked)
        
    def startbuttonclicked(self):
        self.infolabel.setText("Start button clicked")

if __name__ == "__main__":
    # Start app
    app = pg.mkQApp() # QtWidgets.QApplication(["exampleapp"])
    main_window = MainWindow()
    main_window.show()
    app.exec()
