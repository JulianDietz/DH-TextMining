import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


def calculateWords(paper):
    #calculate for Abschnitte
    #print(Paper.text)
    response={}
    total=0
    for index,text in enumerate(paper.text):
        #print(text.title)
        #print(len(text.title))
        #print(text.text)
        total+=len(text.title)
        total+=len(text.text)
        response['abschnitt'+str(index)]=len(text.text)+len(text.title)
    response['total']=total
    return response


def calculateWordFrequency(paperlist):
    #only for the title
    alltext=""
    for paper in paperlist:
        for text in paper.text:
            alltext+=text.text

    corpus=RegexpTokenizer(r'\w+').tokenize(alltext)

    #remove stopwords
    listnostop=[]
    for word in corpus:
        word=word.lower()
        if word not in stopwords.words('english'):
            listnostop.append(word)

    fd = FreqDist(listnostop).most_common()
    #create dict
    dict={}
    for entry in fd:
        dict[entry[0]]=entry[1]
    return dict