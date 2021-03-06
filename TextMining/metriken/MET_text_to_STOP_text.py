from nltk.corpus import stopwords
from TextMining.models import TextVariant
import nltk

# Loopt über alle Bereiche eines Papers und speichert deren Text gestoppwortfiltert in der Datenbank
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

#Stopwortliste nltk(english)
def getStopwordsForTextsection(text):
    text_As_Array = nltk.word_tokenize(text)
    textnostop = ""
    for word in text_As_Array:
        word = str(word).lower()
        if word not in stopwords.words('english'):
            textnostop += " " + word
    return textnostop

# Überprüft ob der Abschnitt schon gestoppwortfiltert gespeichert wurde
def paperIsRehashed(section,fieldname):
    if section[fieldname]:
        return True
    else:
        return False