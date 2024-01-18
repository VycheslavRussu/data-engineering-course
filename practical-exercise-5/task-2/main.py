import pickle
import json
import pymongo

def connect_to_collection():
    # Устанавливаем соединение с MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017')
    # Подключаемся к БД task_1, если её нет, то будет создана новая с таким именем
    db = client['task_1']
    # Получаем коллекцию, если такой нет, то создаем
    collection = db['jobs']
    return collection

def parse_data(file_path):
    # Читаем pkl из прикрепленного файла
    with open('task_2_item.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

def convert_to_json(value_to_convert, filename):
    with open(filename + '.json', 'w',  encoding='UTF-8') as file:
        json.dump(value_to_convert, file, ensure_ascii=False)
    return

def count_mean(list_of_dicts):
    sum = 0
    key_name = list(list_of_dicts[0].keys())[0]
    for item in list_of_dicts:
        sum += item[key_name]
    mean = sum/len(list_of_dicts)
    return round(mean, 2)


# Вставляем данные из pickle в базу данных
# connect_to_collection().insert_many(parse_data('task_2_item.pkl'))

# Вывод минимальной, средней, максимальной salary
min_salary = connect_to_collection().find_one(sort={'salary': 1})['salary']
max_salary = connect_to_collection().find_one(sort={'salary': -1})['salary']

all_salaries = list(connect_to_collection().find(sort={'salary': -1}, projection={'salary':True, '_id':False}))
mean_salary = count_mean(all_salaries)

answer_1 = {'min': min_salary,
            'max': max_salary,
            'mean': mean_salary}

convert_to_json(answer_1, 'answer_1')

# Вывод минимальной, средней, максимальной salary по городу
min_salary_city = connect_to_collection().find_one(filter={'city': 'Прага'}, sort={'salary': 1})['salary']
max_salary_city = connect_to_collection().find_one(filter={'city': 'Прага'}, sort={'salary': -1})['salary']

all_salaries_city = list(connect_to_collection().find(filter={'city': 'Прага'}, sort={'salary': -1}, projection={'salary':True, '_id':False}))
mean_salary_city = count_mean(all_salaries_city)

answer_2 = {'city': 'Прага',
            'min': min_salary_city,
            'max': max_salary_city,
            'mean': mean_salary_city}

convert_to_json(answer_2, 'answer_2')

# Вывод минимальной, средней, максимальной salary по профессии
min_salary_job = connect_to_collection().find_one(filter={'job': 'Медсестра'}, sort={'salary': 1})['salary']
max_salary_job = connect_to_collection().find_one(filter={'job': 'Медсестра'}, sort={'salary': -1})['salary']

all_salaries_job = list(connect_to_collection().find(filter={'job': 'Медсестра'}, sort={'salary': -1}, projection={'salary':True, '_id':False}))
mean_salary_job = count_mean(all_salaries_city)

answer_3 = {'job': 'Медсестра',
            'min': min_salary_job,
            'max': max_salary_job,
            'mean': mean_salary_job}

convert_to_json(answer_3, 'answer_3')

# Вывод минимального, среднего, максимального возраста по городу
min_age_city = connect_to_collection().find_one(filter={'city': 'Прага'}, sort={'age': 1})['age']
max_age_city = connect_to_collection().find_one(filter={'city': 'Прага'}, sort={'age': -1})['age']

all_age_city = list(connect_to_collection().find(filter={'city': 'Прага'}, sort={'age': -1}, projection={'age': True, '_id': False}))
mean_age_city = count_mean(all_age_city)

answer_4 = {'city': 'Прага',
            'min': min_age_city,
            'max': max_age_city,
            'mean': mean_age_city}

convert_to_json(answer_4, 'answer_4')

# Вывод минимального, среднего, максимального возраста по профессии
min_age_job = connect_to_collection().find_one(filter={'job': 'Медсестра'}, sort={'age': 1})['age']
max_age_job = connect_to_collection().find_one(filter={'job': 'Медсестра'}, sort={'age': -1})['age']

all_age_job = list(connect_to_collection().find(filter={'job': 'Медсестра'}, sort={'age': -1}, projection={'age': True, '_id': False}))
mean_age_job = count_mean(all_age_job)

answer_5 = {'job': 'Медсестра',
            'min': min_age_job,
            'max': max_age_job,
            'mean': mean_age_job}

convert_to_json(answer_5, 'answer_5')

# Вывод максимальной заработной платы при минимальном возрасте
max_salary_min_age = connect_to_collection().find_one(sort={'age': 1, 'salary': -1})
answer_6 = {'age': max_salary_min_age['age'],
            'salary': max_salary_min_age['salary']}
convert_to_json(answer_6, 'answer_6')

# Вывод минимальной заработной платы при максимальной возрасте
min_salary_max_age = connect_to_collection().find_one(sort={'age': -1, 'salary': 1})
answer_7 = {'age': min_salary_max_age['age'],
            'salary': min_salary_max_age['salary']}
convert_to_json(answer_7, 'answer_7')

# Вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50000, отсортировать вывод по любому полю.
min_age_city_salary = connect_to_collection().find_one(filter={'$and': [{'city': 'Прага'}, {'salary': {'$gt': 50000}}]}, sort={'age': 1})['age']
max_age_city_salary = connect_to_collection().find_one(filter={'$and': [{'city': 'Прага'}, {'salary': {'$gt': 50000}}]}, sort={'age': -1})['age']

all_age_city_salary = list(connect_to_collection().find(filter={'$and': [{'city': 'Прага'}, {'salary': {'$gt': 50000}}]}, sort={'age': -1}, projection={'age': True, '_id': False}))
mean_age_city_salary = count_mean(all_age_city_salary)

answer_8 = {'city': 'Прага',
            'min': min_age_city_salary,
            'max': max_age_city_salary,
            'mean': mean_age_city_salary}

convert_to_json(answer_8, 'answer_8')

# Вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65
min_9 = connect_to_collection().find_one(
    filter={
        "$and": [
            {"city": "Прага"},
            {"job": "Бухгалтер"},
            {
                "$or": [
                    {
                        "$and": [
                            {"age": {"$gt": 18}},
                            {"age": {"$lt": 25}}
                        ]
                    },
                    {
                        "$and": [
                            {"age": {"$gt": 50}},
                            {"age": {"$lt": 65}}
                        ]
                    }
                ]
            }
        ]
    },
    sort={"salary": 1}
)['salary']

max_9 = connect_to_collection().find_one(
    filter={
        "$and": [
            {"city": "Прага"},
            {"job": "Бухгалтер"},
            {
                "$or": [
                    {
                        "$and": [
                            {"age": {"$gt": 18}},
                            {"age": {"$lt": 25}}
                        ]
                    },
                    {
                        "$and": [
                            {"age": {"$gt": 50}},
                            {"age": {"$lt": 65}}
                        ]
                    }
                ]
            }
        ]
    },
    sort={"salary": -1}
)['salary']

answer_9 = {'city': 'Прага',
            'job': 'Бухглатер',
            'min': min_9,
            'max': max_9}


convert_to_json(answer_9, 'answer_9')