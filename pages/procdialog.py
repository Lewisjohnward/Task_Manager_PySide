"""
    Dialog displaying more information for a process
"""

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "../utils"))
from  processes import process_info

Form, Base = loadUiType("./ui/procdialog.ui")


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self._rows = list(data.keys())

    def data(self, index, role):
        if role == Qt.DisplayRole:
            column = index.column()
            row = index.row()
            if column == 0:
                return self._rows[row].title()
            if column == 1:
                return self._data[self._rows[row]]
            #column_key = self._headers[column]
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

    def rowCount(self, index):
        return len(self._rows)

    def columnCount(self, index):
        return 2

class ProcDialog(Base, Form):
    def __init__(self, pid = None):
        super().__init__()
        self.process_pid = pid
        self.setupUi(self)
        self.connect_signals()
        self.set_style()
        p_info = process_info(self.process_pid)
        self.model = TableModel(p_info)
        self.proc_dialog_table.setModel(self.model)
        self.proc_dialog_table.setColumnWidth(0, 150)
        self.close_btn.setText("x")

        p_name = p_info["name"]
        p_pid = p_info["pid"]
        self.proc_title.setText(f"{p_name} (PID {p_pid})")
        self.start_timer()
        self.exec()

    def start_timer(self):
        self.timer = QTimer.singleShot(1000, self.refresh_data)

    def refresh_data(self):
        p_info = process_info(self.process_pid)
        self.model = TableModel(p_info)
        self.proc_dialog_table.setModel(self.model)
        self.start_timer()

    def set_style(self):
        f = open("./styles.qss").read()
        self.setStyleSheet(f)

    def connect_signals(self):
        self.close_btn.clicked.connect(self.close_me)

    def close_me(self):
        self.close()

