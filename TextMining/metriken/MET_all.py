from TextMining.models import Metric
import re

def calculateAllMetrics(paper):
    #Titel
    addMetricForPart(paper.titleRaw)
    addMetricForPart(paper.titleNltkStw)

    # Abstract
    for section in paper.abstract:
        addMetricForPart(section.textNltkStw)
        addMetricForPart(section.titleNltkStw)
        addMetricForPart(section.textRaw)
        addMetricForPart(section.titleRaw)

    #Text
    for section in paper.content:
        addMetricForPart(section.textNltkStw)
        addMetricForPart(section.titleNltkStw)
        addMetricForPart(section.textRaw)
        addMetricForPart(section.titleRaw)

        #Subtext
        for subsection in section.subsection:
            addMetricForPart(subsection.textNltkStw)
            addMetricForPart(subsection.titleNltkStw)
            addMetricForPart(subsection.textRaw)
            addMetricForPart(subsection.titleRaw)

    paper.save()

def addMetricForPart(part):
    if not paperIsRehashed(part, 'metrik'):
        metrik = Metric(charCountWhiteSpace=MET_char_count_WhiteSpace(part.text),
                    charCountNoWhiteSpace=MET_char_count_No_WhiteSpace(part.text),
                    wordCount=MET_word_count(part.text),
                    punctCount=MET_punctuation_count(part.text),
                    citationCount=MET_citation_count(part.text))
        part.metrik = metrik

#checks if section has StemmedText with this method
def paperIsRehashed(section,fieldname):
    if section[fieldname]:
        return True
    else:
        return False

################## METRIKEN ######################

def MET_char_count_WhiteSpace(text):
    #Remove quotes
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    #Count the text length
    countWithWhitespace = len(text_without_quotes)
    return countWithWhitespace

def MET_char_count_No_WhiteSpace(text):
    #Remove quotes
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    #Join the text and count length
    countNoWhitespace = len("".join(text_without_quotes.split()))

    #print (countNoWhitespace)
    return countNoWhitespace

def MET_word_count(text):
    #Remove quotes
    word_count = len(re.sub(r"(\s\[[^]]*\])", "", text).split(" "))
    return word_count

#Count punctuation without citations
def MET_punctuation_count(text):
    #Remove quotes
    finding = re.findall(r'(?<!\[[0-9])[.,\/#!?\^&\*;:{}=\-_`~“”\"()]', text)
    return len(finding)

def MET_citation_count(text):
    # \[[^]]*\]
    # ['doctors having a degree in internal medicine (MD or DNB', 'Int Med)'] found
    # ValueError: invalid literal for int() with base 10: 'Int Med)'
    finding = re.findall(r"(\[[(\d+)(\-\d+)?]]*\])", text)
    quoteCount = 0
    for quote in finding:
        #print(quote)
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
    #print(quoteCount)
    return quoteCount