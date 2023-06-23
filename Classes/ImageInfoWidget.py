from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QSlider
)

from PyQt5.QtGui import (
    QPixmap,
    QColor
)

from PIL import Image
import numpy as np
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore


class ImageInfoWidget(QWidget):
    def __init__(self, background_vol, foreground_vol, slider_max, id):
        super().__init__()
        # Create a QLabel to display the image
        self.label = QLabel(self)
        self.setMouseTracking(True)
        self.idx = id
        self.volume = background_vol
        self.volume_size = list(self.volume.shape)

        self.alpha_value = 0
        self.slider_value = 0

        self.fv = foreground_vol

        self.pixel_info_label = QLabel(self)
        self.pixel_info_label.setAlignment(QtCore.Qt.AlignCenter)

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(slider_max - 1)

        self.slider_label = QLabel("IDX: 0")
        self.slider_label.setAlignment(QtCore.Qt.AlignBottom)

        self.landmarks = []

        self.initialize()
        self.updateImage()

        # Create a QVBoxLayout to arrange the QLabel
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.pixel_info_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.slider_label)

        self.slider.valueChanged.connect(lambda value: self.updateSliderLabel(value))
        # Connect the mouseMoveEvent
        self.label.mouseMoveEvent = self.mouseMoveEventHandler

    def initialize(self):
        if self.idx == 0:
            value = int(self.volume_size[0]/2)
            self.image = self.volume[value, :, :]
        elif self.idx == 1:
            value = int(self.volume_size[1] / 2)
            self.image = self.volume[:, value, :]
        elif self.idx == 2:
            value = int(self.volume_size[2] / 2)
            self.image = self.volume[:, :, value]
        else:
            NotImplementedError

        self.slider_label.setText(f"IDX: {value}")
        self.slider_value = value
        self.slider.setValue(value)

    def updateImage(self):
        if self.alpha_value == 0:
            self.image = self.getBackgroundImage()
        else:
            i1 = self.getBackgroundImage()
            i2 = self.getForegroundImage()
            self.image = (i1.int() + self.alpha_value * (i2.int() - i1.int())).int()

        PIL_Img = Image.fromarray(np.uint8(self.image), 'L')
        self.pixmap = QPixmap.fromImage(ImageQt(PIL_Img))
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(QtCore.Qt.AlignTop)

    def getBackgroundImage(self):
        if self.idx == 0:
            temp = self.volume[self.slider_value, :, :]
        elif self.idx == 1:
            temp = self.volume[:, self.slider_value, :]
        elif self.idx == 2:
            temp = self.volume[:, :, self.slider_value]
        else:
            NotImplementedError
        return temp

    def getForegroundImage(self):
        if self.idx == 0:
            temp = self.fv[self.slider_value, :, :]
        elif self.idx == 1:
            temp = self.fv[:, self.slider_value, :]
        elif self.idx == 2:
            temp = self.fv[:, :, self.slider_value]
        else:
            NotImplementedError
        return temp

    def updateSliderLabel(self, value):
        self.slider_value = value
        self.slider_label.setText(f"IDX: {value}")
        self.updateImage()

    def mouseMoveEventHandler(self, event):
        # Get the cursor position relative to the QLabel
        pos = event.pos()

        x = pos.x()
        if x > self.pixmap.width() or x <= 0:
            x = "OUT of BOUNDS"

        y = pos.y()
        if y > self.pixmap.height() or y <= 0:
            y = "OUT of BOUNDS"

        # Display the pixel location in the window title
        self.pixel_info_label.setText(
            f"Pixel Location: ({x}, {y})"
        )

    def updateAlpha(self, value):
        self.alpha_value = value
        self.updateImage()

