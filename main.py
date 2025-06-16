# goal:
# I used a system once, that offered multiple choice
# one wrong answer would reset successful answers
# after 5 successful answers, the answer would register as 'learned'
# and frequency would be reduced a lot

import os
import uuid

class Question:
    """different levels of questions, that unlock after prerequisites?"""
    def __init__(self,question_text,answers=None):
        self.question_text=question_text
        if answers!=None:
            self.answers = answers
        else:
            self.answers = []
        self.q_uuid=str(uuid.uuid4())
        
class LearningSystem:
    def __init__(self):
        self.try_load_questions()
        
        self.questions = {}
        self.active_question_ids = []
        self.solved_questions = []
        # maybe I want different levels?
        
        
    def try_load_questions(self):
        myfile_list = os.listdir()
        questions_fn = "questions.csv"
        current_questions_fn = "current_questions.csv"
        solved_questions_fn = "solved_questions.csv"
        
        if questions_fn in myfile_list:
            with open(questions_fn,"r") as f:
                t=f.read()
            t=t.split("\n")
            current_id = None
            current_question = None
            for line in t:
                line=line.split(";")
                myid, questiontext, answer_text=line
                if myid != currentid:
                    if current_question!=None:
                        self.questions[current_question.q_uuid]=current_question
                    current_question = Question(question_text)
                    
                    if myid!="":
                        current_question.q_uuid = myid
                        
                    current_id = current_question.q_uuid
                    current_question.answers.append(answer_text)
                    
            
        else:
            print(f"no {questions_fn} found")
            
        if current_questions_fn in myfile_list:
            with open(current_questions_fn,"r") as f:
                t=f.read()
            lines=t.split("\n")
            for line in lines:
                self.active_question_ids.append(line)
        else:
            print(f"no {current_questions_fn} found")
       
    def main(self):
        self.question_management()
        
    def present_question(self):
        #pick a ranom question
        my_id = random.choice(self.active_question_ids)
        my_question= self.questions[my_id]
        print(my_question.question_text)
        
        answers = list(my_question.answers)
        random.shuffle(answers)
        
        correct_key=answers.index(my_question.answers[0])
        c = 0
        answer_keys=[]
        for x in answers:
            print(f"{c}): {x}")
            answer_keys.append(c)
            c += 1
        
        a = input("your answer")
        if a in answer_keys:
            if a == correct_key:
                # up the count or retire
            else:
                # reset the count
        else:
            print("invalid input")
        
    def question_management(self):
        active_keys_set = set(self.active_question_ids)
        question_keys_set = set(self.questions.keys())
        
        d = question_keys_set.difference(active_keys_set)
        
        have_questions = len(d) > 0
        need_questions = len(self.active_question_ids) < 5
        if have_questions and need_questions:
            this = random.choice(list(d))
            self.active_question_ids.append(this)
            
    def pick_questions(self):
        a = 1
        
def entry():
    L = LearningSystem()
    while True:
        L.main()
    

if __name__=="__main__":
    
