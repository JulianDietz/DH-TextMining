#from TextMining.models import ResWordSegmentCount
import re

method="wordcount"

def word_count_per_section_Paper(paper):
    # Abstract
    for section in paper.abstract:
        print("wordcount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            wordCount= ResWordSegmentCount(wordCount=MET_word_count(section.text))
            section.metrik.wordCountResults = wordCount

    #Text
    for section in paper.text:
        print("wordcount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            wordCount = ResWordSegmentCount(wordCount=MET_word_count(section.text))
            section.metrik.wordCountResults = wordCount

        #Subtext
        for subsection in section.subsection:
            print("wordcount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                wordCount = ResWordSegmentCount(wordCount=MET_word_count(subsection.text))
                subsection.metrik.wordCountResults = wordCount
    paper.save()



def MET_word_count(text):
    #Remove quotes
    word_count = len(re.sub(r"(\s\[[^]]*\])", "", text).split(" "))
    return str(word_count)



def paperIsRehashed(section):
    return False


