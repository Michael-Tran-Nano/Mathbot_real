import re
import pandas as pd
from openpyxl import load_workbook

# Get hats and prices
prices = pd.read_excel('prices.xlsx')

# Get the prices and put it in a dictionary
pridict = {}
for _, row in prices.iterrows():
    pridict[row['Hat'].lower()] = row['Price']

def insertprice(my_str, username):

    # Check for permission
    if str(username) not in ['smartlatios', 'illogicalpuzzle']:
        return "You do not have permission to add prices >:D"
    
    hat, price = my_str.split("=")

    # Remove white space
    hat = hat.strip()
    price = price.strip()

    # Check if hat is already in the list
    if hat.lower() in pridict:
        return f"{hat} is already in the price list"
    
    # Check if price is valid
    if not price.isnumeric():
        return f"{price} is not a valid price"
    
    # Add to Excel
    wb = load_workbook('prices.xlsx')
    ws = wb.worksheets[0] # Select First Worksheet
    ws.append([hat, price])
    wb.save('prices.xlsx')

    # Add in the current dictionary
    pridict[hat] = price

    return f"{hat} has been added to the list with the price {price}"


# Get the math calculation
def answer(my_str): # my_str = 'Kjærlighetsblomst - (Giftering med diamant) * Molotov'

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
            return f'The hat <{hat}> is not found in my price list. Please ask Kartoffel to update it. You can check all prices by using `!pricelist` (use % if you meant to ask about a quiz question)'
        else:
            math += str(pridict[hat])

            if no < nohat - 1:
                math += ope[no]

    result = eval(math)

    # Check if you have an int
    if isinstance(result, int):
        math = re.sub('\*', '\\\*' , math)
        return f'The answer is: {math} = {result}'
    else:
        return "Something went wrong :( Try again"

def pricelist():

    # Load again
    prices = pd.read_excel('prices.xlsx')

    # Fill the string with answers
    answerstring = '```\n'
    for _, row in prices.iterrows():
        answerstring += f"{row['Hat']:<25s}"
        answerstring += '='
        answerstring += f"{str(row['Price']):>7s}"
        answerstring += '\n'
    answerstring += '```' 

    return answerstring