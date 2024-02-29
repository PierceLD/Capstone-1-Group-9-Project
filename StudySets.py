from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import json

class StudySetsScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/study_sets.ui", self)

        self.study_set_count = 0

        self.deleteSetButton.clicked.connect(self.deleteSet)

        # Create table to hold study sets
        self.studySets.setColumnCount(1)
        self.studySets.verticalHeader().setVisible(False)
        self.studySets.horizontalHeader().setVisible(False)
        self.studySets.horizontalHeader().resizeSection(0,800)
        self.studySets.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.update()

    def update(self):
        # Updates the screen with contents of the json
        study_set_list = {}
        self.study_set_count = 0
        self.studySets.clear()
        self.studySets.removeRow(0)
        with open("sets.json", "r") as json_file:
            try:
                study_set_list = json.load(json_file)
            except:
                print("Empty json file")
        
        for study_set in study_set_list:
            self.studySets.setRowCount(self.study_set_count + 1)
            self.studySets.setItem(self.study_set_count, 0, QTableWidgetItem())
            self.studySets.item(self.study_set_count, 0).setText(study_set)
            self.study_set_count += 1
    
    def deleteSet(self):
        if len(self.studySets.selectedItems()) > 0:
            set_to_remove = self.studySets.selectedItems()[0].text()
            with open("sets.json", "r") as json_file:
                try:
                    study_set_list = json.load(json_file)
                except:
                    print("Empty json file")
            del study_set_list[set_to_remove]
            with open("sets.json", "w") as json_file:
              json_file.write(json.dumps(study_set_list, indent=2))

            self.update()