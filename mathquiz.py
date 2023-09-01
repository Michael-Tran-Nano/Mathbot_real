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

    # Check if hats exist. Return that hat if it does not exist
    for hat in hats:
        if hat not in pridict:
            return hat

    # Calculate the result
    math = str(pridict[hats[0]]) + ope[0] + str(pridict[hats[1]]) + ope[1] + str(pridict[hats[2]]) # make something to stop it if it has too many hats, maybe use pop
    result = eval(math)

    return result