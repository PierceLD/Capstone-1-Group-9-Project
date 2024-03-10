from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSignal, QObject

class Question_Popup(QWidget): 
    def __init__(self, question):
        super().__init__()
        self.question = question
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Question")
        self.question_label = QLabel()
        layout.addWidget(self.question_label)

        self.radio_group = QButtonGroup()

        options_layout = QVBoxLayout()
        layout.addLayout(options_layout)

        self.option_buttons = []
        for option in ['A', 'B', 'C', 'D']:
            radio_button = QRadioButton(option)
            font = radio_button.font()
            font.setPointSize(12)
            radio_button.setFont(font)
            self.option_buttons.append(radio_button)
            options_layout.addWidget(radio_button)
            self.radio_group.addButton(radio_button)

        self.update_question()

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_answer)
        layout.addWidget(submit_button)

    def update_question(self):
        text = self.question["question"]
        font = self.question_label.font()
        font.setPointSize(12)
        font.setBold(True)
        self.question_label.setText(text)
        self.question_label.setFont(font)

        for i, option in enumerate(['A', 'B', 'C', 'D']):
            self.option_buttons[i].setText(option + ': ' + self.question[option])

    playerAns = pyqtSignal(bool)
    def submit_answer(self):
        for button in self.option_buttons:
            if button.isChecked():
                answer = button.text()[0]
                print("Submitted answer:", answer)
                
                if (answer == self.question["correct_answer"]):
                    print("correct")
                    self.playerAns.emit(True)
                else:
                    self.playerAns.emit(False)
                
                self.close()
                break
        else:
            print("No answer selected")
            self.playerAns.emit(False)

    def show_popup(self):
        self.update_question()
        self.show()