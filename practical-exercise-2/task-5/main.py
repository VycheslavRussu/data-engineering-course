import pandas as pd
import json
import msgpack

taskDF = pd.read_csv('car_sales.csv')

# Удаляю поле с датами
carsDF = taskDF.drop(['Date'], axis=1)

# Расчет значений для годов выпуска машин
minYear = min(carsDF['Car Year'])
maxYear = max(carsDF['Car Year'])
modeYear = carsDF['Car Year'].value_counts().idxmax()

# Расчет значений для годов выпуска машин
maxSalePrice = max(carsDF['Sale Price'])
minSalePrice = min(carsDF['Sale Price'])
averageSalePrice = carsDF['Sale Price'].mean()
deviationSalePrice = carsDF['Sale Price'].std()

# Расчет значений для комиссии диллера
maxCommissionRate = max(carsDF['Commission Rate'])
minCommissionRate = min(carsDF['Commission Rate'])
averageCommissionRate = carsDF['Commission Rate'].mean()
deviationCommissionRate = carsDF['Commission Rate'].std()

# Расчет значений для дохода диллера
maxCommissionEarned = max(carsDF['Commission Earned'])
minCommissionEarned = min(carsDF['Commission Earned'])
averageCommissionEarned = carsDF['Commission Earned'].mean()
deviationCommissionEarned = carsDF['Commission Earned'].std()

# Лучший продавец
uniqueSales = carsDF['Salesperson'].value_counts()
bestSaler = uniqueSales.idxmax()

# Самый частый покупатель
uniqueCustomers = carsDF['Customer Name'].value_counts()
bestCustomer = uniqueCustomers.idxmax()

# Самый продаваемый бренд
uniqueCarMakeres = carsDF['Car Make'].value_counts()
bestCarMaker = uniqueCarMakeres.idxmax()

# Cамая продаваемая модель
uniqueCarModels = carsDF['Car Model'].value_counts()
bestCarModel = uniqueCarModels.idxmax()

answer = {'minYear': int(minYear), 'maxYear': int(maxYear), 'modeYear': int(modeYear),
          'minSalePrice': minSalePrice, 'maxSalePrice': maxSalePrice, 'averageSalePrice': averageSalePrice, 'deviationSalePrice': deviationSalePrice,
          'minCommissionRate': minCommissionRate, 'maxCommissionRate': maxCommissionRate, 'averageCommissionRate': averageCommissionRate, 'deviationCommissionRate': deviationCommissionRate,
          'minCommissionEarned': minCommissionEarned, 'maxCommissionEarned': maxCommissionEarned, 'averageCommissionEarned': averageCommissionEarned, 'deviationCommissionEarned': deviationCommissionEarned,
          'bestSaler': bestSaler, 'bestCustomer': bestCustomer, 'bestCarMaker': bestCarMaker, 'bestCarModel': bestCarModel}

answerDF = pd.DataFrame.from_dict(answer, orient='index').transpose()

answerDF.to_csv('answer_5.csv', index=False)
answerDF.to_pickle('answer_5.pkl')

with open('answer_5.msgpack', 'wb') as fileMSG:
    msgpack.dump(answer, fileMSG)

with open('answer_5.json', 'w') as file:
    json.dump(answer, file)

# msgpack: 467 bytes, csv: 564 bytes, json: 630 bytes, pkl: 1232 bytes