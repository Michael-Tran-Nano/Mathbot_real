import re
import pandas as pd
from openpyxl import load_workbook

def pricelist():
    answerstring = '```\n'

    # Get hats and prices
    answers = pd.read_excel('prices.xlsx')

    # Fill the string with answers
    for index, row in answers.iterrows():
        answerstring += f"{row['Hat']:<25s}"
        answerstring += '='
        answerstring += f"{str(row['Price']):>7s}"
        answerstring += '\n'

    answerstring += '```'
    
    return answerstring


def insertprice(my_str):

    hat, price = my_str.split("=")

    # Remove white space
    hat = hat.strip()
    price = price.strip()

    # Get the prices and put it in a dictionary
    prices = pd.read_excel('prices.xlsx')
    pridict = {}

    # Fill the dictionary
    for index, row in prices.iterrows():
        pridict[row['Hat'].lower()] = row['Price']

    # Check if hat is already in the list
    if hat.lower() in pridict:
        return f"{hat} is already in the price list"
    
    # Check if price is valid
    if not price.isnumeric():
        return f"{price} is not a valid price"
    
    wb = load_workbook('prices.xlsx')

    # Select First Worksheet
    ws = wb.worksheets[0]

    ws.append([hat, price])
    wb.save('prices.xlsx')

    return hat, price


# Get the math calculation
def answer(my_str): # my_str = 'Kjærlighetsblomst - (Giftering med diamant) * Molotov'

    # Get the prices and put it in a dictionary
    prices = pd.read_excel('prices.xlsx')
    pridict = {}

    # Fill the dictionary
    for index, row in prices.iterrows():
        pridict[row['Hat'].lower()] = row['Price']

    # Get the individual hats and clean it
    hats = re.split('-|\+|\*', my_str)
    hats = [x.strip().lower() for x in hats]
    hats = [re.sub('\(|\)', '' , x) for x in hats]

    # Get the operators
    ope = re.sub('[^-\+\*]', '', my_str)

    # String for calculating
    nohat = len(hats)
    math = ''

    # Make the string for evaluation
    for no, hat in enumerate(hats):

        # Check if hats exist. Return that hat if it does not exist
        if hat not in pridict:
            return hat
        else:
            math += str(pridict[hat])

            if no < nohat - 1:
                math += ope[no]

    result = eval(math)

    # Give result as a tuple
    if isinstance(result, int):
        return (re.sub('\*', '\\\*' , math), result)
