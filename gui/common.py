import sys
import os
import PyQt5.QtWidgets as QTW
import PyQt5.QtGui as QTG


class SimpleWindow:
    def __init__(self, app_name="Simple ROMHacking Tool", size=(1024, 768)):
        self.application = QTW.QApplication([app_name.lower().replace(' ','_')])
        self.window = QTW.QWidget()
        self.window.setWindowIcon(QTG.QIcon(__file__.replace('common.py','resources/default.ico')))
        self.window.resize(size[0], size[1])
        self.window.setWindowTitle(app_name)
        self.content()
        self.window.show()
        sys.exit(self.application.exec())

    def content(self):
        pass
