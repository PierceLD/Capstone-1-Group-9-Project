import random
import json

class Question(): 
    def __init__(self, color):
        super().__init__()
        self.question = []
        self.color = color
        self.set_questions()
        
    def set_questions(self):
        with open("questions.json", "r", encoding="utf-8") as file:
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
                print("Failed to read file.")
                
        
        