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
      self.showanswer.clicked.connect(self.show_answer)
      self.nextQuestion.clicked.connect(self.next_question)
      self.previousQuestion.clicked.connect(self.previous_question)

      self.nextQuestion.setText(">")
      self.previousQuestion.setText("<")

      self.answer_shown = False
    
    
    def load(self, study_set_name):
      self.studySetName.setText(study_set_name)
      self.question_index = 0
      self.selected_set = getSetQuestions(study_set_name)
      
      self.answer_shown = False
      self.showanswer.setText("Show Answer")

      self.question_answer = self.selected_set[self.question_index]["question"]
        
      # Set the text to be the value of question_answer and align to center
      self.questionAnswer.setText(self.question_answer)
      self.questionAnswer.selectAll()
      self.questionAnswer.setAlignment(Qt.AlignmentFlag.AlignCenter)
      cursor = self.questionAnswer.textCursor()
      cursor.clearSelection()
      self.questionAnswer.setTextCursor(cursor)
      

    def show_answer(self):
      if self.answer_shown:
        self.question_answer = self.selected_set[self.question_index]["question"]
        self.questionAnswer.setText(self.question_answer)
        self.showanswer.setText("Show Answer")
        self.answer_shown = False
      else:
        self.question_answer = self.selected_set[self.question_index][self.selected_set[self.question_index]['answer']]
        self.showanswer.setText("Hide Answer")
        self.answer_shown = True
        
      # Set the text to be the value of question_answer and align to center
      self.questionAnswer.setText(self.question_answer)
      self.questionAnswer.selectAll()
      self.questionAnswer.setAlignment(Qt.AlignmentFlag.AlignCenter)
      cursor = self.questionAnswer.textCursor()
      cursor.clearSelection()
      self.questionAnswer.setTextCursor(cursor)


    def next_question(self):
      self.question_index = (self.question_index + 1) % len(self.selected_set)
      self.question_answer = self.selected_set[self.question_index]["question"]
      self.showanswer.setText("Show Answer")
      self.answer_shown = False

      # Set the text to be the value of question_answer and align to center
      self.questionAnswer.setText(self.question_answer)
      self.questionAnswer.selectAll()
      self.questionAnswer.setAlignment(Qt.AlignmentFlag.AlignCenter)
      cursor = self.questionAnswer.textCursor()
      cursor.clearSelection()
      self.questionAnswer.setTextCursor(cursor)


    def previous_question(self):
      self.question_index = (self.question_index - 1) % len(self.selected_set)
      self.question_answer = self.selected_set[self.question_index]["question"]
      self.showanswer.setText("Show Answer")
      self.answer_shown = False

      # Set the text to be the value of question_answer and align to center
      self.questionAnswer.setText(self.question_answer)
      self.questionAnswer.selectAll()
      self.questionAnswer.setAlignment(Qt.AlignmentFlag.AlignCenter)
      cursor = self.questionAnswer.textCursor()
      cursor.clearSelection()
      self.questionAnswer.setTextCursor(cursor)