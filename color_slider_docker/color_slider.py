from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor

class ColorSlider(QWidget):
    default_color = QColor()
    def __init__(self, docker, left_color=default_color, right_color=default_color, parent=None):
        super(ColorSlider, self).__init__(parent)
        self.docker = docker
        self.left_color = left_color
        self.right_color = right_color

    def set_color(self, pos, color):
        if pos == 'left':
            self.left_color = color
        else:
            self.right_color = color

    def update_slider(self):
        patchCount = self.width()
        patchWidth = 1
        canvas = self.docker.canvas()
        base_hsva = self.left_color.colorForCanvas(canvas).getHsvF()
        dest_hsva = self.right_color.colorForCanvas(canvas).getHsvF()
        step_hsva = [(dest_hsva[i] - base_hsva[i])/patchCount for i in range(4)]
        if dest_hsva[0] == -1.0:
            step_hsva[0] = 0
        print('base: ', base_hsva)
        print('dest: ', dest_hsva)
        print('step: ', step_hsva)
        pixmap = QPixmap(self.width(), self.height())
        painter = QPainter(pixmap)
        
        for i in range(patchCount):
            hue = base_hsva[0] + i * step_hsva[0]
            saturation = base_hsva[1] + i * step_hsva[1]
            value = base_hsva[2] + i * step_hsva[2]
            cur_color = QColor.fromHsvF(hue, saturation, value)
            painter.fillRect(i, 0, 1, self.height(), cur_color)

        painter.end()
        
        widget_painter = QPainter(self)
        rendered_image = pixmap.toImage()

        widget_painter.drawImage(0, 0, rendered_image)
                    
    def paintEvent(self, event):
        self.update_slider()
