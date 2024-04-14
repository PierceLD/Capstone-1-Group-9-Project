import random
import json
from Database import *

class Question(): 
    def __init__(self, color, sets):
        super().__init__()
        self.question = []
        self.color = color
        self.sets = sets # list of the 4 set names in order of red, blue, green, yellow
        self.set_questions()
        
    def set_questions(self):
        """with open("questions.json", "r", encoding="utf-8") as file:
            try:
                all_questions = json.load(file)
                
                if self.color == "red":
                    self.question = random.choice(all_questions["Chem"])
                elif self.color == "blue":
                    self.question = random.choice(all_questions["Math"])
                elif self.color == "green":
                    self.question = random.choice(all_questions["CompSci"])
                elif self.color == "yellow":
                    self.question = random.choice(all_questions["History"])
            except:
                print("Failed to read file.")"""
        
        #all_questions = getAllSets()
        if self.color == "red":
            self.question = random.choice(getSetQuestions(self.sets[0]))
        elif self.color == "blue":
            self.question = random.choice(getSetQuestions(self.sets[1]))
        elif self.color == "green":
            self.question = random.choice(getSetQuestions(self.sets[2]))
        elif self.color == "yellow":
            self.question = random.choice(getSetQuestions(self.sets[3]))