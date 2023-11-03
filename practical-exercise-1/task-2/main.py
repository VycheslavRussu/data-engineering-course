taskFile = open('text_2_var_65')

valueLines = taskFile.readlines()

with open('answer_2_var_65', 'w') as answerFile:
    for i in range(0, len(valueLines)):
        valueLines[i] = valueLines[i].split('/')
        valueLines[i] = [int(i) for i in valueLines[i]]
        print(round(sum(valueLines[i])/len(valueLines[i]), 1), file=answerFile)