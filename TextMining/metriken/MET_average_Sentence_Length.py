import nltk


def MET_average_sentence_length(text, wordCount):
    sentTokens = nltk.sent_tokenize(text)
    nonWords = ['.',',','\\','/','#','!','?','^','&','*',';',':','{','}','=','-','_','`','~','“','”','"','(',')',"'",'""',"''",'<','>','[',']']
    sentenceTokensWithoutNonWords = [item for item in sentTokens if item not in nonWords]
    if sentenceTokensWithoutNonWords == []:
        averageSentenceLength = 0
    else:
        averageSentenceLength = wordCount/len(sentenceTokensWithoutNonWords)
    return averageSentenceLength