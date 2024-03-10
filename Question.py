import random
import json

class Question(): 
    def __init__(self):
        super().__init__()
        self.question = []
        self.set_questions()
        
    def set_questions(self):
        with open("questions.json", "r") as file:
            try:
                all_questions = json.load(file)
                self.question = random.choice(all_questions)
            except:
                print("Failed to read file.")