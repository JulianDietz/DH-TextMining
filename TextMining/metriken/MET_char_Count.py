import re


# Berechnet die Anzahl an Zeichen in dem übergebenem Text
def MET_char_count_WhiteSpace(text):
    #Entfernt Zitate
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    countWithWhitespace = len(text_without_quotes)
    return countWithWhitespace


# Berechnet die Anzahl an Zeichen ohne Leerzeichen in dem übergebenem Text
def MET_char_count_No_WhiteSpace(text):
    # Entfernt Zitate
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    countNoWhitespace = len("".join(text_without_quotes.split()))
    return countNoWhitespace
