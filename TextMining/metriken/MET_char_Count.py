#from TextMining.models import ResCharSegmentCount
import re

method="charcount"

def char_count_per_section_Paper(paper):
    # Abstract
    for section in paper.abstract:
        #print("charcount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            charCount= ResCharSegmentCount(charCountWhiteSpace =MET_char_count_WhiteSpace(section.text), charCountNoWhiteSpace= MET_char_count_No_WhiteSpace(section.text))
            section.metrik.charCountResults=charCount

    #Text
    for section in paper.text:
        #print("charcount:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            charCount = ResCharSegmentCount(charCountWhiteSpace=MET_char_count_WhiteSpace(section.text), charCountNoWhiteSpace = MET_char_count_No_WhiteSpace(section.text))
            section.metrik.charCountResults= charCount

        #Subtext
        for subsection in section.subsection:
           # print("charcount:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                charCount = ResCharSegmentCount(charCountWhiteSpace=MET_char_count_WhiteSpace(subsection.text), charCountNoWhiteSpace = MET_char_count_No_WhiteSpace(subsection.text))
                subsection.metrik.charCountResults= charCount
    paper.save()


#Stopwortliste nltk(english) word to lowercase
def MET_char_count_WhiteSpace(text):
    #Remove quotes
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    #Count the text length
    countWithWhitespace = len(text_without_quotes)
    return str(countWithWhitespace)


#Stopwortliste nltk(english) word to lowercase
def MET_char_count_No_WhiteSpace(text):
    #Remove quotes
    text_without_quotes = re.sub(r"(\s\[[^]]*\])", "", text)
    #Join the text and count length
    countNoWhitespace = len("".join(text_without_quotes.split()))

    #print (countNoWhitespace)
    return str(countNoWhitespace)



#checks if section has StemmedText with this method
def paperIsRehashed(section):
    return False
    """if section.metriks:
        if section.metriks.charCountResults.charCountWhiteSpace != "":
            return True
        else:
            return False
    else:
        return False"""

