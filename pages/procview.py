"""
    Process view
"""

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType

from procdialog import ProcDialog
from confirmenddialog import ConfirmEndProcessDialog
import operator
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "../utils"))
from processes import processes
Form, Base = loadUiType("./ui/procview.ui")

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self._headers = list(data[0]["details"].keys())

    def data(self, index, role):
        if role == Qt.DisplayRole:
            column = index.column()
            column_key = self._headers[column]
            if column_key == "uptime":
                value = self._data[index.row()]["details"][column_key]
                # data is given in seconds
                if value < 1:
                    return "Less than a second"
                elif value < 60:
                    return "Less than a minute"
                elif value < 3600:
                    return f"{round(value / 60)} minutes"
                elif value < (3600 * 24):
                    return f"{round(value / (3600))} hours"
                else:
                    return f"{round(value / (3600 * 24))} days"
            else:
                return self._data[index.row()]["details"][column_key]
            #if self._headers[index.column()] == "Runtime":
            #else:
            #return value
        # icons
        #if role == Qt.DecorationRole:
        #value = self._data[index.row()][index.column()]
        #if isinstance(value, bool):
        #    if value:
        #        return QtGui.QIcon('tick.png')

        #    return QtGui.QIcon('cross.png')

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self._data = sorted(self._data, key=lambda d: d["details"][self._headers[col]])
        if order == Qt.DescendingOrder:
            self._data.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._headers)

    def headerData(self, section, orientation, role):
        # row and column headers
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
        #return QVariant()

    def selected_row(self, row):
        return self._data[row]

class ProcView(Base, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.selected_process = None
        
        self.data = processes()
        self.model = TableModel(self.data)
        self.proctable.setModel(self.model)
        self.proctable.clicked.connect(self.handle_click)
        self.proctable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.end_proc_btn.clicked.connect(self.handle_terminate_proc)
        self.end_proc_btn.setDisabled(True)
        self.show_proc_properties_btn.setDisabled(True)

        self.show_proc_properties_btn.setIcon(QIcon("./icons/info.png"))
        self.show_proc_properties_btn.clicked.connect(self.display_proc_details)

    #    self.start_timer()

    #def start_timer(self):
    #    self.timer = QTimer.singleShot(1000, self.refresh_data)

    #def refresh_data(self):
    #    self.emit(SIGNAL("layoutAboutToBeChanged()"))
    #    print(self.proctable.selectionModel().currentIndex())
    #    self.data = processes()
    #    self.model = TableModel(self.data)
    #    self.proctable.setModel(self.model)
    #    print(len(self.data))
    #    print("refresh")
    #    self.emit(SIGNAL("dataChanged()"))
    #    self.emit(SIGNAL("layoutChanged()"))
    #    self.start_timer()


    def handle_click(self, item):
        row = item.row()
        self.end_proc_btn.setEnabled(True)
        self.show_proc_properties_btn.setEnabled(True)
        self.selected_process = self.model.selected_row(row)["process"]

    def handle_terminate_proc(self):
        self.dialog = ConfirmEndProcessDialog(self.selected_process)
        #self.selected_process.kill()

    def display_proc_details(self):
        self.dialog = ProcDialog(self.selected_process)
