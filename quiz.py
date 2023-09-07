import re
import pandas as pd

# Get specific answers
def quizanswer(my_str):

    answer = []

    # Get questions and answers
    answers = pd.read_excel('quiz.xlsx')
    answerdict = {}

    # Fill the dictionary
    for index, row in answers.iterrows():
        quest = re.sub('[^a-z0-9]', '', row['Question'].lower())
        answerdict[quest] = row['Answer']

    # Clean the quiz question
    quest = re.sub('[^a-z0-9]', '', my_str.lower())

    # See if you have the question, and fill possible answers
    for key, item in answerdict.items():
        if quest in key:
            answer.append(item)
    
    # See if there is one or more possible answers
    if len(answer) == 1:
        return answer[0]
    elif len(answer) > 1:
        return answer
    
    return None

# Get all questions and answers
def quizanswers():
    answerstring = '```\n'

    # Get questions and answers
    answers = pd.read_excel('quiz.xlsx')

    # Fill the string with answers
    for index, row in answers.iterrows():
        answerstring += row['Question']
        answerstring += ' - '
        answerstring += row['Answer']
        answerstring += '\n\n'

    answerstring += '```'
    
    return answerstring
