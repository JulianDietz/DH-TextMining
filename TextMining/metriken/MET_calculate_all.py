from TextMining.metriken import MET_char_count_WhiteSpace, MET_char_count_No_WhiteSpace, MET_word_count, \
    MET_punctuation_count, MET_citation_count
from TextMining.models import Metric

def calculateAllMetrics(paper):
    #Titel
    addMetricForPart(paper.titleRaw)
    addMetricForPart(paper.titleNltkStw)
    addMetricForPart(paper.titleNltkStem)

    # Abstract
    for section in paper.abstract:
        addMetricForPart(section.textNltkStw)
        addMetricForPart(section.titleNltkStw)
        addMetricForPart(section.textRaw)
        addMetricForPart(section.titleRaw)
        addMetricForPart(section.textNltkStem)
        addMetricForPart(section.titleNltkStem)

    #Text
    for section in paper.content:
        addMetricForPart(section.textNltkStw)
        addMetricForPart(section.titleNltkStw)
        addMetricForPart(section.textRaw)
        addMetricForPart(section.titleRaw)
        addMetricForPart(section.textNltkStem)
        addMetricForPart(section.titleNltkStem)

        #Subtext
        for subsection in section.subsection:
            addMetricForPart(subsection.textNltkStw)
            addMetricForPart(subsection.titleNltkStw)
            addMetricForPart(subsection.textRaw)
            addMetricForPart(subsection.titleRaw)
            addMetricForPart(subsection.textNltkStem)
            addMetricForPart(subsection.titleNltkStem)

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