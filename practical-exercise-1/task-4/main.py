import pandas as pd

# Чтение данных из CSV
columnsNames = ['id', 'first_name', 'last_name', 'age', 'income', 'phone_number']
inputDF = pd.read_csv('text_4_var_65', names = columnsNames)

# Удаление колонки с номерами
outputDF = inputDF.drop(['phone_number'], axis=1).copy()

# Подсчет среднего дохода и фильтрация строк, в которых доход меньше среднего
outputDF['income'] = outputDF['income'].str.slice(stop=-1)
outputDF['income'] = outputDF['income'].astype(int)
meanIncome = outputDF['income'].mean()
outputDF = outputDF[outputDF['income'] > meanIncome]

# Фильтрация строк, в которых возраст меньше 25 + (var mod 10)
filterAge = 25 + (65 % 10)
outputDF = outputDF[outputDF['age'] >= filterAge]

# Сортировка по ID и запись результатов в csv
outputDF = outputDF.sort_values(by = 'id')
outputDF.to_csv('answer_4_var_65.csv', index = False)