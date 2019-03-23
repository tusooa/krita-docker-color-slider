'''
    Copyright (C) 2019 Tusooa Zhu <tusooa@vista.aero>
    
    This file is part of Krita-docker-color-slider.

    Krita-docker-color-slider is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Krita-docker-color-slider is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Krita-docker-color-slider.  If not, see <https://www.gnu.org/licenses/>.
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPolygon
from PyQt5.QtCore import QPoint
from krita import ManagedColor
import math

class ColorSlider(QWidget):
    default_color = ManagedColor("","","")
    def __init__(self, docker, left_color=default_color, right_color=default_color, parent=None):
        super(ColorSlider, self).__init__(parent)
        self.docker = docker
        self.left_color = left_color
        self.right_color = right_color
        self.slider_pixmap = None
        self.value_x = None
        self.cursor_fill_color = QColor.fromRgbF(1,1,1,1)
        self.cursor_outline_color = QColor.fromRgbF(0, 0, 0, 1)
        self.need_redraw = True

    def set_color(self, pos, color):
        if pos == 'left':
            if self.left_color is not color:
                self.left_color = color
                self.need_redraw = True
        else:
            if self.right_color is not color:
                self.right_color = color
                self.need_redraw = True

    def update_slider(self):
        '''
        Update the slider to a gradient between the two colors.

        The painting of the slider comes from the program Krita. The original code can be accessed
        at the following URL.
        https://github.com/KDE/krita/blob/master/plugins/dockers/advancedcolorselector/kis_shade_selector_line.cpp
        '''
        if self.need_redraw:
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
            
            self.need_redraw = False
        
        widget_painter = QPainter(self)
        self.rendered_image = self.slider_pixmap.toImage()

        widget_painter.drawImage(0, 0, self.rendered_image)
        if self.value_x is not None:
            start_x = self.value_x
            start_y = self.height()/2
            delta_x = self.height()/5
            delta_y = self.height()/5
            points = [QPoint(start_x, start_y)
                      , QPoint(start_x - delta_x, start_y + delta_y)
                      , QPoint(start_x + delta_x, start_y + delta_y)]
            widget_painter.setBrush(QBrush(self.cursor_fill_color))
            widget_painter.setPen(self.cursor_outline_color)
            widget_painter.drawPolygon(QPolygon(points))
                    
    def paintEvent(self, event):
        self.update_slider()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        x = pos.x()
        if x < 0: x = 0
        if x >= self.width(): x = self.width() - 1
        self.value_x = x
        self.update()
        
    def mouseReleaseEvent(self, event):
        pos = event.pos()
        x = pos.x()
        if x < 0: x = 0
        if x >= self.width(): x = self.width() - 1
        self.value_x = x
        y = int(self.height()/2)
        fixedPos = QPoint(x, y)
        color = self.rendered_image.pixelColor(fixedPos)
        mc = self.docker.qcolor_to_managedcolor(color)
        if self.docker.canvas() is not None:
            if self.docker.canvas().view() is not None:
                self.docker.canvas().view().setForeGroundColor(mc)
        self.update()
