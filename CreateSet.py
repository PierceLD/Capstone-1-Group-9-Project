from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic

class CreateSetScreen(QWidget):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      uic.loadUi("ui/create_set.ui", self)

      self.createSetButton.clicked.connect(self.createSet)
      self.addQuestionButton.clicked.connect(self.addQuestion)
      self.removeQuestionButton.clicked.connect(self.removeQuestion)

      self.questionCount = 1

      # Create table to be used for creation of the study set
      self.studyQuestions.setColumnCount(2)
      self.studyQuestions.setRowCount(1)
      self.studyQuestions.verticalHeader().setVisible(False)
      self.studyQuestions.horizontalHeader().setVisible(False)
      self.studyQuestions.horizontalHeader().resizeSection(0,300)
      self.studyQuestions.horizontalHeader().resizeSection(1, 498)

      self.studyQuestions.setCellWidget(0,0,QLineEdit(placeholderText="Question"))
      self.studyQuestions.setCellWidget(0,1,QLineEdit(placeholderText="Answer"))

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
      # This will eventually write the set to a json file
      questions = []
      if self.questionCount > 0:
        for i in range(self.questionCount):
          questions.append({"Question": self.studyQuestions.cellWidget(i,0).text(), "Answer": self.studyQuestions.cellWidget(i,1).text()})
        study_set = {self.SetName.text(): questions}
        print(study_set)
