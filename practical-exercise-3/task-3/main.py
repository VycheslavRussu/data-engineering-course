from bs4 import BeautifulSoup
import json
import statistics
import pandas as pd

# ------------------------------------------------------------
# name: 'Антарес 1490'
# constellation: 'Водолей'
# spectral_class: 'J5I'
# radius: 942774099
# rotation_days: 348.62
# age: 1.44
# distance: 6506839.17
# absolute_magnitude: 8.03
# ------------------------------------------------------------


def pars_data(file_path):

    with open(file_path, 'r') as file:
        xml_data = file.read()

    xml_file = BeautifulSoup(xml_data, features='xml')

    item = dict()

    # Получение имени
    item_name = str()
    item_name_parts = xml_file.find('name').text.split()
    for part in item_name_parts:
        item_name += ' ' + part
    item['name'] = item_name.lstrip()
    item_name = ''

    item['constellation'] = xml_file.find('constellation').text.split()[0]
    item['spectral_class'] = xml_file.find('spectral-class').text.split()[0]
    item['radius'] = int(xml_file.find('radius').text.split()[0])
    item['rotation_days'] = float(xml_file.find('rotation').text.replace('days', '').replace(' ', ''))
    item['age'] = float(xml_file.find('age').text.replace('billion years', '').replace(' ', ''))
    item['distance'] = float(xml_file.find('distance').text.replace('million km', '').replace(' ', ''))
    item['absolute_magnitude'] = float(xml_file.find('absolute-magnitude').text.replace('million km', '').replace(' ', ''))

    return item


storage = list()

# Вызов функции для каждого файла
for i in range(1, 500):
    file_name = f'/Users/vycheslav/PycharmProjects/data-engineering-course/practical-exercise-3/task-3/zip_var_65/{i}.xml'
    storage.append(pars_data(file_name))

# Сохраниение JSONa
json_storage = json.dumps(storage, ensure_ascii=False)
with open('data.json', 'w', encoding='UTF-8') as file:
    file.write(json_storage)


# Отсортированные по возрасту данные
sorted_by_age_storage = sorted(storage, key=lambda x: x['age'])


# Отфильтрованные по (rotation_days) данные
filtred_by_rotation_days = list()
for item in storage:
    if item['rotation_days'] >= 360:
        filtred_by_rotation_days.append(item)


# Для одного выбранного числового поля (radius) посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
total_sum = sum(item['radius'] for item in storage)
min_value = min(item['radius'] for item in storage)
max_value = max(item['radius'] for item in storage)
mean_value = statistics.mean(item['radius'] for item in storage)


# Для одного текстового поля (spectral_class) посчитайте частоту меток
storage_df = pd.read_json('data.json')
values_freq = storage_df['spectral_class'].value_counts()




