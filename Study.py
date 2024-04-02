from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import json

class StudyScreen(QWidget):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      uic.loadUi("ui/study.ui", self)

      self.studySetName.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def load(self, study_set_name):
      self.studySetName.setText(study_set_name)
    
      with open("sets.json", "r") as json_file:
        try:
            self.selected_set = json.load(json_file)[study_set_name]
        except:
            print("Empty json file")

      self.all_question_answer = ""
      for item in self.selected_set:
        self.all_question_answer += "Question: " + item['Question'] + "\n"
        self.all_question_answer += "Answer: " + item['Answer'] + "\n\n"
        
      self.questionAnswer.setText(self.all_question_answer)