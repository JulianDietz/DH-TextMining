#from TextMining.models import ResPunctSegmentCount
import re

method="citationcount"

def punctuation_count_per_section_Paper(paper):
    # Abstract
    for section in paper.abstract:
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            punctCount= ResPunctSegmentCount(punctCount=MET_punctuation_count(section.text))
            section.metrik.punctCountResults = punctCount

    #Text
    for section in paper.text:
        print("punctCount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            punctCount = ResPunctSegmentCount(punctCount=MET_punctuation_count(section.text))
            section.metrik.punctCountResults = punctCount

        #Subtext
        for subsection in section.subsection:
            print("punctCount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                punctCount = ResPunctSegmentCount(punctCount=MET_punctuation_count(subsection.text))
                subsection.metrik.punctCountResults = punctCount
    paper.save()


#Count punctuation without citations
def MET_punctuation_count(text):
    #Remove quotes
    finding = re.findall(r'(?<!\[[0-9])[.,\/#!?\^&\*;:{}=\-_`~“”\"()]', text)
    return str(len(finding))


#checks if section has Wordcount with this method
def paperIsRehashed(section):
    return False


