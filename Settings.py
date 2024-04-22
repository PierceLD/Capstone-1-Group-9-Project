from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Database import *
from music import AudioPlayer
import random

class SettingsScreen(QWidget):
    def __init__(self, game_screen, audioPlayer):
        super().__init__()
        uic.loadUi("ui/settings.ui", self)

        self.game = game_screen
        self.audioPlayer = audioPlayer
        
        self.masterVolumeSlider.valueChanged.connect(self.adjustMasterVolume)
        self.soundEffectsSlider.valueChanged.connect(self.adjustSoundEffectsVolume)
        self.musicVolumeSlider.valueChanged.connect(self.adjustMusicVolume)

        self.masterVolumeSlider.setValue(self.masterVolumeSlider.maximum())
        self.soundEffectsSlider.setValue(self.soundEffectsSlider.maximum())
        self.musicVolumeSlider.setValue(self.musicVolumeSlider.maximum())

        self.applyChangesButton.clicked.connect(self.updateSettings)

    def load(self):
        # set the default of each combo box to already selected mappings
        #self.sets = self.game.set_names
        self.sets = getAllSetNames()
        self.redComboBox.clear()
        self.redComboBox.addItems(self.sets)
        choice = self.game.red_set
        if self.game.red_set not in self.sets:
            choice = random.choice(self.sets)
        self.redComboBox.setCurrentIndex(self.sets.index(choice)) # set default value to current set-color mapping
        self.blueComboBox.clear()
        self.blueComboBox.addItems(self.sets)
        choice = self.game.blue_set
        if choice not in self.sets:
            choice = random.choice(self.sets)
        self.blueComboBox.setCurrentIndex(self.sets.index(choice))
        self.greenComboBox.clear()
        self.greenComboBox.addItems(self.sets)
        choice = self.game.green_set
        if choice not in self.sets:
            choice = random.choice(self.sets)
        self.greenComboBox.setCurrentIndex(self.sets.index(choice))
        self.yellowComboBox.clear()
        self.yellowComboBox.addItems(self.sets)
        choice = self.game.yellow_set
        if choice not in self.sets:
            choice = random.choice(self.sets)
        self.yellowComboBox.setCurrentIndex(self.sets.index(choice))


    def adjustMasterVolume(self, value):
        self.game.audioPlayer.setMasterVolume(value)

    def adjustSoundEffectsVolume(self, value):
        self.game.audioPlayer.setEffectVolume(value)

    def adjustMusicVolume(self, value):
        self.game.audioPlayer.setMusicVolume(value)


    def updateSettings(self):
        # update the Game Screen object with new set mappings
        self.game.red_set = self.redComboBox.currentText()
        self.game.blue_set = self.blueComboBox.currentText()
        self.game.green_set = self.greenComboBox.currentText()
        self.game.yellow_set = self.yellowComboBox.currentText()

        self.game.audioPlayer.setMasterVolume(self.masterVolumeSlider.value())
        self.game.audioPlayer.setEffectVolume(self.soundEffectsSlider.value())
        self.game.audioPlayer.setMusicVolume(self.musicVolumeSlider.value())

        dialog = QDialog()
        dialog.setWindowTitle("Game Over")

        layout = QVBoxLayout()

        label = QLabel("Changes saved.")
        layout.addWidget(label)

        self.audioPlayer.stopMusic()
        self.audioPlayer.changeAndPlayMusic('sound/main.mp3')
        self.audioPlayer.setVolumeM(0.5)

        dialog.setLayout(layout)
        dialog.setModal(True)
        dialog.exec()
