import re
import nltk
from statistics import mean

def MET_average_word_length(text):
    wordTokens = nltk.word_tokenize(text)  # need to take out commas plus other stuff
    Punctuation = ['.',',','\\','/','#','!','?','^','&','*',';',':','{','}','=','-','_','`','~','“','”','"','(',')',"'",'""',"''"]
    wordTokensWithoutPunctuation = [item for item in wordTokens if item not in Punctuation]
    wordLengths = [len(item) for item in wordTokensWithoutPunctuation]
    if wordLengths == []:
        averageWordLengths = 0
    else:
        averageWordLengths = mean(wordLengths)
    return averageWordLengths
