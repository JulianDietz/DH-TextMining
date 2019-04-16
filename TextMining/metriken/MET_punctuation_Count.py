import re

# Berechnet die Anzahl an Interpunktionen im übergebenem Text
def MET_punctuation_count(text):
    finding = re.findall(r'(?<!\[[0-9])[.,\/#!?\^&\*;:{}=\-_`~“”\"()]', text)
    return len(finding)
