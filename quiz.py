import re
import pandas as pd

# Get questions and answers
answers = pd.read_excel('quiz.xlsx')

# Dictionary with questions and answers
answerdict = {}
for _, row in answers.iterrows():
    quest = re.sub('[^a-z0-9]', '', row['Question'].lower())
    answerdict[quest] = row['Answer']

# Get specific answers
def quizanswer(my_str):

    # Clean the quiz question
    quest = re.sub('[^a-z0-9]', '', my_str.lower())

    answer = []

    # See if you have the question, and fill possible answers
    for key, item in answerdict.items():
        if quest in key:
            answer.append(item)
    
    # See if there is one or more possible answers
    if len(answer) == 1:
        return f"The answer is: {answer[0]}", None
    elif len(answer) > 1:
        return f"Possible answers: {', '.join(answer)}", None
    
    return r"Answer to quiz not found :( Please ask Kartoffel to add it. You can also check all the answer by writing `%answers` (Use ! if you meant to send a math question instead)", None

# Make a string with all the answers
answerstring = '```\n'
for index, row in answers.iterrows():
    answerstring += row['Question']
    answerstring += ' - '
    answerstring += row['Answer']
    answerstring += '\n\n'

answerstring += '```'

# Get all questions and answers
def quizanswers():
    return answerstring, None
