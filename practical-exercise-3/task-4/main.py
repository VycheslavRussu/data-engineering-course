from bs4 import BeautifulSoup
import json
import statistics
import pandas as pd

# ------------------------------------------------------------

# 'id': 732691969
# 'name': 'Converse Gloves F - 3070'
# 'category': 'Gloves'
# 'size': 'S'
# 'color': 'Голубой'
# 'material': 'Шерсть'
# 'price': 789480
# 'rating': 3.71
# 'reviews': 562632
# 'exclusive': 'no'
# 'sporty': 'yes'

# ------------------------------------------------------------

def pars_data_from_file(file_path):

    with open(file_path, 'r') as file:
        xml_data = file.read()

    xml_file = BeautifulSoup(xml_data, features='xml')

    storage = list()

    # Находим все продукты на странице по тегу <clothing>
    products_list = xml_file.find_all('clothing')

    for product in products_list:

        item = dict()

        # Т.к. параметры и их количество могут отличаться от товара к товару для каждого item'a получаем список его параметров
        tag_list = product.find_all()

        # Вытаскиваем параметры из каждого тега
        for tag in tag_list:
            if tag.name == 'name':
                item_name = str()
                item_name_parts = tag.text.split()
                for part in item_name_parts:
                    item_name += ' ' + part
                item[tag.name] = item_name.lstrip()
                item_name = ''
            elif (tag.name == 'price') or (tag.name == 'reviews'):
                item[tag.name] = int(tag.text.split()[0])
            elif tag.name == 'rating':
                item[tag.name] = float(tag.text.split()[0])
            else:
                item[tag.name] = tag.text.split()[0]

        storage.append(item)

    return(storage)


# Обход всех файлов и извлечение из них данных
storage_list = list()
for i in range (1, 100):
    file_path = f'/Users/vycheslav/PycharmProjects/data-engineering-course/practical-exercise-3/task-4/zip_var_65/{i}.xml'
    storage_list += pars_data_from_file(file_path)


# Сохраниение JSONa
json_storage = json.dumps(storage_list, ensure_ascii=False)
with open('data.json', 'w', encoding='UTF-8') as file:
    file.write(json_storage)


# Отсортированные по (price) данные
sorted_by_price_storage = sorted(storage_list, key=lambda x: x['price'])


# Отфильтрованные по (size) данные
filtred_by_size = list()
for item in storage_list:
    if item['size'] == 'XL':
        filtred_by_size.append(item)


# Для одного выбранного числового поля (price) посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
total_sum = sum(item['price'] for item in storage_list)
min_value = min(item['price'] for item in storage_list)
max_value = max(item['price'] for item in storage_list)
mean_value = statistics.mean(item['price'] for item in storage_list)


# Для одного текстового поля (spectral_class) посчитайте частоту меток
storage_df = pd.read_json('data.json')
values_freq = storage_df['size'].value_counts()
print(values_freq)