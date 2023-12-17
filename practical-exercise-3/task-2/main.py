from bs4 import BeautifulSoup
import json
import statistics
import pandas as pd

# ------------------------------------------------------------

# item_name: '5.9" Kingston 192GB'
# price: '278973'
# bonus_size: '2789'
# data_id: '25787'
# img: '/upload/733881.webp'

# various values depend on tag «li».
# Всего может быть 7 параметров

# processor: '6x1.6 ГГц'
# ram: '14'
# sim: '3'
# matrix: 'IPS'
# resolution: '1366x1080'
# camera: '19'
# acc: '4798'

# ------------------------------------------------------------

def pars_product_data(product):
    item = dict()

    # Получение имени
    item_name = str()
    item_name_parts = product.find('span').text.split()
    for part in item_name_parts:
        item_name += ' ' + part
    item['name'] = item_name.lstrip()
    item_name = ''

    # Получение основной информации
    item['price'] = int(product.find('price').text.replace('₽', '').replace('\n', '').replace(' ', ''))
    item['bonus_size'] = int(product.find('strong').text.replace('+ начислим', '').replace('бонусов', '').replace('\n', '').replace(' ', ''))
    item['data_id'] = product.find('a', class_='add-to-favorite')['data-id']
    item['img'] = product.find('img')['src']

    # Получение тэгов
    tags = product.find_all('li')
    for tag in tags:
        tag_name = tag['type']
        if tag_name == 'processor':
            item[tag_name] = tag.text.replace('\n', '').replace('ГГц', '').replace(' ', '')
        elif tag_name == 'ram':
            item[tag_name] = int(tag.text.replace('\n', '').replace('GB', '').replace(' ', ''))
        elif tag_name == 'sim':
            item[tag_name] = int(tag.text.replace('\n', '').replace('SIM', '').replace(' ', ''))
        elif tag_name == 'matrix':
            item[tag_name] = tag.text.replace('\n', '').replace(' ', '')
        elif tag_name == 'resolution':
            item[tag_name] = tag.text.replace('\n', '').replace(' ', '')
        elif tag_name == 'camera':
            item[tag_name] = int(tag.text.replace('\n', '').replace('MP', '').replace(' ', ''))
        elif tag_name == 'acc':
            item[tag_name] = int(tag.text.replace('\n', '').replace('мА * ч', '').replace(' ', ''))
        else:
            item[tag_name] = int(tag.text.replace('\n', '').replace(' ', ''))

    return item


def get_list_of_products_data(web_page):
    storage = list()
    all_products_list = web_page.find_all('div', class_='product-item')

    for product in all_products_list:
        storage.append(pars_product_data(product))

    return storage


def get_data_from_file(file_name):

    with open(file_name, 'r') as file:
        html_page = file.read()
        site = BeautifulSoup(html_page, 'html.parser')

    return get_list_of_products_data(site)



storage_list = list()

for i in range(1, 36):
    file_name = f'/Users/vycheslav/PycharmProjects/data-engineering-course/practical-exercise-3/task-2/zip_var_65/{i}.html'
    storage_list += get_data_from_file(file_name)


# Сохранение данных в json
storage_json = json.dumps(storage_list, ensure_ascii=False)
with open('data.json', 'w', encoding='UTF-8') as file:
    file.write(storage_json)


# Отсортированные по цене данные
sorted_values = sorted(storage_list, key=lambda x: x['price'])


# Отфильтрованные по RAM данные
filtred_values = list()
for item in storage_list:
    if ('ram' in item) and (item['ram'] > 12):
        filtred_values.append(item)


# Для одного выбранного числового поля (price) посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
total_sum = sum(item['price'] for item in storage_list)
min_price = min(item['price'] for item in storage_list)
max_price = max(item['price'] for item in storage_list)
mean_price = statistics.mean(item['price'] for item in storage_list)


# Для одного текстового поля (matrix) посчитайте частоту меток
storage_df = pd.read_json('data.json')
values_freq = storage_df['matrix'].value_counts()
