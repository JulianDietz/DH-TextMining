import nltk


def MET_average_sentence_length(text, wordCount):
    sentTokens = nltk.sent_tokenize(text)
    Punctuation = ['.',',','\\','/','#','!','?','^','&','*',';',':','{','}','=','-','_','`','~','“','”','"','(',')',"'",'""',"''",'<','>']
    sentenceTokensWithoutPunctuation = [item for item in sentTokens if item not in Punctuation]
    if sentenceTokensWithoutPunctuation == []:
        averageSentenceLength = 0
    else:
        averageSentenceLength = wordCount/len(sentenceTokensWithoutPunctuation)
    return averageSentenceLength