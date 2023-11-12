import numpy as np
import json

# Загрузка матрицы
taskMatrix = np.load('matrix_65.npy')

# Подсчет суммы всех элементов
sumAllElements = int(np.sum(taskMatrix))

# Подсчет среднего значения
meanValue = np.mean(taskMatrix)

# Подсчет суммы и среднего арифметического главной диагонали
sumMainDiagonal = int(np.trace(taskMatrix))
meanMainDiagonal = sumMainDiagonal / np.size(taskMatrix, 0)

# Подсчет суммы и среднего арифметического побочной диагонали
flippedMatrix = np.fliplr(taskMatrix)
sumSecondaryDiagonal = int(np.trace(flippedMatrix))
meanSecondaryDiagonal = sumSecondaryDiagonal / np.size(taskMatrix, 0)

# Поиск минимального и максимального значений
minValue = int(np.min(taskMatrix))
maxValue = int(np.max(taskMatrix))

# Дамп данных в json файл
answerJSON = {'sum': sumAllElements, 'avr': meanValue, 'sumMD': sumMainDiagonal, 'avrMD': meanSecondaryDiagonal, 'sumSD': sumSecondaryDiagonal, 'avrSD': meanSecondaryDiagonal, 'max': maxValue, 'min': minValue}
with open('answer_1_var_65.json', 'w') as file:
    json.dump(answerJSON, file)

# Нормализуем матрицу и сохраним её
normalizedMatrix = taskMatrix / sumAllElements
np.save('normalized_matrix.npy', normalizedMatrix)
