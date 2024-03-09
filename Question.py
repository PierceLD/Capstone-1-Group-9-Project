import random
import json

class Question(): 
    def __init__(self, size = 7):
        super().__init__()
        self.size = size
        self.questions = []
        self.set_questions(size)
        
    def set_questions(self, size):
        with open("questions.json", "r") as file:
            try:
                all_questions = json.load(file)
                self.questions = random.sample(all_questions, size)
            except:
                print("Failed to read file.")