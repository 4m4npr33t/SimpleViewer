from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QWidget,
    QLabel,
    QRadioButton
)

from PyQt5.QtGui import (
    QPixmap,
    QImage,
)

from Classes.MainWindow import *

import PyQt5.QtGui as QtGui
import sys
from Common.Nifti_IO import *
from PIL import Image
from PIL.ImageQt import ImageQt

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

plt.ion()

device = 'cpu'

path_0 = '/home/amanpreet/disk1/amanpreet/scratch/UCAIR/MR_Reg/Tests/WorkingAffine/R20-091/target.nii.gz'
I0 = LoadNifti(path_0, device)

vol0 = I0.data.squeeze()
vol0 = vol0/vol0.max() * 255

path_1 = '/home/amanpreet/disk1/amanpreet/scratch/UCAIR/MR_Reg/Tests/WorkingAffine/R20-091/Affine.nii.gz'
I1 = LoadNifti(path_1, device)

vol1 = I1.data.squeeze()
vol1 = vol1/vol1.max() * 255

app = QApplication([])

window = MainWindow(vol0, vol1)

# window = QWidget()
# window.setWindowTitle("Simple Viewer")
#
# main_layout = QVBoxLayout(window)
#
# layout1 = VolumeWidget(vol0, vol1)
# main_layout.addWidget(layout1)

window.setStyleSheet("background-color:grey;")


window.show()
sys.exit(app.exec())
