import sys
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QBrush, QPalette
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QAction, QTabWidget, QLineEdit, QSpinBox, QDialogButtonBox, QToolButton, QDialog, QPlainTextEdit, QCompleter, QMenu
from PyQt5.Qt import Qt, pyqtSignal, pyqtSlot
import math
from krita import *

from .color_slider_line import ColorSliderLine

class Color_Slider_Docker(DockWidget):
    # Init the docker

    def __init__(self):
        super(Color_Slider_Docker, self).__init__()

        main_program = Krita.instance()
        settings = main_program.readSetting("", "ColorSliderColors",
                                             "1,0.8,0.4,0,0,0,0,0")
        
        # make base-widget and layout
        self.widget = QWidget()
        self.sliders = []
        for line in settings.split(";"):
            colors = line.split(',')
            leftColor = self.parseColor(colors[0:3])
            rightColor = self.parseColor(colors[4:7])
            self.sliders.append(ColorSliderLine(leftColor, rightColor, self))
            
        self.layout = QVBoxLayout()
        for line in self.sliders:
            self.layout.addWidget(line)
            
        self.widget.setLayout(self.layout)
        self.setWindowTitle(i18n("Color Slider Docker"))
        self.setWidget(self.widget)

    def parseColor(self, array):
        color = ManagedColor("","","")
        color.setComponents([float(x) for x in array])
        return color

    def canvasChanged(self, canvas):
        pass

    
Application.addDockWidgetFactory(DockWidgetFactory("color_slider_docker", DockWidgetFactoryBase.DockRight, Color_Slider_Docker))
