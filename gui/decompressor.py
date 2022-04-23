import PyQt5.QtCore as QTC
import PyQt5.QtGui as QTG
import PyQt5.QtWidgets as QTW
from gui.common import SimpleWindow
from gui.widgets.buttons import SimpleButton
from gui.widgets.file_input import FileInput
from gui.widgets.textbox import HexadecimalTextbox
from gui.widgets.combobox import SimpleCombobox
from gui.widgets.tileviewer import SimpleTileViewer
from romhacking.tile_visualization.bpp_4_linear import *
from romhacking.tile_visualization.bpp_4_planar_composite import *
from romhacking.tile_visualization.bpp_2_planar import *
from romhacking.tile_visualization.bpp_2_planar_composite import *
from pathlib import Path


class DecompressorWindow(SimpleWindow):
    def __init__(self, app_name, decompressor_callback=None, compressor_callback=None, codec=None):
        self.callback_decompressor = decompressor_callback
        self.callback_compressor = compressor_callback
        self.selected_codec = codec
        super(DecompressorWindow, self).__init__(app_name, size=(640, 200))

    def content(self):
        self.input = FileInput("Input File", "Select File", self.select_input)
        self.output = FileInput(
            "Output File", "Select File", self.select_output)
        self.offset = HexadecimalTextbox("Offset")

        buttonDecompress = SimpleButton("Decompress", self.action_decompress)
        buttonCompress = SimpleButton("Compress", self.action_decompress)

        areaDecompressor = QTW.QVBoxLayout(self.window)
        areaDecompressorInput = QTW.QHBoxLayout()
        areaDecompressorOutput = QTW.QHBoxLayout()
        areaDecompressorOffset = QTW.QHBoxLayout()
        areaDecompressorOffsetLeft = QTW.QHBoxLayout()
        areaDecompressorOffsetLeft = QTW.QHBoxLayout()
        areaDecompressorOffsetRight = QTW.QHBoxLayout()
        areaDecompressorActions = QTW.QHBoxLayout()
        areaDecompressorActionsLeft = QTW.QHBoxLayout()
        areaDecompressorActionsCenter = QTW.QHBoxLayout()
        areaDecompressorActionsRight = QTW.QHBoxLayout()

        areaDecompressorOffsetLeft.insertStretch(2, 2)
        areaDecompressorOffsetLeft.insertStretch(2, 2)
        areaDecompressorOffsetRight.insertStretch(2, 2)
        areaDecompressorActionsLeft.insertStretch(2, 2)
        areaDecompressorActionsRight.insertStretch(2, 2)

        areaDecompressorOffset.insertLayout(0, areaDecompressorOffsetLeft)
        areaDecompressorOffset.insertLayout(1, areaDecompressorOffsetLeft)
        areaDecompressorOffset.insertLayout(2, areaDecompressorOffsetRight)
        areaDecompressorActions.insertLayout(0, areaDecompressorActionsLeft)
        areaDecompressorActions.insertLayout(1, areaDecompressorActionsCenter)
        areaDecompressorActions.insertLayout(2, areaDecompressorActionsRight)
        areaDecompressor.insertLayout(0, areaDecompressorInput)
        areaDecompressor.insertLayout(1, areaDecompressorOutput)
        areaDecompressor.insertLayout(2, areaDecompressorOffset)
        areaDecompressor.insertLayout(4, areaDecompressorActions)

        areaDecompressorInput.addWidget(self.input)
        areaDecompressorOutput.addWidget(self.output)
        areaDecompressorOffsetLeft.addWidget(self.offset)
        areaDecompressorActionsCenter.addWidget(buttonDecompress)
        areaDecompressorActionsCenter.addWidget(buttonCompress)

    def select_input(self):
        path, filter = QTW.QFileDialog.getOpenFileName(self.window, 'Select file',
                                                       '', 'All files (*)')
        if path:
            self.input.textbox.setText(path)

    def select_output(self):
        path, filter = QTW.QFileDialog.getOpenFileName(self.window, 'Select file',
                                                       '', 'All files (*)')
        if path:
            self.output.textbox.setText(path)

    def action_decompress(self):
        input = self.input.textbox.text()
        output = self.output.textbox.text()
        offset = int(self.offset.textbox.text(), 16)
        self.callback_decompressor(input, output, self.selected_codec, offset)


