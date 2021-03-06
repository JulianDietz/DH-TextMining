import nltk

# Berechnet die Anzahl an Wörtern in dem übergebenem Text
def MET_word_count(text):
    wordTokens = nltk.word_tokenize(text)
    nonWords = ['.', ',', '\\', '/', '#', '!', '?', '^', '&', '*', ';', ':', '{', '}', '=', '-', '_', '`', '~',
                '“', '”', '"', '(', ')', "'", '""', "''", '<', '>', '[', ']', ' ', '%', '&', '§', "’","", '']
    wordTokensWithoutNonWords = [item for item in wordTokens if item not in nonWords]
    wordCount = len(wordTokensWithoutNonWords)
    return wordCount



