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

      self.mode = 0
      self.questionCount = 0
      self.set_name_buffer = ""

      self.studySetsButton.clicked.connect(self.clearSet)
      self.createSetButton.clicked.connect(self.createSet)
      self.addQuestionButton.clicked.connect(self.addQuestion)
      self.removeQuestionButton.clicked.connect(self.removeQuestion)

      # Create table to be used for creation of the study set
      self.studyQuestions.setColumnCount(2)
      self.studyQuestions.verticalHeader().setVisible(False)
      self.studyQuestions.horizontalHeader().setVisible(False)
      self.studyQuestions.horizontalHeader().resizeSection(0,300)
      self.studyQuestions.horizontalHeader().resizeSection(1, 498)


    def loadCreateMode(self):
      self.mode = 0
      self.createSetButton.setText("Create Set")

      self.studyQuestions.setRowCount(1)
      self.studyQuestions.setCellWidget(0,0,QLineEdit(placeholderText="Question"))
      self.studyQuestions.setCellWidget(0,1,QLineEdit(placeholderText="Answer")) 

    def loadEditMode(self, study_set_name):
      self.studyQuestions.clear()
      self.questionCount = 0

      self.mode = 1
      self.set_name_buffer = study_set_name
      self.createSetButton.setText("Save")
      self.SetName.setText(study_set_name)
      selected_set = getSetQuestions(study_set_name)
      
      for i in range(len(selected_set)):
        self.questionCount += 1
        self.studyQuestions.setRowCount(self.questionCount)
        self.studyQuestions.setCellWidget(self.questionCount - 1,0,QLineEdit(placeholderText="Question", text=selected_set[i]["question"]))
        self.studyQuestions.setCellWidget(self.questionCount - 1,1,QLineEdit(placeholderText="Answer", text=selected_set[i][selected_set[i]["answer"]])) 
        


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
          
        if self.mode == 1:
          removeStudySet(self.set_name_buffer)
          self.set_name_buffer = self.SetName.text()

        # Insert set into database
        insertStudySet(self.SetName.text(), questions)

    def clearSet(self):
      # Clears the study set
      self.studyQuestions.clear()
      self.questionCount = 0
      self.addQuestion()
      self.SetName.clear()