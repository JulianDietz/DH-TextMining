import nltk
from statistics import mean

def MET_average_word_length(text):
    wordTokens = nltk.word_tokenize(text)
    nonWords = ['.',',','\\','/','#','!','?','^','&','*',';',':','{','}','=','-','_','`','~','“','”','"','(',')',"'",'""',"''",'<','>','[',']']
    wordTokensWithoutNonWords = [item for item in wordTokens if item not in nonWords]
    wordLengths = [len(item) for item in wordTokensWithoutNonWords]
    if wordLengths == []:
        averageWordLengths = 0
    else:
        averageWordLengths = mean(wordLengths)
    return averageWordLengths
