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
    