import re
import copy

taskFile = open('text_1_var_65')
allWords = re.findall(r'\w+', taskFile.read())

searchList = copy.copy(allWords)
uniqeWordsCountDict = {}

uniqeWords = list(set(searchList))
for i in range(0, len(uniqeWords) - 1):
    uniqeWordsCountDict[searchList[i]] = searchList.count(uniqeWords[i])

sorted_uniqeWordsCount = sorted(uniqeWordsCountDict.items(), key=lambda x: x[1], reverse=True)
word = [item[0] for item in sorted_uniqeWordsCount]
count = [item[1] for item in sorted_uniqeWordsCount]

with open('answer_1_var_65', 'w') as answerFile:
    for j in range(0, len(sorted_uniqeWordsCount)-1):
        print(word[j],':', count[j], file=answerFile)