import json
import msgpack

with open('products_65.json', 'r') as file:
    taskJSON = json.load(file)

products = {}

for item in taskJSON:
    if item['name'] in products:
        products[item['name']].append(item['price'])
    else:
        products[item['name']] = list()
        products[item['name']].append(item['price'])

productsParams = list()

for keys in products:
    averagePrice = sum(products[keys])/len(products[keys])
    minPrice = min(products[keys])
    maxPrice = max(products[keys])
    productsParams.append({'name': keys, 'averagePrice': averagePrice, 'maxPrice': maxPrice, 'minPrice': minPrice})

with open('answer_3_var_65.json', 'w') as answer:
    json.dump(productsParams, answer)


productsParamsMSGPACK = msgpack.packb(productsParams)

with open('msgpack_answer_3_var_65.msgpack', 'wb') as msgpackAnswer:
    msgpackAnswer.write(productsParamsMSGPACK)

# Размер msgpack немного меньше, чем у json