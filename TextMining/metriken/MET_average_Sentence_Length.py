import re
import nltk
from statistics import mean

def MET_average_sentence_length(text, wordCount):
    sentTokens = nltk.sent_tokenize(text)  # need to take out commas plus other stuff
    Punctuation = ['.',',','\\','/','#','!','?','^','&','*',';',':','{','}','=','-','_','`','~','“','”','"','(',')',"'",'""',"''"]
    sentenceTokensWithoutPunctuation = [item for item in sentTokens if item not in Punctuation]
    print(sentenceTokensWithoutPunctuation)
    if sentenceTokensWithoutPunctuation == []:
        averageSentenceLength = 0
    else:
        averageSentenceLength = wordCount/len(sentenceTokensWithoutPunctuation)
    return averageSentenceLength