class MultiDecompressorWindow(SimpleWindow):
    def __init__(self, app_name, decompressor_callback=None, compressor_callback=None, codec_list=[]):
        self.callback_decompressor = decompressor_callback
        self.callback_compressor = compressor_callback
        self.codec_list = codec_list
        super(MultiDecompressorWindow, self).__init__(
            app_name, size=(640, 200))

    def content(self):

        self.input = FileInput("Input File", "Select File", self.select_input)
        self.output = FileInput(
            "Output File", "Select File", self.select_output)
        self.offset = HexadecimalTextbox("Offset")
        self.codec = SimpleCombobox("Codec", self.codec_list)

        buttonDecompress = SimpleButton("Decompress", self.action_decompress)
        buttonCompress = SimpleButton("Compress", self.action_decompress)

        areaDecompressor = QTW.QVBoxLayout(self.window)
        areaDecompressorInput = QTW.QHBoxLayout()
        areaDecompressorOutput = QTW.QHBoxLayout()
        areaDecompressorOffset = QTW.QHBoxLayout()
        areaDecompressorOffsetLeft = QTW.QHBoxLayout()
        areaDecompressorOffsetLeft = QTW.QHBoxLayout()
        areaDecompressorOffsetRight = QTW.QHBoxLayout()
        areaDecompressorCodecs = QTW.QHBoxLayout()
        areaDecompressorCodecsLeft = QTW.QHBoxLayout()
        areaDecompressorCodecsLeft = QTW.QHBoxLayout()
        areaDecompressorCodecsRight = QTW.QHBoxLayout()
        areaDecompressorActions = QTW.QHBoxLayout()
        areaDecompressorActionsLeft = QTW.QHBoxLayout()
        areaDecompressorActionsCenter = QTW.QHBoxLayout()
        areaDecompressorActionsRight = QTW.QHBoxLayout()

        areaDecompressorOffsetLeft.insertStretch(2, 2)
        areaDecompressorOffsetLeft.insertStretch(2, 2)
        areaDecompressorOffsetRight.insertStretch(2, 2)
        areaDecompressorCodecsLeft.insertStretch(2, 2)
        areaDecompressorCodecsRight.insertStretch(2, 2)
        areaDecompressorCodecsLeft.insertStretch(2, 2)
        areaDecompressorActionsLeft.insertStretch(2, 2)
        areaDecompressorActionsRight.insertStretch(2, 2)

        areaDecompressorOffset.insertLayout(0, areaDecompressorOffsetLeft)
        areaDecompressorOffset.insertLayout(1, areaDecompressorOffsetLeft)
        areaDecompressorOffset.insertLayout(2, areaDecompressorOffsetRight)
        areaDecompressorCodecs.insertLayout(0, areaDecompressorCodecsLeft)
        areaDecompressorCodecs.insertLayout(1, areaDecompressorCodecsLeft)
        areaDecompressorCodecs.insertLayout(2, areaDecompressorCodecsRight)
        areaDecompressorActions.insertLayout(0, areaDecompressorActionsLeft)
        areaDecompressorActions.insertLayout(1, areaDecompressorActionsCenter)
        areaDecompressorActions.insertLayout(2, areaDecompressorActionsRight)
        areaDecompressor.insertLayout(0, areaDecompressorInput)
        areaDecompressor.insertLayout(1, areaDecompressorOutput)
        areaDecompressor.insertLayout(2, areaDecompressorOffset)
        areaDecompressor.insertLayout(3, areaDecompressorCodecs)
        areaDecompressor.insertLayout(4, areaDecompressorActions)

        areaDecompressorInput.addWidget(self.input)
        areaDecompressorOutput.addWidget(self.output)
        areaDecompressorOffsetLeft.addWidget(self.offset)
        areaDecompressorCodecsLeft.addWidget(self.codec)
        areaDecompressorActionsCenter.addWidget(buttonDecompress)
        areaDecompressorActionsCenter.addWidget(buttonCompress)

    def select_input(self):
        path, filter = QTW.QFileDialog.getOpenFileName(self.window, 'Select file',
                                                       '', 'All files (*)')
        if path:
            self.input.textbox.setText(path)

    def select_output(self):
        path, filter = QTW.QFileDialog.getOpenFileName(self.window, 'Select file',
                                                       '', 'All files (*)')
        if path:
            self.output.textbox.setText(path)

    def action_decompress(self):
        input = self.input.textbox.text()
        output = self.output.textbox.text()
        offset = int(self.offset.textbox.text(), 16)
        codec = self.codec.dropdown.currentText()
        self.callback_decompressor(input, output, codec, offset)


