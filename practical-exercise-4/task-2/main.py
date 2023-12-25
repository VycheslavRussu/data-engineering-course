import sqlite3
import pandas as pd
import json

def parse_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def connect_to_db(file_name):
    return sqlite3.connect(file_name)

def insert_to_db(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO info (name, rating, convenience,
            security, functionality, comment) 
        VALUES(:name, :rating, :convenience,
            :security, :functionality, :comment)
    ''', data)
    db.commit()

data = parse_data('task_2_var_65_subitem.json')
db = connect_to_db('../task-1/task_1.db')
# insert_to_db(db, data)

cursor = db.cursor()

# Запрос 1

result_1_query = cursor.execute(f'''
    SELECT *
    FROM buildings
    JOIN info ON buildings.name = info.name
    WHERE (parking == 'True') AND rating BETWEEN 4 AND 5 
    ORDER BY rating DESC
''')

# print(result_1_query.fetchall())


# Запрос 2

result_2_query = cursor.execute(f'''
    SELECT buildings.id, buildings.name, buildings.city,
        buildings.year, info.rating, info.comment 
    FROM buildings
    JOIN info ON buildings.name = info.name
    WHERE (city == 'Кишинев') AND (security >= 3) AND (rating BETWEEN 4 AND 5) 
    ORDER BY rating DESC
''')


# print(result_2_query.fetchall())

# Запрос 3

result_3_query = cursor.execute(f'''
    SELECT buildings.city, buildings.year, info.rating 
    FROM buildings
    JOIN info ON buildings.name = info.name
    WHERE (security > 3) AND (rating > 4) 
    ORDER BY rating DESC
''')

# print(result_3_query.fetchall())