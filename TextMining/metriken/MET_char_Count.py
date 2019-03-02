import re

#Stopwortliste nltk(english) word to lowercase
def MET_char_count_WhiteSpace(text):
    #Remove quotes
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    #Count the text length
    countWithWhitespace = len(text_without_quotes)
    return str(countWithWhitespace)


#Stopwortliste nltk(english) word to lowercase
def MET_char_count_No_WhiteSpace(text):
    #Remove quotes
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    #Join the text and count length
    countNoWhitespace = len("".join(text_without_quotes.split()))

    #print (countNoWhitespace)
    return str(countNoWhitespace)
