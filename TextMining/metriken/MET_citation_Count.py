import re

#Count punctuation without citations
def MET_citation_count(text):
    finding = re.findall(r"(\[\d+(,*-?\d*)*\])", text)
    quoteCount = 0
    for quote in finding:
        if "," in quote[0]:
            quotes = quote[0].replace("[","").replace("]","").split(",")
            for splitQuote in quotes:
                if "-" in splitQuote:
                    splitQuote = splitQuote.split("-")
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


