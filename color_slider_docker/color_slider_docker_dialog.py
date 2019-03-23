from PyQt5.QtWidgets import QDialog

class ColorSliderDockerDialog(QDialog):
    def __init__(self, ui_color_slider, parent=None):
        super(ColorSliderDockerDialog, self).__init__(parent)

        self.ui_color_slider = ui_color_slider

    def accept(self):
        self.ui_color_slider.docker.settings_changed()

        super(ColorSliderDockerDialog, self).accept()

    def closeEvent(self, event):
        event.accept()
