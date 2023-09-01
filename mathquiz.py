import re
import pandas as pd

# Get the math calculation
def answer(my_str): # my_str = 'Kjærlighetsblomst - (Giftering med diamant) * Molotov'

    # Get the prices and put it in a dictionary
    prices = pd.read_excel('prices.xlsx')
    pridict = {}

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

    return result