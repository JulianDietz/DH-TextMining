import re

def MET_word_count(text):
    #Remove quotes
    #TODO meinen word count hernehmen? ich glaub der wäre besser, siehe paper Efficiency of Development of Fish Industry in Uzbekistan
    #TODO titleNltkStw ist 6 statt 5
    word_count = len(re.sub(r"(\s\[[^]]*\])", "", text).split(" "))
    return word_count



