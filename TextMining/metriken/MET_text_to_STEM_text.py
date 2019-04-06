from nltk.corpus import stopwords
from TextMining.models import TextVariant
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

def stemText(paper):
    #Titel
    section=paper
    if not paperIsRehashed(section,'titleNltkStem'):
        stemmedText_String = TextVariant(text=getStemForTextsection(section.titleRaw.text))
        section.titleNltkStem = stemmedText_String

    # Abstract
    for section in paper.abstract:
        if not paperIsRehashed(section,'textNltkStem'):
            stemmedText_String = TextVariant(text=getStemForTextsection(section.textRaw.text))
            section.textNltkStem = stemmedText_String
        if not paperIsRehashed(section,'titleNltkStem'):
            stemmedText_String = TextVariant(text=getStemForTextsection(section.titleRaw.text))
            section.titleNltkStem = stemmedText_String

    #Text
    for section in paper.content:
        if not paperIsRehashed(section,'textNltkStem'):
            stemmedText_String = TextVariant(text=getStemForTextsection(section.textRaw.text))
            section.textNltkStem = stemmedText_String
        if not paperIsRehashed(section,'titleNltkStem'):
            stemmedText_String = TextVariant(text=getStemForTextsection(section.titleRaw.text))
            section.titleNltkStem = stemmedText_String

        #Subtext
        for subsection in section.subsection:
            if not paperIsRehashed(subsection,'textNltkStem'):
                stemmedText_String = TextVariant(text=getStemForTextsection(subsection.textRaw.text))
                subsection.textNltkStem = stemmedText_String
            if not paperIsRehashed(subsection, 'titleNltkStem'):
                stemmedText_String = TextVariant(text=getStemForTextsection(subsection.titleRaw.text))
                subsection.titleNltkStem = stemmedText_String
    paper.save()


#PorterStemmer nltk
def getStemForTextsection(text):
    ps = PorterStemmer()
    text_As_Array = RegexpTokenizer(r'\w+').tokenize(text) #Satzzeichen weg??
    textstemmed = ""
    #words = word_tokenize(sentence)
    for word in text_As_Array:
        textstemmed += " " + ps.stem(word)
    return textstemmed

#checks if section has StemmedText with this method
def paperIsRehashed(section,fieldname):
    if section[fieldname]:
        return True
    else:
        return False