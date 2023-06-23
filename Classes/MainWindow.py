from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QSlider,
    QRadioButton
)

from PyQt5.QtGui import (
    QPixmap,
    QColor
)

from PIL import Image
import numpy as np
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore
from Classes.VolumeWidget import *


class MainWindow(QWidget):
    def __init__(self, vol1, vol2):
        super().__init__()

        # Create a QVBoxLayout to arrange the VolumeWidgets vertically
        main_layout = QVBoxLayout(self)

        # Create the VolumeWidget
        self.VolumneLayout = VolumeWidget(vol1, vol2)
        self.VolumneLayout1 = VolumeWidget(vol2, vol1)
        main_layout.addWidget(self.VolumneLayout)
        main_layout.addWidget(self.VolumneLayout1)
