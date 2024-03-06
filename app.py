import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from MainMenu import MainMenuScreen
from Game import GameScreen
from StudySets import StudySetsScreen
from CreateSet import CreateSetScreen
from Study import StudyScreen

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
        self.study_sets.createSetButton.clicked.connect(self.goToCreateSet) # button to go to the create set screen
        self.study_sets.studyButton.clicked.connect(self.goToStudy)

        self.create_set = CreateSetScreen()
        self.stackedWidget.addWidget(self.create_set)
        self.create_set.studySetsButton.clicked.connect(self.goToStudySets) # button to return you to study sets screen

        self.study = StudyScreen()
        self.stackedWidget.addWidget(self.study)
        self.study.studySetsButton.clicked.connect(self.goToStudySets)

    # screen switching is handled here because the QStackedWidget is a part of MainWindow
    def goToMainMenu(self):
        self.stackedWidget.setCurrentIndex(0)

    def goToGame(self):
        self.stackedWidget.setCurrentIndex(1)
        self.game.startGame()

    def goToStudySets(self):
        self.study_sets.update()
        self.stackedWidget.setCurrentIndex(2)

    def goToCreateSet(self):
        self.stackedWidget.setCurrentIndex(3)

    # Goes the the study screen while loading in relevant information
    def goToStudy(self):
        if self.study_sets.study_set_selected:
            self.study.load(self.study_sets.selected_set_name)
            self.stackedWidget.setCurrentIndex(4)
        self.study_sets.study_set_selected = False
        self.study_sets.selected_set_name = ""

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    w = MainWindow() # Create main window
    w.show() # displays the window
    app.exec() # execute the app