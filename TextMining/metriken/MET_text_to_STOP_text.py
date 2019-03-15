from nltk.corpus import stopwords
from TextMining.models import TextVariant
from nltk.tokenize import RegexpTokenizer

def removeStopwords(paper):
    #Titel
    section=paper
    if not paperIsRehashed(section,'titleNltkStw'):
        stopWordFilteredText_String = TextVariant(text=getStopwordsForTextsection(section.titleRaw.text))
        section.titleNltkStw = stopWordFilteredText_String

    # Abstract
    for section in paper.abstract:
        if not paperIsRehashed(section,'textNltkStw'):
            stopWordFilteredText_String = TextVariant(text=getStopwordsForTextsection(section.textRaw.text))
            section.textNltkStw = stopWordFilteredText_String
        if not paperIsRehashed(section,'titleNltkStw'):
            stopWordFilteredText_String = TextVariant(text=getStopwordsForTextsection(section.titleRaw.text))
            section.titleNltkStw = stopWordFilteredText_String

    #Text
    for section in paper.content:
        if not paperIsRehashed(section,'textNltkStw'):
            stopWordFilteredText_String = TextVariant(text=getStopwordsForTextsection(section.textRaw.text))
            section.textNltkStw = stopWordFilteredText_String
        if not paperIsRehashed(section,'titleNltkStw'):
            stopWordFilteredText_String = TextVariant(text=getStopwordsForTextsection(section.titleRaw.text))
            section.titleNltkStw = stopWordFilteredText_String

        #Subtext
        for subsection in section.subsection:
            if not paperIsRehashed(subsection,'textNltkStw'):
                stopWordFilteredText_String = TextVariant(text=getStopwordsForTextsection(subsection.textRaw.text))
                subsection.textNltkStw = stopWordFilteredText_String
            if not paperIsRehashed(subsection, 'titleNltkStw'):
                stopWordFilteredText_String = TextVariant(text=getStopwordsForTextsection(subsection.titleRaw.text))
                subsection.titleNltkStw = stopWordFilteredText_String
    paper.save()

#Stopwortliste nltk(english) word to lowercase
def getStopwordsForTextsection(text):
    #print('Ausgangstext:')
    #print(text)
    text_As_Array = RegexpTokenizer(r'\w+').tokenize(text) #Satzzeichen weg???!?!????
    #print("text:"+text)
    textnostop = ""
    for word in text_As_Array:
        word = str(word).lower()
        if word not in stopwords.words('english'):
            textnostop += " " + word
    #print('stopworttext:')
    #print(textnostop)
    return textnostop

#checks if section has StemmedText with this method
def paperIsRehashed(section,fieldname):
    if section[fieldname]:
        #print('vorhanden')
        return True
    else:
        #print('noch nicht vorhanden')
        return False