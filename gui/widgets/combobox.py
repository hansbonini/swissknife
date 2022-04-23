import PyQt5.QtWidgets as QTW

class SimpleCombobox(QTW.QWidget):
    def __init__(self, label="", list=[], *args, **kwargs):
        super(SimpleCombobox, self).__init__(*args, **kwargs)
        self.label = QTW.QLabel()
        self.label.setText(label+":")
        self.dropdown = QTW.QComboBox()
        self.dropdown.addItems(list)
        layout = QTW.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)
        self.setLayout(layout)