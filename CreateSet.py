from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
from Database import *
import random

class CreateSetScreen(QWidget):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      uic.loadUi("ui/create_set.ui", self)

      self.questionCount = 1

      self.studySetsButton.clicked.connect(self.clearSet)
      self.createSetButton.clicked.connect(self.createSet)
      self.addQuestionButton.clicked.connect(self.addQuestion)
      self.removeQuestionButton.clicked.connect(self.removeQuestion)

      # Create table to be used for creation of the study set
      self.studyQuestions.setColumnCount(2)
      self.studyQuestions.setRowCount(1)
      self.studyQuestions.verticalHeader().setVisible(False)
      self.studyQuestions.horizontalHeader().setVisible(False)
      self.studyQuestions.horizontalHeader().resizeSection(0,300)
      self.studyQuestions.horizontalHeader().resizeSection(1, 498)
      self.studyQuestions.setCellWidget(0,0,QLineEdit(placeholderText="Question"))
      self.studyQuestions.setCellWidget(0,1,QLineEdit(placeholderText="Answer"))
      print("Sets:",getAllSets())
      
    def addQuestion(self):
      self.questionCount += 1
      self.studyQuestions.setRowCount(self.questionCount)
      self.studyQuestions.setCellWidget(self.questionCount - 1, 0, QLineEdit(placeholderText="Question"))
      self.studyQuestions.setCellWidget(self.questionCount - 1, 1, QLineEdit(placeholderText="Answer"))

    def removeQuestion(self):
      if self.questionCount > 0:
        self.questionCount -= 1
        self.studyQuestions.removeCellWidget(self.questionCount, 0)
        self.studyQuestions.removeCellWidget(self.questionCount, 1)
        self.studyQuestions.setRowCount(self.questionCount)

    def createSet(self):
      # Creates a study set
      questions = []
      answer_list = []
      if self.questionCount > 0 and self.SetName.text() != "" and not self.SetName.text().isspace(): 
        for i in range(self.questionCount):
          if self.studyQuestions.cellWidget(i,0).text() != "" and self.studyQuestions.cellWidget(i,1).text() != "":
            questions.append({"text": self.studyQuestions.cellWidget(i,0).text(), "options":[], "correct_option":[random.randint(0,3)]})
            answer_list.append(self.studyQuestions.cellWidget(i,1).text())

        # Fills in options list
        for i in range(len(questions)):
          while len([x for x in answer_list if x != answer_list[i]]) < 4:
            answer_list.append(" ")
          questions[i]["options"] = random.sample([x for x in answer_list if x != answer_list[i]], 3)
          questions[i]["options"].insert(questions[i]["correct_option"][0], answer_list[i])
          
        # Insert set into database
        insertStudySet(self.SetName.text(), questions)

    def clearSet(self):
      # Clears the study set
      self.studyQuestions.clear()
      self.questionCount = 0
      self.addQuestion()
      self.SetName.clear()