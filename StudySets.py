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


        self.deleteSetButton.clicked.connect(self.deleteSet)
        self.studyButton.clicked.connect(self.study)

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


        study_set_list = [x for x in os.listdir() if ".json" in x]

        # with open("sets.json", "r") as json_file:
        #     try:
        #         study_set_list = json.load(json_file)
        #     except:
        #         print("Empty json file")
        
        for study_set in study_set_list:
            self.studySets.setRowCount(self.study_set_count + 1)
            self.studySets.setItem(self.study_set_count, 0, QTableWidgetItem())
            self.studySets.item(self.study_set_count, 0).setText(study_set[:-5])
            self.study_set_count += 1
    
    # Deletes a set from the JSON file
    def deleteSet(self):
        if len(self.studySets.selectedItems()) > 0:
            set_to_remove = self.studySets.selectedItems()[0].text()
            os.remove(set_to_remove + ".json")
            removeStudySet(set_to_remove)
            self.update()

    # Checks if a set was selected to study
    def study(self):
        if len(self.studySets.selectedItems()) > 0:
            self.selected_set_name = self.studySets.selectedItems()[0].text()
            self.study_set_selected = True
