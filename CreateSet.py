from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import json

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
      # Writes the set to a json file if it has a name and at least one question and answer pair
      questions = []
      study_set_list = {}
      if self.questionCount > 0 and self.SetName.text() != "":
        for i in range(self.questionCount):
          if self.studyQuestions.cellWidget(i,0).text() != "" and self.studyQuestions.cellWidget(i,1).text() != "":
            questions.append({"Question": self.studyQuestions.cellWidget(i,0).text(), "Answer": self.studyQuestions.cellWidget(i,1).text()})
        study_set = {self.SetName.text(): questions}

        if len(questions) > 0:
          print(study_set)
          with open("sets.json", "r") as json_file:
            try:
              study_set_list = json.load(json_file)
            except:
              print("empty json file")
          
          if self.SetName.text() in study_set_list:
            pass # TODO: add a popup window
          else:
            study_set_list[self.SetName.text()] = questions
            with open("sets.json", "w") as json_file:
              json_file.write(json.dumps(study_set_list, indent=2))

    def clearSet(self):
      # Clears the study set
      self.studyQuestions.clear()
      self.questionCount = 0
      self.addQuestion()
      self.SetName.clear()