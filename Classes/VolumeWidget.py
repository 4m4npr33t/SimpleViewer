from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
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
from Classes.ImageInfoWidget import *


class VolumeWidget(QWidget):
    def __init__(self, background_vol, foreground_vol):
        super().__init__()

        self.bv = background_vol
        self.fv = foreground_vol

        self.image_widget_list = []

        s = self.bv.shape

        # Create a QVBoxLayout to arrange the ImageSliderWidgets vertically
        main_layout = QVBoxLayout(self)

        # Create a QHBoxLayout for the ImageSliderWidgets and the vertical slider
        layout = QHBoxLayout()
        for idx in range(0, 3):
            image_widget = ImageInfoWidget(self.bv, self.fv, s[idx], idx)
            self.image_widget_list.append(image_widget)
            layout.addWidget(image_widget)

        # Create a vertical QSlider
        self.slider = QSlider(QtCore.Qt.Vertical)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        layout.addWidget(self.slider)

        self.slider.valueChanged.connect(lambda value: self.updateAlphaLabel(value))

        # Create a QLabel for the slider label
        self.slider_label = QLabel("Alpha : 0")
        self.slider_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.slider_label)

        main_layout.addLayout(layout)


    def updateAlphaLabel(self, value):
        self.slider_label.setText(f"Alpha: {value/100}")
        for idx in range(0, 3):
            self.image_widget_list[idx].updateAlpha(value/100)

