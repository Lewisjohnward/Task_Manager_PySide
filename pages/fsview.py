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
from processes import diskData
Form, Base = loadUiType("./ui/fsview.ui")

class FileSystemViewDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def paint(self, painter, option, index):
        if index.column() == 5:
            progress = int(index.data())

            progressBarOption = QStyleOptionProgressBar()
            progressBarOption.rect = option.rect
            progressBarOption.minimum = 0
            progressBarOption.maximum = 100
            progressBarOption.progress = progress
            progressBarOption.text = str(progress) + "%"
            progressBarOption.textVisible = True

            QApplication.style().drawControl(QStyle.CE_ProgressBar, progressBarOption, painter)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)
        
class FsView(Base, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.disk_data = diskData()
        self._headers = list(self.disk_data[0].keys())

        self.delegate = FileSystemViewDelegate()
        self.treeWidget.setItemDelegate(self.delegate)
        self.treeWidget.setHeaderLabels(self._headers)
        self.treeWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        for di in self.disk_data:
            self.item = QTreeWidgetItem(self.treeWidget)
            for pos, key in enumerate(di):
                self.item.setText(pos, str(di[key]))
                self.item.setSizeHint(pos, QSize(200, 30))
