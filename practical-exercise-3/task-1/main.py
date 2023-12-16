import statistics

from bs4 import BeautifulSoup
import json

# Функция, которая парсит данные с html страницы и возвращает словарь с нужными данными
def pars_data(file_name):
    with open(file_name, 'r') as f:
        content = f.read()

    info = dict()

    site = BeautifulSoup(content, 'html.parser')

    info['type'] = site.span.text.replace('Тип:', "").replace('\n', '').lstrip().split()[0]

    competition_list = site.h1.text.replace('\n', '').replace('Турнир:', '').lstrip().split()
    competition_name = str()
    for part in competition_list:
        competition_name += ' ' + part
    info['competition'] = competition_name.lstrip()

    town_and_date_list = site.p.text.replace('Начало:', '').replace('Город:', '').lstrip().split()
    info['town'] = town_and_date_list[0]
    info['start_date'] = town_and_date_list[1]

    info['rounds_count'] = int(site.find('span', class_='count').text.replace('Количество туров:', '').lstrip())
    info['time_control'] = int(site.find('span', class_='year').text.replace('Контроль времени:', '').replace('мин', '').lstrip())
    info['min_rate'] = int(site.find_all('span')[-3].text.replace('Минимальный рейтинг для участия:', '').lstrip())
    info['rate'] = float(site.find_all('span')[-2].text.replace('Рейтинг:', '').lstrip())
    info['views'] = int(site.find_all('span')[-1].text.replace('Просмотры:', '').lstrip())

    info['image_source'] = site.find('img')['src']

    return info



storage = list()

# Вызов функции для каждого файла
for i in range(1, 10):
    file_name = f'/Users/vycheslav/PycharmProjects/data-engineering-course/practical-exercise-3/task-1/zip_var_65/{i}.html'
    storage.append(pars_data(file_name))



# # Сохраниение JSONa
# json_storage = json.dumps(storage, ensure_ascii=False)
# with open('data.json', 'w', encoding='UTF-8') as file:
#     file.write(json_storage)


# Отсортированные по количеству туров данные
sorted_by_rounds_storage = sorted(storage, key=lambda x: x['rounds_count'])
print(sorted_by_rounds_storage)


# Отфильтрованные по названию города данные
filtred_by_town = list()
for town in storage:
    if town['town'] == 'Овьедо':
        filtred_by_town.append(town)


# Для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
total_sum = sum(dict['views'] for dict in storage)
min_value = min(dict['views'] for dict in storage)
max_value = max(dict['views'] for dict in storage)
mean_value = statistics.mean(dict['views'] for dict in storage)


# Для одного текстового поля посчитайте частоту меток
count_town = sum(dict['town'] == 'Овьедо' for dict in storage)
