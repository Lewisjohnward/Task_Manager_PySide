from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtUiTools import loadUiType
import pyqtgraph as pg
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "./pages"))

#uiclass, baseclass = pg.Qt.loadUiType("./designer/resource_view.ui")
#
#class MainWindow(uiclass, baseclass):
#    def __init__(self):
#        super().__init__()
#        self.setupUi(self)
#
#        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
#
#    def plot(self, hour, temperature):
#        self.cpuHistoryGraph.plot(hour, temperature)

from procview import ProcView
Form, Base = loadUiType("./ui/main.ui")

#class ResView(QWidget, Ui_ResView):
#    def __init__(self):
#        super().__init__()
#        self.setupUi(self)


class MainWindow(Base, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.layout = self.centralWidget().layout()
        self.connectUi()
        self.proc_view()

        self.search_btn.setIcon(QIcon("./icons/search.png"))
        self.menu_btn.setIcon(QIcon("./icons/menu.png"))

    def connectUi(self):
        children = self.view_btns_container.findChildren(QPushButton, None, Qt.FindDirectChildrenOnly)
        for child in children:
            child.clicked.connect(self.delete_current_view)

        self.view_proc.clicked.connect(self.proc_view)
        self.view_res.clicked.connect(self.res_view)
        self.view_fs.clicked.connect(self.fs_view)
        self.view_fs.setDisabled(True)

    def delete_current_view(self):
        current_view = self.findChild(QWidget, "Form")
        current_view.deleteLater()

    def proc_view(self):
        self.procview = ProcView()
        self.layout.addWidget(self.procview)

    def res_view(self):
        self.resview = ResView()
        self.layout.addWidget(self.resview)

    def fs_view(self):
        print("fs view")


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    style = open("./styles.qss").read()
    w.setStyleSheet(style)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
