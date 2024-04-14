from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSignal, QObject
from music import AudioPlayer

class Question_Popup(QWidget): 
    def __init__(self, question):
        super().__init__()
        self.question = question
        self.audioPlayer = AudioPlayer()
        
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
        correct = False
        for button in self.option_buttons:
            if button.isChecked():
                answer = button.text()[0]
                print("Submitted answer:", answer)
                
                if (answer == self.question["answer"]):
                    self.playerAns.emit(True)
                    correct = True
                else:
                    self.playerAns.emit(False)
                
                self.close()
                self.show_message("Correct." if correct else "Incorrect.")
                break
        else:
            print("No answer selected")
            self.playerAns.emit(False)
            self.close()
    
    dialog_closed = pyqtSignal()
    def show_message(self, msg):
        alert = QDialog()
        alert.setWindowTitle("Result")
        alert.setModal(True)

        layout = QVBoxLayout()

        label = QLabel(msg)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label)
        
        if msg == "Correct.":
            label.setStyleSheet("QLabel { color: rgb(26, 186, 29); }")
           
            self.audioPlayer.playSoundEffect('sound/correct.mp3')
        else:
            label.setStyleSheet("QLabel { color: rgb(186, 26, 26); }")
            
            self.audioPlayer.playSoundEffect('sound/wrong.mp3', .05)
            
        
        alert.setLayout(layout)

        alert.finished.connect(lambda: self.dialog_closed.emit())
        
        alert.exec()

    def show_popup(self):
        self.update_question()
        self.show()