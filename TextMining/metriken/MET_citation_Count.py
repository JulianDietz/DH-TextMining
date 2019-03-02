import re

#Count punctuation without citations
def MET_citation_count(text):
    # \[[^]]*\]
    # ['doctors having a degree in internal medicine (MD or DNB', 'Int Med)'] found
    # ValueError: invalid literal for int() with base 10: 'Int Med)'
    finding = re.findall(r"(\[[(\d+)(\-\d+)?]]*\])", text)
    quoteCount = 0
    for quote in finding:
        print(quote)
        if "-" in quote:
            quotes = quote.replace("[","").replace("]","").split("-")
            #print(quotes)
            while "-" in quotes: quotes.remove("-")
            #print(quotes)
            quoteCount += (int(quotes[1]) -int(quotes[0])) + 1
        elif "," in quote:
            quotes = (quote.split(","))
            while "," in quotes: quotes.remove(",")
            quoteCount += len(quotes)
        else:
            quoteCount += 1
    print(quoteCount)
    return str(quoteCount)


