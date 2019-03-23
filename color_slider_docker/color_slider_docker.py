import sys
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QBrush, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QAction, QTabWidget, QLineEdit, QSpinBox, QDialogButtonBox, QToolButton, QDialog, QPlainTextEdit, QCompleter, QMenu, QPushButton
from PyQt5.Qt import Qt, pyqtSignal, pyqtSlot
import math
from krita import *

from .color_slider_line import ColorSliderLine
from .ui_color_slider_docker import UIColorSliderDocker

class Color_Slider_Docker(DockWidget):
    # Init the docker

    def __init__(self):
        super(Color_Slider_Docker, self).__init__()

        main_program = Krita.instance()
        settings = main_program.readSetting("", "ColorSliderColors",
                                             "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,1,0.8,0.4,0,"
                                            + "RGBA,U8,sRGB-elle-V2-srgbtrc.icc,0,0,0,0")

        self.default_left_color = self.qcolor_to_managedcolor(QColor.fromRgbF(0.4, 0.8, 1, 1))
        self.default_right_color = self.qcolor_to_managedcolor(QColor.fromRgbF(0, 0, 0, 1))

        # make base-widget and layout
        self.widget = QWidget()
        self.sliders = []
        self.mainLayout = QHBoxLayout()
        self.settingsButton = QPushButton('S')
        self.settingsButton.setMaximumSize(30, 30)
        self.mainLayout.addWidget(self.settingsButton)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(1)
        self.mainLayout.addLayout(self.layout)
        for line in settings.split(";"):
            colors = line.split(',')
            leftColor = self.parseColor(colors[0:7])
            rightColor = self.parseColor(colors[7:])
            widget = ColorSliderLine(leftColor, rightColor, self)
            self.sliders.append(widget)
            self.layout.addWidget(widget)
            
        self.widget.setLayout(self.mainLayout)
        self.setWindowTitle(i18n("Color Slider Docker"))
        self.setWidget(self.widget)
        [x.show() for x in self.sliders]

        self.settingsButton.clicked.connect(self.init_ui)

        #self.createActions(main_program.activeWindow())

    def settings_changed(self):
        if self.ui.line_edit is not None:
            num_sliders = int(self.ui.line_edit.text())
            if len(self.sliders) > num_sliders:
                for extra_line in self.sliders[num_sliders:]:
                    self.layout.removeWidget(extra_line)
                    extra_line.setParent(None)

                self.sliders = self.sliders[0:num_sliders]
            elif len(self.sliders) < num_sliders:
                for i in range(num_sliders - len(self.sliders)):
                    widget = ColorSliderLine(self.default_left_color, self.default_right_color, self)
                    self.sliders.append(widget)
                    self.layout.addWidget(widget)
        self.writeSettings()

    def get_color_space(self):
        if self.canvas() is not None:
            if self.canvas().view() is not None:
                canvasColor = self.canvas().view().foregroundColor()
                return ManagedColor(canvasColor.colorModel(), canvasColor.colorDepth(), canvasColor.colorProfile())
        return ManagedColor('RGBA', 'U8', 'sRGB-elle-V2-srgbtrc.icc')

    def init_ui(self):
        self.ui = UIColorSliderDocker()
        self.ui.initialize(self)
        
    def createActions(self, window):
        action = window.createAction('color_slider_docker', i18n('Color Slider Docker'))
        action.setToolTip(i18n('Choose colors from a gradient between two colors.'))
        action.triggered.connect(self.init_ui)

    def writeSettings(self):
        main_program = Krita.instance()
        setting = ';'.join(
            [self.color_to_settings(line.left) + ',' + self.color_to_settings(line.right)
             for line in self.sliders])
            
        main_program.writeSetting("", "ColorSliderColors", setting)

    def color_to_settings(self, managedcolor):
        return ','.join([managedcolor.colorModel()
                         , managedcolor.colorDepth()
                         , managedcolor.colorProfile()
        ]) + ',' + ','.join(map(str, managedcolor.components()))
        
    def parseColor(self, array):
        color = ManagedColor(array[0], array[1], array[2])
        color.setComponents([float(x) for x in array[3:]])
        return color

    def canvasChanged(self, canvas):
        pass

    def qcolor_to_managedcolor(self, qcolor):
        mc = self.get_color_space()
        mc.setComponents([qcolor.blueF(), qcolor.greenF(), qcolor.redF(), qcolor.alphaF()])
        return mc

    def managedcolor_to_qcolor(self, managedcolor):
        [b, g, r, a] = managedcolor.components()
        return QColor.fromRgbF(r, g, b, a)
        #return managedcolor.colorForCanvas(self.canvas())
    
        
    
Application.addDockWidgetFactory(DockWidgetFactory("color_slider_docker", DockWidgetFactoryBase.DockRight, Color_Slider_Docker))
