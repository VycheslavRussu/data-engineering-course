import json
import sqlite3
import csv
import statistics
import pandas as pd

connection = sqlite3.connect('task_1.db')
cursor = connection.cursor()

def parse_data(file_name):
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        storage = list()
        for row in csv_reader:
            row_dict = {key: value for key, value in row.items()}
            storage.append(row_dict)
    return storage

def connect_to_db(file_name):
    return sqlite3.connect(file_name)

def insert_to_db(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO buildings (name, street, city,
            zipcode, floors, year, 
            parking, prob_price, views) 
        VALUES(
            :name, :street, :city,
            :zipcode, :floors, :year, 
            :parking, :prob_price, :views)
    ''', data)
    db.commit()

items = parse_data('task_1_var_65_item.csv')
db = connect_to_db('task_1.db')
# insert_to_db(db, items)
number = 65+10
cursor = db.cursor()


# Task 1
query_1 = cursor.execute(f'''
    SELECT *
    FROM buildings
    ORDER BY year ASC
    LIMIT {number}
''')

result_1 = query_1.fetchall()
keys = [description[0] for description in cursor.description]

result = list()
for item in result_1:
    result.append(dict(zip(keys, item)))

json_data = json.dumps(result, ensure_ascii=False)
with open('answer_1.json', 'w', encoding='UTF-8') as file:
    file.write(json_data)


# Task 2
# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
data_task_2 = cursor.execute('''
    SELECT floors
    FROM buildings
''')

values_list_2 = list()
for item in data_task_2.fetchall():
    values_list_2.append(item[0])

sum = sum(values_list_2)
min = min(values_list_2)
max = max(values_list_2)
mean = statistics.mean(values_list_2)

# print(sum, min, max, mean)

# Task 3
# Вывод частоты встречаемости для категориального поля;
df = pd.DataFrame(values_list_2)
# print(df.value_counts())


# Task 4
result_4_query = cursor.execute(f'''
    SELECT *
    FROM buildings
    WHERE parking == 'True'
    ORDER BY floors ASC
    LIMIT {number}
''')

result_4 = result_4_query.fetchall()

keys = [description[0] for description in cursor.description]
result = list()
for row in result_4:
    result.append(dict(zip(keys, row)))

json_data = json.dumps(result, ensure_ascii=False)
with open('answer_4.json', 'w', encoding='UTF-8') as file:
    file.write(json_data)
