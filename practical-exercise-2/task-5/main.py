import pandas as pd
import json

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

# 10 лучших продавцов
uniqueSales = carsDF['Salesperson'].value_counts()
bestSales = uniqueSales[0:10].to_dict()

# 10 самых частых покупателей
uniqueCustomers = carsDF['Customer Name'].value_counts()
bestCustomers = uniqueCustomers[0:10].to_dict()

# 10 самых продаваемых брендов автомобилей
uniqueCarMakeres = carsDF['Car Make'].value_counts()
bestCarMakers = uniqueCarMakeres[0:10].to_dict()

# 10 самых продаваемых моделей машин
uniqueCarModels = carsDF['Car Model'].value_counts()
bestCarModels = uniqueCarModels[0:10].to_dict()

answer = {'minYear': int(minYear), 'maxYear': int(maxYear), 'modeYear': int(modeYear),
          'minSalePrice': minSalePrice, 'maxSalePrice': maxSalePrice, 'averageSalePrice': averageSalePrice, 'deviationSalePrice': deviationSalePrice,
          'minCommissionRate': minCommissionRate, 'maxCommissionRate': maxCommissionRate, 'averageCommissionRate': averageCommissionRate, 'deviationCommissionRate': deviationCommissionRate,
          'minCommissionEarned': minCommissionEarned, 'maxCommissionEarned': maxCommissionEarned, 'averageCommissionEarned': averageCommissionEarned, 'deviationCommissionEarned': deviationCommissionEarned,
          'bestSales': bestSales, 'bestCustomers': bestCustomers, 'bestCarMakers': bestCarMakers, 'bestCarModels': bestCarMakers}

with open('answer_5.json', 'w') as file:
    json.dump(answer, file)