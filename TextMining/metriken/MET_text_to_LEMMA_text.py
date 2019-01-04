from TextMining.models import TextVariant
from nltk.stem import WordNetLemmatizer
import nltk
import re

method="nltk lemmatizer: english"

wordnet_lemmatizer = WordNetLemmatizer()

def lemmatize_Paper(paper):
    # Abstract
    for section in paper.abstract:
        #print("leammtized:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            #print('not Lemmatized')
            lemmatizedText= TextVariant(text=lemmatize_text_segment(section.text),method=method)
            section.lemmatizedText = lemmatizedText

    #Text
    for section in paper.text:
        #print("leammtized:" + str(paperIsRehashed(section)))
        if not paperIsRehashed(section):
            lemmatizedText = TextVariant(text=lemmatize_text_segment(section.text), method=method)
            section.lemmatizedText = lemmatizedText

        #Subtext
        for subsection in section.subsection:
            #print("leammtized:"+str(paperIsRehashed(section)))
            if not paperIsRehashed(section):
                lemmatizedText = TextVariant(text=lemmatize_text_segment(subsection.text), method=method)
                subsection.lemmatizedText = (lemmatizedText)
    paper.save()


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a' #Adjektiv
    elif treebank_tag.startswith('V'):
        return 'v' #Verb
    elif treebank_tag.startswith('N'):
        return 'n' #Nomen
    elif treebank_tag.startswith('R'):
        return 'r'  #Adverb
    else:
        return 'n'



#Stopwortliste nltk(english) word to lowercase
def lemmatize_text_segment(text):
    #Remove quotes
    text_without_quotes = re.sub(r"(\[([0-9]+[,-]*)*\])", "", text)
    #Tokenize the text
    text_tokenized = nltk.word_tokenize(text_without_quotes)
    #Tag the text
    text_tagged = nltk.pos_tag(text_tokenized)

    #Lemmatize
    textWordNetLemmatizer = [wordnet_lemmatizer.lemmatize(word[0], get_wordnet_pos(word[1])) for word in text_tagged]

    return " ".join(textWordNetLemmatizer)

#checks if section has LemmatizedText with this method
def paperIsRehashed(section):
    return False

    """if section.lemmatizedText:
        for lemmatizedText in section.lemmatizedText:
            if lemmatizedText.method==method and lemmatizedText.text != "":
                print("Lemmatized Text Hier")
                print(lemmatizedText.text)
                return True
            else:
                return False
    else:
        return False"""


