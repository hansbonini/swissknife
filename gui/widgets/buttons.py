import PyQt5.QtWidgets as QTW


class SimpleButton(QTW.QWidget):
    def __init__(self, text="", callback=None, *args, **kwargs):
        super(SimpleButton, self).__init__(*args, **kwargs)
        self.button = QTW.QPushButton(text)
        self.button.clicked.connect(callback)
        layout = QTW.QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
