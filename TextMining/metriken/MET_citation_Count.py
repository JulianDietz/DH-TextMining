from TextMining.models import ResCitationSegmentCount
import re

method="citationcount"

def citation_count_per_section_Paper(paper):
    # Abstract
    for section in paper.abstract:
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            citCount= ResCitationSegmentCount(citationCount=MET_citation_count(section.text))
            section.metrik.citationCountResults = citCount

    #Text
    for section in paper.text:
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            citCount = ResCitationSegmentCount(citationCount=MET_citation_count(section.text))
            section.metrik.citationCountResults = citCount

        #Subtext
        for subsection in section.subsection:
            print("punctCount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                citCount = ResCitationSegmentCount(citationCount=MET_citation_count(subsection.text))
                subsection.metrik.citationCountResults = citCount
    paper.save()


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

#checks if section has Wordcount with this method
def paperIsRehashed(section):
    return False


