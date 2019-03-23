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
from PyQt5.QtWidgets import QDialogButtonBox, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
import krita

from .color_slider_docker_dialog import ColorSliderDockerDialog

class UIColorSliderDocker(object):
    def __init__(self):
        self.kritaInstance = krita.Krita.instance()
        self.mainDialog = ColorSliderDockerDialog(self, self.kritaInstance.activeWindow().qwindow())

        self.buttonBox = QDialogButtonBox(self.mainDialog)
        self.vbox = QVBoxLayout(self.mainDialog)
        self.hbox = QHBoxLayout(self.mainDialog)
        self.line_edit = None

        self.buttonBox.accepted.connect(self.mainDialog.accept)
        self.buttonBox.rejected.connect(self.mainDialog.reject)

        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
    def initialize(self, docker):
        self.docker = docker

        self.vbox.addLayout(self.hbox)
        self.hbox.addWidget(QLabel(i18n('Number of slider lines: ')))
        self.line_edit = QLineEdit(str(len(docker.sliders)))
        self.line_edit.setValidator(QIntValidator(1, 8))
        self.hbox.addWidget(self.line_edit)

        self.vbox.addWidget(self.buttonBox)

        self.mainDialog.show()
        self.mainDialog.activateWindow()
        self.mainDialog.exec_()
        
