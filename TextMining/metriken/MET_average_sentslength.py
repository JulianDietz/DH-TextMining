from TextMining.models import ResWordSegmentCount
import re

method="sentsCount"


def sentencelength_average_per_section_Paper(paper):
    # Abstract
    for section in paper.abstract:
        #print("sentsCount" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            #sentsCount= ResWordSegmentCount.objects.create(sentsCount=MET_sents_count(section))
            section.metrik.sentslengthAverage = MET_sents_count(section.text)

    #Text
    for section in paper.text:
        #print("sentsCount" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            #sentsCount = ResWordSegmentCount.objects.create(sentsCount=MET_sents_count(section))
            section.metrik.sentslengthAverage = MET_sents_count(section.text)

        #Subtext
        for subsection in section.subsection:
            print("sentsCount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                #sentsCount = ResWordSegmentCount.objects.create(sentsCount=MET_sents_count(section))
                subsection.metrik.sentslengthAverage = MET_sents_count(section.text)
    paper.save()



def MET_sents_count(text):
    #Remove quotes
    sents = text.split('.')
    avg_len = sum(len(x.split()) for x in sents) / len(sents)
    return avg_len



def paperIsRehashed(section):
    return False


