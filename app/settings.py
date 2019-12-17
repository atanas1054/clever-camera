from pathlib import Path

import remi.gui as gui
import yaml
from remi import App

from camera_widget import CameraWidget
from config import Config
from gui import CustomButton, HorizontalLine


class Settings(gui.Container):
    def __init__(self, app: App, *args):
        super(Settings, self).__init__(*args)
        self.app_instance = app
        self.saveSettings = CustomButton("Save Settings")
        self.saveSettings.set_size(300, 40)
        self.cameraWidget = CameraWidget(app)
        self.css_width = "100%"
        self.append(HorizontalLine())
        mainLayout = gui.VBox()
        buttonLayout = gui.HBox()
        buttonLayout.append(self.saveSettings)
        mainLayout.append(self.cameraWidget)
        self.append(mainLayout)
        self.append(buttonLayout)
        self.load_settings()
        # signals
        self.saveSettings.onclick.do(self.save_settings)

    def save_settings(self, emitter=None):
        camera_config = self.cameraWidget.get_settings()
        config = {"camera": camera_config}
        with Config.CONFIG_PATH.open("w") as file:
            yaml.dump(config, file)

    def load_settings(self):
        if not Config.CONFIG_PATH.exists():
            return False
        with Config.CONFIG_PATH.open("r") as file:
            config = yaml.load(file, Loader=yaml.Loader)

        self.cameraWidget.set_settings(config["camera"])
