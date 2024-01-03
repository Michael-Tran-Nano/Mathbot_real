import re
import pandas as pd
import json

# Dictionary with questions and answers
with open('vb_answers.json', encoding="utf-8") as json_file:
    answerdict = json.load(json_file)

# Get specific answers
def vb_answer(my_str):

    # Clean the quiz question
    quest = re.sub('[^a-z0-9]', '', my_str.lower())

    answer = []

    # See if you have the question, and fill possible answers
    for key, item in answerdict.items():
        if quest in re.sub('[^a-z0-9]', '', key.lower()):
            answer.append(f"{key} - {item}")
    
    # See if there is one or more possible answers
    if len(answer) == 1:
        return f'```{answer[0]}```'
    elif len(answer) > 1:
        answers =  f"```More than one question matched:\n{'¤'.join(answer)}```".replace('¤', '\n')
        if len(answers) <= 2000:
            return answers
        else:
            return "Too many possible answers found (I can use a maximum of 2000 characters). Please specifiy your question more."
    
    return r"Answer to question not found :( You can also check all the recorded answers by writing `%answers`. You can add new questions here: https://docs.google.com/spreadsheets/d/1U422_XwiOC4BKMlZrSP6BqfM3LKpeGmkc76NFZbAdZg/edit?usp=sharing"

# Make a string with all the answers
answerstring = '```\n'
for quest in answerdict.keys():
    answerstring += quest
    answerstring += ' - '
    answerstring += answerdict[quest]
    answerstring += '\n\n'

answerstring += '```'

# Get all questions and answers
def vb_answers():
    return "You can see all the answers here: https://docs.google.com/spreadsheets/d/1OEXN_p_QoSpP_UlKWqKVbC1lym7N1Ye1yh5JLn8Fbd0/edit?usp=sharing\nYou can add new questions here: https://docs.google.com/spreadsheets/d/1U422_XwiOC4BKMlZrSP6BqfM3LKpeGmkc76NFZbAdZg/edit?usp=sharing"
