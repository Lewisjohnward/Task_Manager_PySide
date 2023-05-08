from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType
import pyqtgraph as pg

Form, Base = loadUiType("./ui/resview.ui")

class ResView(Base, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