class MultiDecompressorWithTileViewerWindow(SimpleWindow):
    def __init__(self, app_name, decompressor_callback=None, compressor_callback=None, codec_list=[]):
        self.callback_decompressor = decompressor_callback
        self.callback_compressor = compressor_callback
        self.codec_list = codec_list
        super(MultiDecompressorWithTileViewerWindow, self).__init__(
            app_name, size=(800, 200))

    def content(self):

        self.input = FileInput("Input File", "Select File", self.select_input)
        self.output = FileInput(
            "Output File", "Select File", self.select_output)
        self.offset = HexadecimalTextbox("Offset")
        self.codec = SimpleCombobox("Codec", self.codec_list)
        self.tileviewer = SimpleTileViewer("Preview")

        buttonDecompress = SimpleButton("Decompress", self.action_decompress)
        buttonCompress = SimpleButton("Compress", self.action_decompress)

        areaWindow = QTW.QHBoxLayout(self.window)
        areaPreview = QTW.QVBoxLayout()
        areaDecompressor = QTW.QVBoxLayout()

        areaDecompressorInput = QTW.QHBoxLayout()
        areaDecompressorOutput = QTW.QHBoxLayout()
        areaDecompressorOffset = QTW.QHBoxLayout()
        areaDecompressorOffsetLeft = QTW.QHBoxLayout()
        areaDecompressorOffsetRight = QTW.QHBoxLayout()
        areaDecompressorCodecs = QTW.QHBoxLayout()
        areaDecompressorCodecsLeft = QTW.QHBoxLayout()
        areaDecompressorCodecsRight = QTW.QHBoxLayout()
        areaDecompressorActions = QTW.QHBoxLayout()
        areaDecompressorActionsLeft = QTW.QHBoxLayout()
        areaDecompressorActionsCenter = QTW.QHBoxLayout()
        areaDecompressorActionsRight = QTW.QHBoxLayout()

        areaDecompressorOffsetRight.insertStretch(2, 2)
        areaDecompressorCodecsRight.insertStretch(2, 2)
        areaDecompressorActionsLeft.insertStretch(2, 2)
        areaDecompressorActionsRight.insertStretch(2, 2)

        areaDecompressorOffset.insertLayout(0, areaDecompressorOffsetLeft)
        areaDecompressorOffset.insertLayout(1, areaDecompressorOffsetRight)
        areaDecompressorCodecs.insertLayout(0, areaDecompressorCodecsLeft)
        areaDecompressorCodecs.insertLayout(1, areaDecompressorCodecsRight)
        areaDecompressorActions.insertLayout(0, areaDecompressorActionsLeft)
        areaDecompressorActions.insertLayout(1, areaDecompressorActionsCenter)
        areaDecompressorActions.insertLayout(2, areaDecompressorActionsRight)
        areaDecompressor.insertLayout(0, areaDecompressorInput)
        areaDecompressor.insertLayout(1, areaDecompressorOutput)
        areaDecompressor.insertLayout(2, areaDecompressorOffset)
        areaDecompressor.insertLayout(3, areaDecompressorCodecs)
        areaDecompressor.insertLayout(4, areaDecompressorActions)

        areaDecompressorInput.addWidget(self.input)
        areaDecompressorOutput.addWidget(self.output)
        areaDecompressorOffsetLeft.addWidget(self.offset)
        areaDecompressorCodecsLeft.addWidget(self.codec)
        areaDecompressorActionsCenter.addWidget(buttonDecompress)
        areaDecompressorActionsCenter.addWidget(buttonCompress)

        areaPreview.addWidget(self.tileviewer)

        areaWindow.insertLayout(0, areaDecompressor)
        areaWindow.insertLayout(1, areaPreview)

    def select_input(self):
        path, filter = QTW.QFileDialog.getOpenFileName(self.window, 'Select file',
                                                       '', 'All files (*)')
        if path:
            self.input.textbox.setText(path)

    def select_output(self):
        path, filter = QTW.QFileDialog.getOpenFileName(self.window, 'Select file',
                                                       '', 'All files (*)')
        if path:
            self.output.textbox.setText(path)

    def action_decompress(self):
        input = self.input.textbox.text()
        output = self.output.textbox.text()
        offset = int(self.offset.textbox.text(), 16)
        codec = self.codec.dropdown.currentText()
        self.callback_decompressor(input, output, codec, offset)
        self.render_preview()

    def render_preview(self):
        output = self.output.textbox.text()
        self.tileviewer.update_tiles(output, BPP2_Planar)
