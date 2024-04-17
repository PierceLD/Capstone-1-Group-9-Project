from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Database import *
import random

class SettingsScreen(QWidget):
    def __init__(self, game_screen):
        super().__init__()
        uic.loadUi("ui/settings.ui", self)

        self.game = game_screen

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

    def updateSettings(self):
        # update the Game Screen object with new set mappings
        self.game.red_set = self.redComboBox.currentText()
        self.game.blue_set = self.blueComboBox.currentText()
        self.game.green_set = self.greenComboBox.currentText()
        self.game.yellow_set = self.yellowComboBox.currentText()

        dialog = QDialog()
        dialog.setWindowTitle("Game Over")

        layout = QVBoxLayout()

        label = QLabel("Changes saved.")
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.setModal(True)
        dialog.exec()
