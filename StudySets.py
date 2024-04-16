from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import json
from Database import *
import os

class StudySetsScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/study_sets.ui", self)

        self.study_set_count = 0
        self.study_set_selected = False
        self.selected_set_name = ""

        self.uploadJSONButton.clicked.connect(self.uploadJSON)
        self.deleteSetButton.clicked.connect(self.deleteSet)
        self.studyButton.clicked.connect(self.study)
        self.editSetButton.clicked.connect(self.editSet)

        # Create table to hold study sets
        self.studySets.setColumnCount(1)
        self.studySets.verticalHeader().setVisible(False)
        self.studySets.horizontalHeader().setVisible(False)
        self.studySets.horizontalHeader().resizeSection(0,800)
        self.studySets.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.studySets.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.update()

    # Updates the studysets screen
    def update(self):
        # Updates the screen with contents of the json
        study_set_list = {}
        self.study_set_count = 0
        self.studySets.clear()
        self.studySets.removeRow(0)

        study_set_list = getAllSetNames()
        
        for study_set in study_set_list:
            self.studySets.setRowCount(self.study_set_count + 1)
            self.studySets.setItem(self.study_set_count, 0, QTableWidgetItem())
            self.studySets.item(self.study_set_count, 0).setText(study_set)
            self.study_set_count += 1
    
    # Deletes a set from the database
    def deleteSet(self):
        if len(self.studySets.selectedItems()) > 0:
            set_to_remove = self.studySets.selectedItems()[0].text()
            removeStudySet(set_to_remove)
            self.update()

    def editSet(self):
        if len(self.studySets.selectedItems()) > 0:
            self.selected_set_name = self.studySets.selectedItems()[0].text()
            self.study_set_selected = True     

    # Checks if a set was selected to study
    def study(self):
        if len(self.studySets.selectedItems()) > 0:
            self.selected_set_name = self.studySets.selectedItems()[0].text()
            self.study_set_selected = True

    # uploads json file representing a study set to the database
    def uploadJSON(self):
        #self.audioPlayer.playSoundEffect('sound/button.mp3')
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Upload JSON File", 
            "", 
            "JSON Files (*.json)"
        )
        if file_path:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                print("File uploaded successfully:", file_path)
                print("Uploaded File Name:", file_name)
                print("JSON data:", data)
            
            questions = [q for q in data["questions"] if q["type"] == "multiple_choice"]
            if file_name in getAllSetNames():
                print(f"Study set '{file_name}' already exists, rename your file or add a different file.")
            else:
                insertStudySet(file_name, questions)
                print(f"Study set '{file_name}' was successfully added.")
        self.update()