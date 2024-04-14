from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic

class SettingsScreen(QWidget):
    def __init__(self, game_screen):
        super().__init__()
        uic.loadUi("ui/settings.ui", self)

        self.game = game_screen

        self.applyChangesButton.clicked.connect(self.updateSettings)

    def load(self):
        # set the default of each combo box to already selected mappings
        self.sets = self.game.set_names
        self.redComboBox.clear()
        self.redComboBox.addItems(self.sets)
        self.redComboBox.setCurrentIndex(self.sets.index(self.game.red_set)) # set default value to current set-color mapping
        self.blueComboBox.clear()
        self.blueComboBox.addItems(self.sets)
        self.blueComboBox.setCurrentIndex(self.sets.index(self.game.blue_set))
        self.greenComboBox.clear()
        self.greenComboBox.addItems(self.sets)
        self.greenComboBox.setCurrentIndex(self.sets.index(self.game.green_set))
        self.yellowComboBox.clear()
        self.yellowComboBox.addItems(self.sets)
        self.yellowComboBox.setCurrentIndex(self.sets.index(self.game.yellow_set))

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
