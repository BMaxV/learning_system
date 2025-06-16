# goal:
# I used a system once, that offered multiple choice
# one wrong answer would reset successful answers
# after 5 successful answers, the answer would register as 'learned'
# and frequency would be reduced a lot

import os
import uuid
import random

class Question:
    """different levels of questions, that unlock after prerequisites?"""
    def __init__(self,question_text,answers=None):
        self.question_text=question_text
        if answers!=None:
            self.answers = answers
        else:
            self.answers = []
        self.q_uuid=str(uuid.uuid4())
        self.correct_count = 0
        
class LearningSystem:
    def __init__(self):
        
        
        # maybe I want different levels?
        
        self.questions = {}
        self.active_question_ids = []
        self.solved_questions = []
        
        self.try_load_questions()
        
        
        
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
                if len(line)==1:
                    break
                myid, question_text, answer_text=line
                if myid != current_id:
                    if current_question!=None:
                        self.questions[current_question.q_uuid]=current_question
                    print(f"making {question_text}")
                    current_question = Question(question_text)
                    
                    if myid!="":
                        current_question.q_uuid = myid
                        
                    current_id = current_question.q_uuid
                current_question.answers.append(answer_text)
            
            #add the last
            self.questions[current_question.q_uuid]=current_question
            
        else:
            print(f"no {questions_fn} found")
        
        print("loaded", len(self.questions), "questions")
        
        
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
        self.present_question()
        
    def present_question(self):
        #pick a ranom question
        my_id = random.choice(self.active_question_ids)
        my_question= self.questions[my_id]
        print(my_question.question_text)
        
        answers = list(my_question.answers)
        print(answers)
        random.shuffle(answers)
        
        correct_key = str(answers.index(my_question.answers[0]))
        print("correct_key",[correct_key])
        c = 0
        answer_keys = []
        for x in answers:
            print(f"{c}): {x}")
            answer_keys.append(str(c))
            c += 1
        
        user_answer = input("your answer")
        print([user_answer])
        if user_answer in answer_keys:
            if user_answer == correct_key:
                # up the count or retire
                print("correct")
                my_question.correct_count += 1
            else:
                print("wrong")
                # reset the count
                my_question.correct_count = 0
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
        
        # I want a high frequency and a low frequency question pool
        # I want to do high frequency questions until none are left
        # 
        a = 1
        
def entry():
    L = LearningSystem()
    while True:
        L.main()
    

if __name__=="__main__":
    entry()
    
