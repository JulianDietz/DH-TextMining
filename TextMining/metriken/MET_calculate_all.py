from TextMining.metriken import MET_char_count_WhiteSpace, MET_char_count_No_WhiteSpace, MET_word_count, \
    MET_punctuation_count, MET_citation_count, MET_average_word_length, MET_average_sentence_length
from TextMining.models import Metric, TotalValues
import TextMining.models

def calculateAllMetrics(paper):
    splitters = ['.','!','?']
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
        paperText['NltkStem'].append(section.textNltkStem.text)
        paperText['Raw'].append(section.textRaw.text)

        abstractText['NltkStw'].append(section.textNltkStw.text)
        abstractText['Raw'].append(section.textRaw.text)
        abstractText['NltkStem'].append(section.textNltkStem.text)

        #fails for section.titleRaw.text="" ?
        if len(section.titleRaw.text) > 0:
            if section.titleRaw.text[-1] not in splitters:
                paperText['Raw'].append(section.titleRaw.text + ".")
                abstractTitles['Raw'].append(section.titleRaw.text + ".")
            else:
                paperText['Raw'].append(section.titleRaw.text)
                abstractTitles['Raw'].append(section.titleRaw.text)

        if len(section.titleNltkStem.text) > 0:
            if section.titleNltkStem.text[-1] not in splitters:
                paperText['NltkStem'].append(section.titleNltkStem.text + ".")
                abstractTitles['NltkStem'].append(section.titleNltkStem.text + ".")
            else:
                paperText['NltkStem'].append(section.titleNltkStem.text)
                abstractTitles['NltkStem'].append(section.titleNltkStem.text)

        if len(section.titleNltkStw.text) > 0:
            if section.titleNltkStw.text[-1] not in splitters:
                paperText['NltkStw'].append(section.titleNltkStw.text + ".")
                abstractTitles['NltkStw'].append(section.titleNltkStw.text + ".")
            else:
                paperText['NltkStw'].append(section.titleNltkStw.text)
                abstractTitles['NltkStw'].append(section.titleNltkStw.text)



    #Text
    for section in paper.content:
        addMetricForPart(section.textNltkStw)
        addMetricForPart(section.titleNltkStw)
        addMetricForPart(section.textRaw)
        addMetricForPart(section.titleRaw)
        addMetricForPart(section.textNltkStem)
        addMetricForPart(section.titleNltkStem)

        paperText['NltkStw'].append(section.textNltkStw.text)
        paperText['Raw'].append(section.textRaw.text)
        paperText['NltkStem'].append(section.textNltkStem.text)

        sectionText['NltkStw'].append(section.textNltkStw.text)
        sectionText['Raw'].append(section.textRaw.text)
        sectionText['NltkStem'].append(section.textNltkStem.text)

        if len(section.titleRaw.text) > 0:
            if section.titleRaw.text[-1] not in splitters:
                paperText['Raw'].append(section.titleRaw.text + ".")
                sectionTitles['Raw'].append(section.titleRaw.text + ".")
            else:
                paperText['Raw'].append(section.titleRaw.text)
                sectionTitles['Raw'].append(section.titleRaw.text)

        if len(section.titleNltkStem.text) > 0:
            if section.titleNltkStem.text[-1] not in splitters:
                paperText['NltkStem'].append(section.titleNltkStem.text + ".")
                sectionTitles['NltkStem'].append(section.titleNltkStem.text + ".")
            else:
                paperText['NltkStem'].append(section.titleNltkStem.text)
                sectionTitles['NltkStem'].append(section.titleNltkStem.text)

        if len(section.titleNltkStw.text) > 0:
            if section.titleNltkStw.text[-1] not in splitters:
                paperText['NltkStw'].append(section.titleNltkStw.text + ".")
                sectionTitles['NltkStw'].append(section.titleNltkStw.text + ".")
            else:
                paperText['NltkStw'].append(section.titleNltkStw.text)
                sectionTitles['NltkStw'].append(section.titleNltkStw.text)


        #Subtext
        for subsection in section.subsection:
            addMetricForPart(subsection.textNltkStw)
            addMetricForPart(subsection.titleNltkStw)
            addMetricForPart(subsection.textRaw)
            addMetricForPart(subsection.titleRaw)
            addMetricForPart(subsection.textNltkStem)
            addMetricForPart(subsection.titleNltkStem)

            paperText['NltkStw'].append(section.textNltkStw.text)
            paperText['Raw'].append(section.textRaw.text)
            paperText['NltkStem'].append(section.textNltkStem.text)

            subsectionText['NltkStw'].append(section.textNltkStw.text)
            subsectionText['Raw'].append(section.textRaw.text)
            subsectionText['NltkStem'].append(section.textNltkStem.text)

            if len(section.titleRaw.text) > 0:
                if section.titleRaw.text[-1] not in splitters:
                    paperText['Raw'].append(section.titleRaw.text + ".")
                    subsectionTitles['Raw'].append(section.titleRaw.text + ".")
                else:
                    paperText['Raw'].append(section.titleRaw.text)
                    subsectionTitles['Raw'].append(section.titleRaw.text)

            if len(section.titleNltkStem.text) > 0:
                if section.titleNltkStem.text[-1] not in splitters:
                    paperText['NltkStem'].append(section.titleNltkStem.text + ".")
                    subsectionTitles['NltkStem'].append(section.titleNltkStem.text + ".")
                else:
                    paperText['NltkStem'].append(section.titleNltkStem.text)
                    subsectionTitles['NltkStem'].append(section.titleNltkStem.text)

            if len(section.titleNltkStw.text) > 0:
                if section.titleNltkStw.text[-1] not in splitters:
                    paperText['NltkStw'].append(section.titleNltkStw.text +".")
                    subsectionTitles['NltkStw'].append(section.titleNltkStw.text + ".")
                else:
                    paperText['NltkStw'].append(section.titleNltkStw.text)
                    subsectionTitles['NltkStw'].append(section.titleNltkStw.text)

    variants = ['Raw','NltkStem','NltkStw']
    for variant in variants:
        paperText[variant] = "" + (" ".join(paperText[variant]))
        abstractTitles[variant] = "" + (" ".join(abstractTitles[variant]))
        abstractText[variant] = "" + (" ".join(abstractText[variant]))
        sectionTitles[variant] = "" + (" ".join(sectionTitles[variant]))
        sectionText[variant] = "" + (" ".join(sectionText[variant]))
        subsectionTitles[variant] = "" + (" ".join(subsectionTitles[variant]))
        subsectionText[variant] = "" + (" ".join(subsectionText[variant]))

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



