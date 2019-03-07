import re

#Count punctuation without citations
def MET_punctuation_count(text):
    #Remove quotes
    finding = re.findall(r'(?<!\[[0-9])[.,\/#!?\^&\*;:{}=\-_`~“”\"()]', text)
    return len(finding)
