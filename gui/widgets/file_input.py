import PyQt5.QtWidgets as QTW


class FileInput(QTW.QWidget):
    def __init__(self, label="", button="Select File", callback=None, *args, **kwargs):
        super(FileInput, self).__init__(*args, **kwargs)
        self.label = QTW.QLabel()
        self.label.setText(label+":")
        self.textbox = QTW.QLineEdit()
        self.button = QTW.QPushButton(button)
        self.button.clicked.connect(callback)
        layout = QTW.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        self.setLayout(layout)
