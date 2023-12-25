import sqlite3
import pandas as pd
import json
import csv
import statistics

def parse_csv(file_name):
    with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        data = list()
        for row in csv_reader:
            row_dict = {key: value for key, value in row.items()}
            row_dict['instrumentalness'] = ''
            row_dict['explicit'] = ''
            data.append(row_dict)

    return data

def parse_txt(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    data = list()
    item = dict()

    for line in lines:
        if line == '=====\n':
            data.append(item.copy())
        else:
            splitted = line.split('::')
            if splitted[0] in ['duration_ms', 'year']:
                item[splitted[0]] = int(splitted[1])
            elif splitted[0] in ['tempo', 'instrumentalness', 'loudness']:
                item[splitted[0]] = float(splitted[1])
            else:
                item[splitted[0]] = splitted[1].replace('\n', '')
            item['key'] = ''
            item['energy'] = ''
    return data

def connect_to_db(file_name):
    return sqlite3.connect(file_name)

def insert_to_db(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO music (artist, song, duration_ms,
            year, tempo, genre, energy, key,
            loudness, instrumentalness, explicit) 
        VALUES (:artist, :song, :duration_ms,
            :year, :tempo, :genre, :energy, :key,
            :loudness, :instrumentalness, :explicit) 
    ''', data)
    db.commit()

# Получение данных
data_from_text = parse_txt('task_3_var_65_part_1.text')
data_from_csv = parse_csv('task_3_var_65_part_2.csv')
storage = data_from_csv + data_from_text

db = connect_to_db('task_3.db')

# Загрузка в базу данных
# insert_to_db(db, storage)


# Task 1
# вывод первых (VAR+10) отсортированных по произвольному числовому полю строк

number = 65+10
cursor = db.cursor()
query_1 = cursor.execute(f'''
    SELECT *
    FROM music
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
query_2 = cursor.execute('''
    SELECT duration_ms
    FROM music
''')

values_list_2 = list()
for item in query_2.fetchall():
    values_list_2.append(item[0])

sum = sum(values_list_2)
min = min(values_list_2)
max = max(values_list_2)
mean = statistics.mean(values_list_2)


# Task 3
# Вывод частоты встречаемости для категориального поля;
query_3 = cursor.execute('''
    SELECT genre
    FROM music
''')

values_list_3 = list()
for item in query_3.fetchall():
    values_list_3.append(item[0])

df = pd.DataFrame(values_list_3)
# print(df.value_counts())



# Task 4
result_4_query = cursor.execute(f'''
    SELECT *
    FROM music
    WHERE genre == 'hip hop'
    ORDER BY year ASC
    LIMIT 80
''')

result_4 = result_4_query.fetchall()

keys = [description[0] for description in cursor.description]
result = list()
for row in result_4:
    result.append(dict(zip(keys, row)))

json_data = json.dumps(result, ensure_ascii=False)
with open('answer_4.json', 'w', encoding='UTF-8') as file:
    file.write(json_data)

