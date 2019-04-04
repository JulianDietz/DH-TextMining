from TextMining.metriken import MET_char_count_WhiteSpace, MET_char_count_No_WhiteSpace, MET_word_count, \
    MET_punctuation_count, MET_citation_count, MET_average_word_length, MET_average_sentence_length
from TextMining.models import Metric
def calculateAllMetrics(paper):
    #Total text to compute averaged metriks
    paperText = createTotalsDict()
    abstractTitles = createTotalsDict()
    abstractText = createTotalsDict()
    sectionTitles = createTotalsDict()
    sectionText = createTotalsDict()
    subsectionTitles = createTotalsDict()
    subsectionText = createTotalsDict()

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

        paperText['NltkStw'].append(section.textNltkStw.text)
        paperText['NltkStw'].append(section.titleNltkStw.text)
        paperText['Raw'].append(section.textRaw.text)
        paperText['Raw'].append(section.titleRaw.text)
        paperText['NltkStem'].append(section.textNltkStem.text)
        paperText['NltkStem'].append(section.titleNltkStem.text)

        abstractTitles['NltkStw'].append(section.titleNltkStw.text)
        abstractTitles['Raw'].append(section.titleRaw.text)
        abstractTitles['NltkStem'].append(section.titleNltkStem.text)

        abstractText['NltkStw'].append(section.textNltkStw.text)
        abstractText['Raw'].append(section.textRaw.text)
        abstractText['NltkStem'].append(section.textNltkStem.text)

    #Text
    for section in paper.content:
        addMetricForPart(section.textNltkStw)
        addMetricForPart(section.titleNltkStw)
        addMetricForPart(section.textRaw)
        addMetricForPart(section.titleRaw)
        addMetricForPart(section.textNltkStem)
        addMetricForPart(section.titleNltkStem)

        paperText['NltkStw'].append(section.textNltkStw.text)
        paperText['NltkStw'].append(section.titleNltkStw.text)
        paperText['Raw'].append(section.textRaw.text)
        paperText['Raw'].append(section.titleRaw.text)
        paperText['NltkStem'].append(section.textNltkStem.text)
        paperText['NltkStem'].append(section.titleNltkStem.text)

        sectionTitles['NltkStw'].append(section.titleNltkStw.text)
        sectionTitles['Raw'].append(section.titleRaw.text)
        sectionTitles['NltkStem'].append(section.titleNltkStem.text)

        sectionText['NltkStw'].append(section.textNltkStw.text)
        sectionText['Raw'].append(section.textRaw.text)
        sectionText['NltkStem'].append(section.textNltkStem.text)

        #Subtext
        for subsection in section.subsection:
            addMetricForPart(subsection.textNltkStw)
            addMetricForPart(subsection.titleNltkStw)
            addMetricForPart(subsection.textRaw)
            addMetricForPart(subsection.titleRaw)
            addMetricForPart(subsection.textNltkStem)
            addMetricForPart(subsection.titleNltkStem)

            paperText['NltkStw'].append(section.textNltkStw.text)
            paperText['NltkStw'].append(section.titleNltkStw.text)
            paperText['Raw'].append(section.textRaw.text)
            paperText['Raw'].append(section.titleRaw.text)
            paperText['NltkStem'].append(section.textNltkStem.text)
            paperText['NltkStem'].append(section.titleNltkStem.text)

            subsectionTitles['NltkStw'].append(section.titleNltkStw.text)
            subsectionTitles['Raw'].append(section.titleRaw.text)
            subsectionTitles['NltkStem'].append(section.titleNltkStem.text)

            subsectionText['NltkStw'].append(section.textNltkStw.text)
            subsectionText['Raw'].append(section.textRaw.text)
            subsectionText['NltkStem'].append(section.textNltkStem.text)

    addTotalsForAveragedMetriks(paper,paperText,abstractTitles,abstractText,sectionTitles,sectionText,
                                subsectionTitles,subsectionText)

    paper.save()

def addMetricForPart(part):
    if not paperIsRehashed(part, 'metrik'):
        metrikCharCountWhiteSpace = MET_char_count_WhiteSpace(part.text)
        metrikCharCountNoWhiteSpace = MET_char_count_No_WhiteSpace(part.text)
        metrikWordCount = MET_word_count(part.text)
        metrikPunctCount = MET_punctuation_count(part.text)
        metrikCitationCount = MET_citation_count(part.text)
        metrikAverageWordLength = MET_average_word_length(part.text)
        metrikAverageSentenceLength = MET_average_sentence_length(part.text, metrikWordCount)

        metrik = Metric(charCountWhiteSpace=metrikCharCountWhiteSpace,
                        charCountNoWhiteSpace=metrikCharCountNoWhiteSpace,
                        wordCount=metrikWordCount,
                        punctCount=metrikPunctCount,
                        citationCount=metrikCitationCount,
                        averageWordLength=metrikAverageWordLength,
                        averageSentenceLength=metrikAverageSentenceLength)
        part.metrik = metrik


#checks if section has StemmedText with this method
def paperIsRehashed(section,fieldname):
    if section[fieldname]:
        return True
    else:
        return False


def createTotalsDict():
    return {'Raw': [], 'NltkStem': [], 'NltkStw': []}


def addTotalMetrik(part):
    return ""

def addTotalsForAveragedMetriks(paper,paperText,abstractTitles,abstractText,sectionTitles,sectionText,
                                subsectionTitles,subsectionText):
    for section in paper.content:
        print(section.textRaw.text)
    paperText = []
    abstractTitles = []
    abstractText = []
    sectionTitles = []
    sectionText = []
    subsectionTitles = []
    subsectionText = []

    return ""


    totalPaper = FloatField()
    totalAbstractTitles = FloatField()
    totalAbstractText = FloatField()
    totalSectionTitles = FloatField()
    totalSectionText = FloatField()
    totalSubsectionTitles = FloatField()
    totalSubsectionText = FloatField()