from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import QPoint
from krita import ManagedColor
import math

class ColorSlider(QWidget):
    default_color = QColor()
    def __init__(self, docker, left_color=default_color, right_color=default_color, parent=None):
        super(ColorSlider, self).__init__(parent)
        self.docker = docker
        self.left_color = left_color
        self.right_color = right_color
        self.slider_pixmap = None

    def set_color(self, pos, color):
        if pos == 'left':
            self.left_color = color
        else:
            self.right_color = color

    def update_slider(self):
        patchCount = self.width()
        patchWidth = 1
        base_hsva = self.docker.managedcolor_to_qcolor(self.left_color).getHsvF()
        dest_hsva = self.docker.managedcolor_to_qcolor(self.right_color).getHsvF()
        diff_hsva = [(dest_hsva[i] - base_hsva[i]) for i in range(4)]
        if dest_hsva[0] == -1.0:
            diff_hsva[0] = 0
        elif diff_hsva[0] > 0.5: # make sure the sliding goes through a minor arc
            diff_hsva[0] = diff_hsva[0] - 1.0
        elif diff_hsva[0] < -0.5:
            diff_hsva[0] = diff_hsva[0] + 1.0

        step_hsva = [x/patchCount for x in diff_hsva]
            
        print('base: ', base_hsva)
        print('dest: ', dest_hsva)
        print('step: ', step_hsva)
        self.slider_pixmap = QPixmap(self.width(), self.height())
        painter = QPainter(self.slider_pixmap)
        
        for i in range(patchCount):
            hue = base_hsva[0] + i * step_hsva[0]
            while hue < 0.0: hue += 1.0
            while hue > 1.0: hue -= 1.0
            saturation = base_hsva[1] + i * step_hsva[1]
            value = base_hsva[2] + i * step_hsva[2]
            cur_color = QColor.fromHsvF(hue, saturation, value)
            painter.fillRect(i, 0, 1, self.height(), cur_color)

        painter.end()
        
        widget_painter = QPainter(self)
        self.rendered_image = self.slider_pixmap.toImage()

        widget_painter.drawImage(0, 0, self.rendered_image)
                    
    def paintEvent(self, event):
        self.update_slider()

    def mouseReleaseEvent(self, event):
        pos = event.pos()
        x = pos.x()
        if x < 0: x = 0
        if x >= self.width(): x = self.width() - 1
        y = int(self.height()/2)
        fixedPos = QPoint(x, y)
        color = self.rendered_image.pixelColor(fixedPos)
        mc = self.docker.qcolor_to_managedcolor(color)
        if self.docker.canvas() is not None:
            if self.docker.canvas().view() is not None:
                self.docker.canvas().view().setForeGroundColor(mc)
