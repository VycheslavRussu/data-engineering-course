import pymongo
import json

def connect_to_collection():
    # Устанавливаем соединение с MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017')
    # Подключаемся к БД task_1, если её нет, то будет создана новая с таким именем
    db = client['task_1']
    # Получаем коллекцию, если такой нет, то создаем
    collection = db['jobs']
    return collection

def parse_data(file_path):
    # Читаем json из прикрепленного файла
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def convert_to_json(value_to_convert, filename):
    with open(filename + '.json', 'w',  encoding='UTF-8') as file:
        json.dump(value_to_convert, file, ensure_ascii=False)
    return

# Вставляем данные из json'a в базу данных
# connect_to_collection().insert_many(parse_data('task_1_item.json'))

# Task 1
# Вывод первых 10 записей, отсортированных по убыванию по полю salary
query_1 = list(connect_to_collection().find(filter={},
                                            sort={'salary': -1},
                                            limit=10,
                                            projection={"_id": False}))
# convert_to_json(query_1, 'answer_1')

# Task 2
# вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортировать по убыванию по полю salary
query_2 = list(connect_to_collection().find(filter={'age': {'$lt': 30}},
                                            sort={'salary': -1},
                                            limit=15,
                                            projection={"_id": False}))
# convert_to_json(query_2, 'answer_2')

# Task 3
# Ввывод первых 10 записей, отфильтрованных по сложному предикату: (записи только из произвольного города,
# записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age
query_3 = list(connect_to_collection().find(filter={'city': 'Прага',
                                                    'job': {'$in': ['IT-специалист', 'Инженер', 'Косметолог']}},
                                            sort={'age': 1},
                                            limit=10,
                                            projection={"_id": False}))
# convert_to_json(query_3, 'answer_3')

# Task 4
# Вывод количества записей, получаемых в результате следующей фильтрации
# (age в произвольном диапазоне, year в [2019,2022], 50000 < salary <= 75000 || 125000 < salary < 150000).
query_4 = list(connect_to_collection().find(filter={'$and': [{'age': {'$gt': 20}},
                                                             {'age': {'$lt': 30}}],
                                                    '$or': [{'$and': [{'salary': {'$gt': 50000}},
                                                                      {'salary': {'$lte': 75000}}]},
                                                            {'$and': [{'salary': {'$gt': 125000}},
                                                                      {'salary': {'$lte': 150000}}]}]}))
print(len(query_4))
# 33