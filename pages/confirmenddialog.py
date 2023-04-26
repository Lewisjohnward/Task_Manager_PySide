from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType

Form, Base = loadUiType("./ui/confirmenddialog.ui")

class ConfirmEndProcessDialog(Base, Form):
    def __init__(self, process):
        super().__init__()
        self.process = process
        print(dir(self.process))
        print(self.process.pid)
        self.setupUi(self)
        self.resize(300, 200)
        self.bold_warning_message.setText(f"Are you sure you want to end the selected process: \"{self.process.name()}\" (PID: {self.process.pid})?")

        self.warning_message.setText("Ending a process may destroy data, break the session or introduce a security risk. Only unreponsive processes should be ended.")
        self.pixmap = QPixmap("./icons/warning.png")
        self.warning_icon.setPixmap(self.pixmap.scaled(75, 75, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.connect_btns()
        style = open("./styles.qss").read()
        self.setStyleSheet(style)
        self.exec()

    def connect_btns(self):
        self.cancel.clicked.connect(self.handle_cancel)
        self.end_process.clicked.connect(self.handle_end_process)

    def handle_end_process(self):
        print("ending process")


    def handle_cancel(self):
        print("cancelled")
        self.close()

        
