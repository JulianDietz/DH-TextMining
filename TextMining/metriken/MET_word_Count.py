import nltk

def MET_word_count(text):
    wordTokens = nltk.word_tokenize(text)
    Punctuation = ['.',',','\\','/','#','!','?','^','&','*',';',':','{','}','=','-','_','`','~','“','”','"','(',')',"'",'""',"''",'<','>']
    wordTokensWithoutPunctuation = [item for item in wordTokens if item not in Punctuation]
    wordCount = len(wordTokensWithoutPunctuation)
    return wordCount



