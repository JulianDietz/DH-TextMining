import re

# Berechnet die Anzahl an Zitaten im Text. Zitate der Form [2,4,7] zählen dabei als 3 Zitate
# Zitate der Form [1-6] zählen als 6 Zitate
def MET_citation_count(text):
    finding = re.findall(r"(\[\d+(,*-?\d*)*\])", text)
    quoteCount = 0
    for quote in finding:
        if "," in quote[0]:
            quotes = quote[0].replace("[","").replace("]","").split(",")
            for splitQuote in quotes:
                if "-" in splitQuote:
                    splitQuote = splitQuote.split("-")
                    if splitQuote[1].isdigit() and splitQuote[0].isdigit():
                        quoteCount += int(splitQuote[1])-int(splitQuote[0]) +1
                else:
                    quoteCount = quoteCount +1
        else:
            if "-" in quote[0]:
                splitQuote = quote[0].replace("[","").replace("]","").split("-")
                quoteCount += int(splitQuote[1]) - int(splitQuote[0]) + 1
            else:
                quoteCount = quoteCount + 1
    return quoteCount


