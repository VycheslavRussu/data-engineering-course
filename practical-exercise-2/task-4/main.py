import pickle
import json

with open('products_65.pkl', 'rb') as pickleFile:
    productsAndPrices = pickle.load(pickleFile)

with open('price_info_65.json', 'r') as jsonFile:
    productsActions = json.load(jsonFile)

for action in productsActions:
    for product in productsAndPrices:
        if action['name'] == product['name']:
            if action['method'] == 'add':
                product['price'] = product['price'] + action['param']
            elif action['method'] == 'sub':
                product['price'] = product['price'] - action['param']
            elif action['method'] == 'percent+':
                product['price'] = product['price'] + (product['price'] * action['param'])
            elif action['method'] == 'percent-':
                product['price'] = product['price'] - (product['price'] * action['param'])


with open('answer_4_var_65.pkl', 'wb') as answerFile:
    pickle.dump(productsAndPrices, answerFile)