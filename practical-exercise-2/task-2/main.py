import numpy as np

targetValue = 500 + 65
taskMatrix = np.load('matrix_65_2.npy')

x = np.array([])
y = np.array([])
z = np.array([])

for i in range(0, np.size(taskMatrix, 0)):
    for j in range(0, np.size(taskMatrix, 1)):
        if taskMatrix[i][j] > targetValue:
            x = np.append(x, i).astype(int)
            y = np.append(y, j).astype(int)
            z = np.append(z, taskMatrix[i][j]).astype(int)

np.savez('answer_2_var_65.npz', x=x, y=y, z=z)
np.savez_compressed('compressed_answer_2_var_65.npz', x=x, y=y, z=z)

# Размер файлов отличается почти в 10 раз