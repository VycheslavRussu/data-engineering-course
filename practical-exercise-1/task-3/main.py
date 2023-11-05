taskFile = open('text_3_var_65')
valueLines = taskFile.readlines()

limitValue = 50 + 65

with open('answer_3_var_65', 'w') as answerFile:
    for i in range(0, len(valueLines)):
        valueLines[i] = valueLines[i].split(',')
        for j in range(0, len(valueLines[i])):
            if valueLines[i][j] != 'NA':
                valueLines[i][j] = int(valueLines[i][j])
        for j in range(0, len(valueLines[i])-1):
            if valueLines[i][j] == 'NA':
                valueLines[i][j] = (valueLines[i][j-1] + valueLines[i][j+1])/2
        for j in range(0, len(valueLines[i])):
            if valueLines[i][j]**0.5 >= limitValue:
                print(valueLines[i][j], ',', sep='', end='', file=answerFile)
        print('', file=answerFile)
