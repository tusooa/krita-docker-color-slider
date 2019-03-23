from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QRect

from .color_slider import ColorSlider

class ColorSliderBtn(QLabel):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super(ColorSliderBtn, self).__init__(parent)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

class ColorSliderLine(QWidget):
    def __init__(self, left_color, right_color, docker, parent=None):
        super(ColorSliderLine, self).__init__(parent)
        self.left_button = ColorSliderBtn()
        self.left_button.setMaximumSize(30, 30)
        self.right_button = ColorSliderBtn()
        self.right_button.setMaximumSize(30, 30)
        self.docker = docker
        self.color_slider = ColorSlider(docker)
        self.set_color('left', left_color)
        self.set_color('right', right_color)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.left_button)
        self.layout.addWidget(self.color_slider)
        self.layout.addWidget(self.right_button)
        self.left_button.clicked.connect(self.slot_update_left_color)
        self.right_button.clicked.connect(self.slot_update_right_color)

    def set_color(self, pos, color):
        button_to_set = None
        if pos == 'left':
            self.left = color
            button_to_set = self.left_button
        else:
            self.right = color
            button_to_set = self.right_button

        self.color_slider.set_color(pos, color)
        colorSq = QPixmap(button_to_set.width(), button_to_set.height())
        colorSq.fill(color.colorForCanvas(self.docker.canvas()))
        button_to_set.setPixmap(colorSq)
        

    @pyqtSlot()
    def slot_update_left_color(self):
        if self.docker.canvas() is not None:
            if self.docker.canvas().view() is not None:
                self.set_color('left', self.docker.canvas().view().foregroundColor())
        self.color_slider.update()

    @pyqtSlot()
    def slot_update_right_color(self):
        if self.docker.canvas() is not None:
            if self.docker.canvas().view() is not None:
                self.set_color('right', self.docker.canvas().view().foregroundColor())
        self.color_slider.update()
