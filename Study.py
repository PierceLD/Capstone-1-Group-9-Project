from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Database import *

class StudyScreen(QWidget):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      uic.loadUi("ui/study.ui", self)

      self.studySetName.setAlignment(Qt.AlignmentFlag.AlignCenter)
      self.showAnswers.clicked.connect(self.show_answers)
      self.answers_shown = False
    
    def load(self, study_set_name):
      self.studySetName.setText(study_set_name)

      self.selected_set = getSetQuestions(study_set_name)

      self.all_question_answer = ""
      for item in self.selected_set:
        self.all_question_answer += item['question'] + "\n\n"
        
      self.questionAnswer.setText(self.all_question_answer)
      
    def show_answers(self):
      self.all_question_answer = ""

      if self.answers_shown:
        self.load(self.studySetName.text())
        self.showAnswers.setText("Show Answers")
      else:
        for item in self.selected_set:
          self.all_question_answer += item['question'] + "\n"
          self.all_question_answer += "Answer: " + item[item['answer']] + "\n\n"
          self.showAnswers.setText("Hide Answers")
      
      self.answers_shown = not self.answers_shown
        
      self.questionAnswer.setText(self.all_question_answer)