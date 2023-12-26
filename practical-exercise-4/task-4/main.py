import pickle
import csv
import sqlite3
import statistics

# --------------------------------------------------

# method:
# quantity_sub
# quantity_add
# price_abs
# price_percent
# remove
# available

# --------------------------------------------------

def parse_csv(file_name):
    with open(file_name, 'r') as file:
        csv_rows = csv.DictReader(file, delimiter=';')
        data = list()
        for row in csv_rows:
            row_dict = {key: value for key, value in row.items()}
            row_dict['version'] = 0
            data.append(row_dict)
    return data


def parse_pkl(file_name):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    return data


def connect_to_db(file_name):
    return sqlite3.connect(file_name)


def insert_to_db(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO products (name, price, quantity,
            category, fromCity, isAvailable, views, version) 
        VALUES (:name, :price, :quantity,
            :category, :fromCity, :isAvailable, :views, :version) 
    ''', data)
    db.commit()


def remove(db, name):
    cursor = db.cursor()
    cursor.execute('''
        DELETE FROM products
        WHERE name = ?
    ''', [name])
    db.commit()

def version_update(db, name):
    cursor = db.cursor()
    cursor.execute('''
        UPDATE products
        SET version = version + 1
        WHERE name = ?
    ''', [name])
    # db.commit()

def set_available(db, name, param):
    cursor = db.cursor()
    cursor.execute('''
            UPDATE products
            SET isAvailable = ?
            WHERE name = ?
        ''', (param, name))
    version_update(db, name)
    db.commit()

def price_percent(db, name, param):
    cursor = db.cursor()
    cursor.execute('''
            UPDATE products
            SET price = ROUND((price * (1 + ?)), 2)
            WHERE name = ?
        ''', (param, name))
    version_update(db, name)
    db.commit()

def price_abs(db, name, param):
    cursor = db.cursor()
    query = cursor.execute('''
            UPDATE products
            SET price = (price + ?)
            WHERE (name = ?) AND ((price + ?) > 0)
        ''', (param, name, param))
    if query.rowcount > 0:
        version_update(db, name)
        db.commit()

def update_quantity(db, name, param):
    cursor = db.cursor()
    query = cursor.execute('''
            UPDATE products
            SET quantity = quantity + ?
            WHERE (name = ?) AND ((quantity + ?) >= 0)
        ''', (param, name, param))
    if query.rowcount > 0:
        version_update(db, name)
        db.commit()

def handle_update(db, update_list):
    for item in update_list:
        if item['method'] == 'remove':
            remove(db, item['name'])
        elif item['method'] == 'available':
            set_available(db, item['name'], item['param'])
        elif item['method'] == price_percent:
            price_percent(db, item['name'], item['param'])
        elif item['method'] == price_abs:
            price_abs(db, item['name'], item['param'])
        elif item['method'] == 'quantity_sub':
            update_quantity(db, item['name'], item['param'])
        elif item['method'] == 'quantity_add':
            update_quantity(db, item['name'], item['param'])


db = connect_to_db('task_4.db')
cursor = db.cursor()
data_pkl = parse_pkl('task_4_var_65_update_data.pkl')
data_csv = parse_csv('task_4_var_65_product_data.csv')


# insert_to_db(db, data_csv)
# handle_update(db, data_pkl)

# Task 1
# Топ 10 самых обновляемых товаров
query_1 = cursor.execute('''
    SELECT id, name, version
    FROM products
    ORDER BY version DESC
    LIMIT 10
''')
# for item in query_1.fetchall():
#     print(item)

# Task 2
# проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
query_2 = cursor.execute('''
    SELECT price
    FROM products
''')

storage_2 = list()
for item in query_2.fetchall():
    storage_2.append(item[0])

summ_price = sum(storage_2)
min_price = min(storage_2)
max_price = max(storage_2)
mean_price = round(statistics.mean(storage_2), 2)

# print(summ_price, min_price, max_price, mean_price)


# Task 3
# проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
query_3 = cursor.execute('''
    SELECT quantity
    FROM products
''')

storage_3 = list()
for item in query_3.fetchall():
    storage_3.append(item[0])

summ_quantity = sum(storage_3)
min_quantity = min(storage_3)
max_quantity = max(storage_3)
mean_quantity = round(statistics.mean(storage_3), 2)

# print(summ_quantity, min_quantity, max_quantity, mean_quantity)


# Task 3
query_4 = cursor.execute('''
    SELECT name, price
    FROM products
    WHERE views > 50000
    ORDER BY views DESC
''')

# for item in query_4.fetchall():
#     print(item)