def addTotalsForAveragedMetriks(paper,paperText,abstractTitles,abstractText,sectionTitles,sectionText,
                                subsectionTitles,subsectionText):

    averageWordLengthPaperTextRaw = MET_average_word_length(paperText['Raw'])
    averageWordLengthAbstractTitlesRaw = MET_average_word_length(abstractTitles['Raw'])
    averageWordLengthAbstractTextRaw = MET_average_word_length(abstractText['Raw'])
    averageWordLengthSectionTitlesRaw = MET_average_word_length(sectionTitles['Raw'])
    averageWordLengthSectionTextRaw = MET_average_word_length(sectionText['Raw'])
    averageWordLengthSubsectionTitlesRaw = MET_average_word_length(subsectionTitles['Raw'])
    averageWordLengthSubsectionTextRaw = MET_average_word_length(subsectionText['Raw'])

    averageWordLengthPaperTextNltkStem = MET_average_word_length(paperText['NltkStem'])
    averageWordLengthAbstractTitlesNltkStem = MET_average_word_length(abstractTitles['NltkStem'])
    averageWordLengthAbstractTextNltkStem = MET_average_word_length(abstractText['NltkStem'])
    averageWordLengthSectionTitlesNltkStem = MET_average_word_length(sectionTitles['NltkStem'])
    averageWordLengthSectionTextNltkStem = MET_average_word_length(sectionText['NltkStem'])
    averageWordLengthSubsectionTitlesNltkStem = MET_average_word_length(subsectionTitles['NltkStem'])
    averageWordLengthSubsectionTextNltkStem = MET_average_word_length(subsectionText['NltkStem'])

    averageWordLengthPaperTextNltkStw = MET_average_word_length(paperText['NltkStw'])
    averageWordLengthAbstractTitlesNltkStw = MET_average_word_length(abstractTitles['NltkStw'])
    averageWordLengthAbstractTextNltkStw = MET_average_word_length(abstractText['NltkStw'])
    averageWordLengthSectionTitlesNltkStw = MET_average_word_length(sectionTitles['NltkStw'])
    averageWordLengthSectionTextNltkStw = MET_average_word_length(sectionText['NltkStw'])
    averageWordLengthSubsectionTitlesNltkStw = MET_average_word_length(subsectionTitles['NltkStw'])
    averageWordLengthSubsectionTextNltkStw = MET_average_word_length(subsectionText['NltkStw'])

    averageSentenceLengthPaperTextRaw = MET_average_sentence_length(paperText['Raw'],
                                                                        MET_word_count(paperText['Raw']))
    averageSentenceLengthAbstractTitlesRaw = MET_average_sentence_length(abstractTitles['Raw'],
                                                                        MET_word_count(abstractTitles['Raw']))
    averageSentenceLengthAbstractTextRaw = MET_average_sentence_length(abstractText['Raw'],
                                                                        MET_word_count(abstractText['Raw']))
    averageSentenceLengthSectionTitlesRaw = MET_average_sentence_length(sectionTitles['Raw'],
                                                                        MET_word_count(sectionTitles['Raw']))
    averageSentenceLengthSectionTextRaw = MET_average_sentence_length(sectionText['Raw'],
                                                                        MET_word_count(sectionText['Raw']))
    averageSentenceLengthSubsectionTitlesRaw = MET_average_sentence_length(subsectionTitles['Raw'],
                                                                        MET_word_count(subsectionTitles['Raw']))
    averageSentenceLengthSubsectionTextRaw = MET_average_sentence_length(subsectionText['Raw'],
                                                                        MET_word_count(subsectionText['Raw']))

    averageSentenceLengthPaperTextNltkStem = MET_average_sentence_length(paperText['NltkStem'],
                                                                        MET_word_count(paperText['NltkStem']))
    averageSentenceLengthAbstractTitlesNltkStem = MET_average_sentence_length(abstractTitles['NltkStem'],
                                                                        MET_word_count(abstractTitles['NltkStem']))
    averageSentenceLengthAbstractTextNltkStem = MET_average_sentence_length(abstractText['NltkStem'],
                                                                        MET_word_count(abstractText['NltkStem']))
    averageSentenceLengthSectionTitlesNltkStem = MET_average_sentence_length(sectionTitles['NltkStem'],
                                                                        MET_word_count(sectionTitles['NltkStem']))
    averageSentenceLengthSectionTextNltkStem = MET_average_sentence_length(sectionText['NltkStem'],
                                                                        MET_word_count(sectionText['NltkStem']))
    averageSentenceLengthSubsectionTitlesNltkStem = MET_average_sentence_length(subsectionTitles['NltkStem'],
                                                                        MET_word_count(subsectionTitles['NltkStem']))
    averageSentenceLengthSubsectionTextNltkStem = MET_average_sentence_length(subsectionText['NltkStem'],
                                                                        MET_word_count(subsectionText['NltkStem']))

    averageSentenceLengthPaperTextNltkStw = MET_average_sentence_length(paperText['NltkStw'],
                                                                        MET_word_count(paperText['NltkStw']))
    averageSentenceLengthAbstractTitlesNltkStw = MET_average_sentence_length(abstractTitles['NltkStw'],
                                                                        MET_word_count(abstractTitles['NltkStw']))
    averageSentenceLengthAbstractTextNltkStw = MET_average_sentence_length(abstractText['NltkStw'],
                                                                        MET_word_count(abstractText['NltkStw']))
    averageSentenceLengthSectionTitlesNltkStw = MET_average_sentence_length(sectionTitles['NltkStw'],
                                                                        MET_word_count(sectionTitles['NltkStw']))
    averageSentenceLengthSectionTextNltkStw = MET_average_sentence_length(sectionText['NltkStw'],
                                                                        MET_word_count(sectionText['NltkStw']))
    averageSentenceLengthSubsectionTitlesNltkStw = MET_average_sentence_length(subsectionTitles['NltkStw'],
                                                                        MET_word_count(subsectionTitles['NltkStw']))
    averageSentenceLengthSubsectionTextNltkStw = MET_average_sentence_length(subsectionText['NltkStw'],
                                                                        MET_word_count(subsectionText['NltkStw']))

    totalsRawAverageWordLength = TextMining.models.TotalValues(totalPaper=averageWordLengthPaperTextRaw,
                                                      totalAbstractTitles=averageWordLengthAbstractTitlesRaw,
                                                      totalAbstractText=averageWordLengthAbstractTextRaw,
                                                      totalSectionTitles=averageWordLengthSectionTitlesRaw,
                                                      totalSectionText=averageWordLengthSectionTextRaw,
                                                      totalSubsectionTitles=averageWordLengthSubsectionTitlesRaw,
                                                      totalSubsectionText=averageWordLengthSubsectionTextRaw)

    totalsNltkStemAverageWordLength = TextMining.models.TotalValues(totalPaper=averageWordLengthPaperTextNltkStem,
                                                      totalAbstractTitles=averageWordLengthAbstractTitlesNltkStem,
                                                      totalAbstractText=averageWordLengthAbstractTextNltkStem,
                                                      totalSectionTitles=averageWordLengthSectionTitlesNltkStem,
                                                      totalSectionText=averageWordLengthSectionTextNltkStem,
                                                      totalSubsectionTitles=averageWordLengthSubsectionTitlesNltkStem,
                                                      totalSubsectionText=averageWordLengthSubsectionTextNltkStem)

    totalsNltkStwAverageWordLength = TextMining.models.TotalValues(totalPaper=averageWordLengthPaperTextNltkStw,
                                                      totalAbstractTitles=averageWordLengthAbstractTitlesNltkStw,
                                                      totalAbstractText=averageWordLengthAbstractTextNltkStw,
                                                      totalSectionTitles=averageWordLengthSectionTitlesNltkStw,
                                                      totalSectionText=averageWordLengthSectionTextNltkStw,
                                                      totalSubsectionTitles=averageWordLengthSubsectionTitlesNltkStw,
                                                      totalSubsectionText=averageWordLengthSubsectionTextNltkStw)

    totalsRawAverageSentenceLength = TextMining.models.TotalValues(totalPaper=averageSentenceLengthPaperTextRaw,
                                                      totalAbstractTitles=averageSentenceLengthAbstractTitlesRaw,
                                                      totalAbstractText=averageSentenceLengthAbstractTextRaw,
                                                      totalSectionTitles=averageSentenceLengthSectionTitlesRaw,
                                                      totalSectionText=averageSentenceLengthSectionTextRaw,
                                                      totalSubsectionTitles=averageSentenceLengthSubsectionTitlesRaw,
                                                      totalSubsectionText=averageSentenceLengthSubsectionTextRaw)

    totalsNltkStemAverageSentenceLength = TextMining.models.TotalValues(totalPaper=averageSentenceLengthPaperTextNltkStem,
                                                      totalAbstractTitles=averageSentenceLengthAbstractTitlesNltkStem,
                                                      totalAbstractText=averageSentenceLengthAbstractTextNltkStem,
                                                      totalSectionTitles=averageSentenceLengthSectionTitlesNltkStem,
                                                      totalSectionText=averageSentenceLengthSectionTextNltkStem,
                                                      totalSubsectionTitles=averageSentenceLengthSubsectionTitlesNltkStem,
                                                      totalSubsectionText=averageSentenceLengthSubsectionTextNltkStem)

    totalsNltkStwAverageSentenceLength = TextMining.models.TotalValues(totalPaper=averageSentenceLengthPaperTextNltkStw,
                                                      totalAbstractTitles=averageSentenceLengthAbstractTitlesNltkStw,
                                                      totalAbstractText=averageSentenceLengthAbstractTextNltkStw,
                                                      totalSectionTitles=averageSentenceLengthSectionTitlesNltkStw,
                                                      totalSectionText=averageSentenceLengthSectionTextNltkStw,
                                                      totalSubsectionTitles=averageSentenceLengthSubsectionTitlesNltkStw,
                                                      totalSubsectionText=averageSentenceLengthSubsectionTextNltkStw)


    totalsForAveragedMetriks = TextMining.models.TotalValuesForAveragedMetriks(
        totalsAverageSentenceLengthRaw=totalsRawAverageSentenceLength,
        totalsAverageSentenceLengthNltkStw=totalsNltkStwAverageSentenceLength,
        totalsAverageSentenceLengthNltkStem=totalsNltkStemAverageSentenceLength,
        totalsAverageWordLengthRaw=totalsRawAverageWordLength,
        totalsAverageWordLengthNltkStw=totalsNltkStwAverageWordLength,
        totalsAverageWordLengthNltkStem=totalsNltkStemAverageWordLength
        )


    paper.totalValuesForAveragedMetriks = totalsForAveragedMetriks