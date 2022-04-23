import PyQt5.QtWidgets as QTW

class HexadecimalTextbox(QTW.QWidget):
    def __init__(self, label="", callback=None, *args, **kwargs):
        super(HexadecimalTextbox, self).__init__(*args, **kwargs)
        self.label = QTW.QLabel()
        self.label.setText(label+":")
        self.textbox = QTW.QLineEdit()
        self.textbox.setInputMask("HHHHHHHH")
        layout = QTW.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        self.setLayout(layout)