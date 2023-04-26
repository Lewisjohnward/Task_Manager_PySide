from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType

Form, Base = loadUiType("./ui/procdialog.ui")

class ProcDialog(Base, Form):
    def __init__(self, process = None):
        super().__init__()
        self.setupUi(self)
        self.selected_process = process
        self.connect_signals()
        self.populate_dialog()
        self.exec()

    def connect_signals(self):
        self.close_btn.clicked.connect(self.close_me)

    def populate_dialog(self):
        name = self.selected_process.name()
        self.proc_title.setText(name)
        self.proc_dialog_table.setRowCount(1)
        self.proc_dialog_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.proc_dialog_table.horizontalHeader().hide()
        self.proc_dialog_table.setColumnCount(2)
        #self.proc_dialog_table.insertRow(1)
        item = QTableWidgetItem("My name is jeff")
        self.proc_dialog_table.setItem(0, 1, item)
        #print(self.selected_process.name())


    def close_me(self):
        self.close()

