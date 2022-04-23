import PyQt5.QtWidgets as QTW
import PyQt5.QtCore as QTC
from PIL import Image
import random

class SimpleTileViewer(QTW.QWidget):
    def __init__(self, label="", *args, **kwargs):
        super(SimpleTileViewer, self).__init__(*args, **kwargs)
        self.zoom = 2
        self.label_text = label
        self.image_buffer = Image.new('RGBA', (16*8, 16*8), (0, 0, 0, 255))
        self.image_buffer = self.image_buffer.resize((self.zoom*self.image_buffer.size[0], self.zoom*self.image_buffer.size[1]),0)
        self.pixmap = self.image_buffer.toqpixmap()
        self.image = QTW.QLabel()
        self.image.setPixmap(self.pixmap)
        self.label = QTW.QLabel()
        self.label.setText(self.label_text+":")
        self.palette = []
        for i in range(0,0x10):
            self.palette.append((i*15, i*15, i*15, 255))
        self.custom_layout = QTW.QVBoxLayout()
        self.custom_layout.addWidget(self.label)
        self.custom_layout.addWidget(self.image)
        self.setLayout(self.custom_layout)

    def update_tiles(self, binary=None, codec=None):
        self.clear_layout()
        self.image_buffer = Image.new('RGBA', (16*8, 16*8), (0, 0, 0, 255))
        self.image_buffer = self.image_buffer.resize((self.zoom*self.image_buffer.size[0], self.zoom*self.image_buffer.size[1]),0)
        self.pixmap = self.image_buffer.toqpixmap()
        self.image = QTW.QLabel()
        self.image.setPixmap(self.pixmap)
        self.label = QTW.QLabel()
        self.label.setText(self.label_text+":")
        if binary and codec:
            self.binary = open(binary, 'rb')
            self.tiles = codec(self.binary, self.palette, 0x0)
            self.image_buffer = self.tiles.get_buffer()
            self.image_buffer = self.image_buffer.resize((self.zoom*self.image_buffer.size[0], self.zoom*self.image_buffer.size[1]),0)
            self.pixmap = self.image_buffer.toqpixmap()
            self.image = QTW.QLabel()
            self.image.setPixmap(self.pixmap)
            self.image.setAlignment(QTC.Qt.AlignLeft | QTC.Qt.AlignTop)
            self.custom_layout.addWidget(self.label)
            self.custom_layout.addWidget(self.image)

    def clear_layout(self):
        while self.custom_layout.count():
            child = self.custom_layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())
            
            
        
