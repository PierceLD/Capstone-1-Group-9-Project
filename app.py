import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from MainMenu import MainMenuScreen
from Game import GameScreen
from StudySets import StudySetsScreen
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/pages.ui', self)

        self.setWindowTitle("You-Know")

        self.setFixedSize(QSize(900, 600))

        self.main_menu = MainMenuScreen()
        self.stackedWidget.addWidget(self.main_menu) # add each screen to the QStackedWidget
        self.main_menu.playButton.clicked.connect(self.goToGame) # clicking Play button takes you to game screen
        self.main_menu.studySetsButton.clicked.connect(self.goToStudySets) # clicking Study Sets button takes you to study sets screen

        self.game = GameScreen()
        self.stackedWidget.addWidget(self.game)
        self.game.mainMenuButton.clicked.connect(self.goToMainMenu) # button to return you to main menu

        self.study_sets = StudySetsScreen()
        self.stackedWidget.addWidget(self.study_sets)
        self.study_sets.mainMenuButton.clicked.connect(self.goToMainMenu) # button to return you to main menu

    # screen switching is handled here because the QStackedWidget is a part of MainWindow
    def goToMainMenu(self):
        self.stackedWidget.setCurrentIndex(0)

    def generateCards(self):
      colors = ['red', 'blue', 'green', 'yellow']
      card_info = []

      # generate random number from 0-9 and pick a random color in the 'colors' array
      for _ in range(10):
          random_number = random.randint(0, 9)
          random_color = random.choice(colors)
          
          card = {'number': random_number, 'color': random_color}
          card_info.append(card)

      card_x = 100 # current x position of card

      for ele in card_info:
        card = QPushButton(str(ele["number"]), self.game)
        card.setGeometry(QRect(card_x, 350, 100, 150))
        card.setStyleSheet(f"QPushButton {{background-color: {ele['color']}; font-size: 32px; border-radius: 10px; border: 3px solid rgb(0, 0, 0); text-align: top left; padding-left: 5px;}}")
        card.show()
        card_x += 50

    def goToGame(self, game_screen):
        self.stackedWidget.setCurrentIndex(1)
        self.generateCards()

    def goToStudySets(self):
        self.stackedWidget.setCurrentIndex(2)

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    # Create main window
    w = MainWindow()
    w.show() # displays the window
    
    app.exec() # execute the app