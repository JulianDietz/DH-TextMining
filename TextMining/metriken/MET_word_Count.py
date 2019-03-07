import re

def MET_word_count(text):
    #Remove quotes
    word_count = len(re.sub(r"(\s\[[^]]*\])", "", text).split(" "))
    return word_count



