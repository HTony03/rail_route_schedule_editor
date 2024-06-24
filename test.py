if __name__ == "__main__":
    pass

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtUiTools import QUiLoader

mylist = [
    {'train': 'C117|C117', 'type': 'COMMUTER', 'speedmax': '120',
     'composition': 'LPPPPL', 'flags': 'X1', 'stops':
         [{'stationcode': 'a', 'stationname': '新建车站 1',
           'stoptrack': 2, 'arrivetime': '08:06:00', 'stoptime': 1},
          {'stationcode': 'b', 'stationname': '新建车站 2',
           'stoptrack': 2, 'arrivetime': '08:09:00', 'stoptime': 1}]},
    {'train': 'C126|C126', 'type': 'COMMUTER', 'speedmax': '120',
     'composition': 'LPPPPL', 'flags': 'X0', 'stops':
         [{'stationcode': 'b', 'stationname': '新建车站 2',
           'stoptrack': 1, 'arrivetime': '08:04:00', 'stoptime': 1},
          {'stationcode': 'a', 'stationname': '新建车站 1',
           'stoptrack': 1, 'arrivetime': '08:07:00', 'stoptime': 1}]},
    {'train': 'C125|C125', 'type': 'COMMUTER', 'speedmax': '120',
     'composition': 'LPPPPL', 'flags': 'X0', 'stops':
         [{'stationcode': 'b', 'stationname': '新建车站 2',
           'stoptrack': 1, 'arrivetime': '08:02:00', 'stoptime': 1},
          {'stationcode': 'a', 'stationname': '新建车站 1',
           'stoptrack': 1, 'arrivetime': '08:05:00', 'stoptime': 1}]},
    {'train': 'C124|C124', 'type': 'COMMUTER', 'speedmax': '120',
     'composition': 'LPPPPL', 'flags': 'X0', 'stops':
         [{'stationcode': 'b', 'stationname': '新建车站 2',
           'stoptrack': 1, 'arrivetime': '08:00:00', 'stoptime': 1},
          {'stationcode': 'a', 'stationname': '新建车站 1',
           'stoptrack': 1, 'arrivetime': '08:03:00', 'stoptime': 1}]},
    {'train': 'C116|C116', 'type': 'COMMUTER', 'speedmax': '120',
     'composition': 'LPPPPL', 'flags': 'X0', 'stops':
         [{'stationcode': 'a', 'stationname': '新建车站 1',
           'stoptrack': 2, 'arrivetime': '08:04:00', 'stoptime': 1},
          {'stationcode': 'b', 'stationname': '新建车站 2',
           'stoptrack': 2, 'arrivetime': '08:07:00', 'stoptime': 1}]},
    {'train': 'C115|C115', 'type': 'COMMUTER', 'speedmax': '120',
     'composition': 'LPPPPL', 'flags': 'X0', 'stops':
         [{'stationcode': 'a', 'stationname': '新建车站 1',
           'stoptrack': 2, 'arrivetime': '08:02:00', 'stoptime': 1},
          {'stationcode': 'b', 'stationname': '新建车站 2',
           'stoptrack': 2, 'arrivetime': '08:05:00', 'stoptime': 1}]},
    {'train': 'C114|C114', 'type': 'COMMUTER', 'speedmax': '120',
     'composition': 'LPPPPL', 'flags': 'X0', 'stops':
         [{'stationcode': 'a', 'stationname': '新建车站 1',
           'stoptrack': 2, 'arrivetime': '08:00:00', 'stoptime': 1},
          {'stationcode': 'b', 'stationname': '新建车站 2',
           'stoptrack': 2, 'arrivetime': '08:03:00', 'stoptime': 1}]}]


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load(r'.\test.ui', self)  # replace 'your_form.ui' with your actual .ui file name
        self.ui.setWindowTitle("Current Trains")
        self.ui.show()

        # Assuming your QTableWidget object name is 'tableWidget'
        self.ui.tableWidget.setRowCount(len(mylist))  # Set the number of rows
        self.ui.tableWidget.setColumnCount(6)  # Set the number of columns

        self.ui.tableWidget.setHorizontalHeaderLabels(['train', 'type','speedmax','composition','flags','stops'])
        # Assuming 'data' is your list of lists
        data = mylist

        for i, row in enumerate(data):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(row['train']))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row['type']))
            self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(row['speedmax']))
            self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(row['composition']))
            self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(row['flags']))
            # self.ui.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(row['stops'])))
            # Add a button in the third column for each row
            button = QtWidgets.QPushButton('Show Details')
            button.clicked.connect(
                lambda checked, row=i: self.show_details(row))  # Pass the row index to the show_details method
            self.ui.tableWidget.setCellWidget(i, 5, button)  # Set the button as the cell widget
    def show_details(self, row):
        # This slot will be called when a button is clicked
        # The row index of the clicked button is passed as an argument
        # print(f'Button in row {row} clicked!')
        # self.window_trainui = trainUi(row)
        # self.window_trainui.show()

        def __init__(row):
            station_list = mylist[row]['stops']
            loader = QUiLoader()
            ui = loader.load(r'.\smalltable.ui', self)  # Load the UI directly into this instance
            ui.setWindowTitle("Stops of train:%s"%mylist[row]['train'])

            # Assuming your QTableWidget object name is 'tableWidget'
            ui.tableWidget.setRowCount(len(station_list))  # Set the number of rows
            ui.tableWidget.setColumnCount(5)  # Set the number of columns

            ui.tableWidget.setHorizontalHeaderLabels(
                ['stationcode', 'stationname', 'stoptrack', 'arrivetime', 'stoptime'])

            for i, row in enumerate(station_list):
                ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(row['stationcode']))
                ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row['stationname']))
                ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row['stoptrack'])))
                ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(row['arrivetime']))
                ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(row['stoptime'])))
            ui.show()
        __init__(row)




app = QtWidgets.QApplication([])
app.setQuitOnLastWindowClosed(True)
window = MainUi()
app.lastWindowClosed.connect(app.quit())
app.exec()