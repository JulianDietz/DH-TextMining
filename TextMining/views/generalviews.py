# -*- coding: utf-8 -*-
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from TextMining.models import Paper, Metadata
import json
from django.shortcuts import redirect
from os import listdir,system
from os.path import join
from TextMining import metriken
from TextMining.saveFile import savePaper

#currentJsonfiles=[]

'''init ntlk run:
import nltk
nltk.download('stopwords')
'''

def helloWorld(request):
    return render(request, 'helloWorld.html')


def processPaperView (request):
    context = {}
    return render(request, 'processPaper.html', context)

#Aufbereiten der Text Stopwortfiltern und lemmatisieren
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all()
    for paper in paperlist:
        print(paper)
        metriken.removeStopwords(paper) #MET_text_to_STOP_text
        #metriken.lemmatize_Paper(paper) #MET_text_to_LEMMA_text
        #metriken.char_count_per_section_Paper(paper) #MET_char_Count
        #metriken.citation_count_per_section_Paper(paper) #MET_citation_Count
        #metriken.punctuation_count_per_section_Paper(paper) #MET_punctuation_Count
        #metriken.word_count_per_section_Paper(paper) #MET_word_Count
        #metriken.sentencelength_average_per_section_Paper(paper) #MET_average_sentslength

    print("Papersind aufbereitet")
    return JsonResponse({'sucess': 'Super!!!!!'})

def readJsonFilesView (request):
    context = {}
    return render(request, 'readJsonFiles.html', context)

def readJsonFiles(request):
    # loads all Json files....
    readpath = "./outputNew20"
    onlyOne = False
    counter=0
    for filename in listdir(readpath):
        if not onlyOne:
            if filename != ".DS_Store": #file.endswith('.json')
                file = open(join(readpath, filename), 'r', encoding='utf-8', errors="ignore")
                paperJson = json.load(file)
                paper=savePaper(paperJson)
                counter+=1
        onlyOne=False

    return JsonResponse({'sucess':'Super!!!!!'})


#Testen obs klappt
def startDB(request):
    system('mongod')


'''def calculateMetriken(request):
    papers = Paper.objects.all()
    for paper in papers:
        words=metriken.calculateWords(paper)
        print(words)
    # save words in DB
    context = {'info': 'metriken werden berechnet'}
    categories = Metadata.objekts.distinct('category')
    return render(request, 'startseite.html', context, categories)

def calculateFreqWords(request):
    corpus1=metriken.calculateWordFrequency(Paper.objects.filter(metaData__category='Food & Nutrition'))
    #print(corpus1)
    corpus2 = metriken.calculateWordFrequency(Paper.objects.filter(metaData__category='Mathematics'))
    #print(corpus2)
    return render(request, 'old/freqWords.html', {"corpus1":corpus1, "corpus2":corpus2})

def showStartPage(request):
    return render(request, 'startseite.html')

def calculateMeanImpactFactor(impact):
    sum = 0
    counter = 0
    for factor in impact:
        sum += factor
        counter += 1
    mean = sum/counter
    return mean



#hier alles was benötigt wird rein, wird bei url:http://127.0.0.1:8000/textMining/vergleich/ aufgerufen
def showVergleichPage(request):
    categories = Paper.objects.distinct('metaData.category')
    #countries = Paper.objects.distinct('authors.authorList.university.university_universityCountry')
    #authors = Paper.objects.distinct('authors_authorList.authorName')
    #journals = Paper.objects.distinct('metaData.journalTitle')
    #impactfactor = Paper.objects.distinct('metaData.impactfactor')
    #meanimpact = calculateMeanImpactFactor(impactfactor)
    #keywords = Paper.objects.distinct('metaData.keywords')
    context = {'categories': categories}
    #context = {'categories': categories, 'countries':countries, 'authors': authors, 'journals': journals,
     #          'impactfactor': impactfactor, 'keywords':keywords}
    return render(request, 'vergleich.html',context)

#TODO DB files download!

def showResults(request):
    #1. getCorpora filterdata should bei in the request
    corpus1 = Paper.objects(title__icontains='physics')
    corpus2 = Paper.objects(title__icontains='speech')
    #2.calculate sum for some Metrtiken.
    dict={'average':None,'modus':None,'median':None,'varianz':None}
    print(len(corpus1))
    print(len(corpus2.distinct('title')))
    #Anzahl der Autoren
    #Anzahl der Referenzen
    #Anzahl unterschiedliche Universitäten
    print("Anzahl unterschiedliche Universitäten")
    print(len(corpus1.distinct(field='authors.authorList.university.university_universityCountry')))
    print(len(corpus2.distinct(field='authors.authorList.university.university_universityCountry')))
    #Anzahl der Keywords
    print("Anzahl der Keyword")
    print(len(corpus1.distinct('metaData.keywords')))
    print(len(corpus2.distinct('metaData.keywords')))
    #Häufigste Keywords
    #print("Häufigste Keywords")

    ######Analyse berechnen!
    corpus1result=[]
    for paper in corpus1:
        numpictures = 0
        numtables = 0
        numabsaetze = 0
        numsubabsaetze = 0
        numtablesdesclength = 0
        for section in paper.text:
            numabsaetze+=1
            numpictures+=section.pictures.count
            numtables += section.tables.count
            for table in section.tables.tablesList:
                numtablesdesclength+=len(table.tableDescription.split(' '))
            numsubabsaetze=+len(section.subsection)
        corpus1result.append({'tables':numtables,'pictures':numpictures,'absaetze':numabsaetze,'tabledescription':numtablesdesclength,'subabsaetze':numsubabsaetze})
    print(corpus1result)
    #Anzahl Tabellen
    #Anzahl Bilder
    #Anzahl Überschriften
    #Absätze pro Einheit
    #Tabelle durchschnittliche Beschriftungslänge
    #Readability
    
    result={'abstract':{'charcount':{'array':[],'result':{}}}}
    #calculate Metriken
    for paper in corpus1:
        for section in paper.abstract:
            result['abstract']['charcount']['array'].append(section.metrik.charCountResults.charCountNoWhiteSpace)
    print(result['abstract']['charcount']['array'])
    ######Analyse berechnen ende 
    context={'corpus1':corpus1,'corpus2':corpus2}
    return render(request, 'ergebnis.html',context)




@csrf_exempt
def ajaxCategorie (request):
    if request.method == 'POST':
        categorie=request.POST.get('categorie')
        print('get journals for categorie:'+categorie)
        categoriePaper=Paper.objects(metaData__category__exact=categorie)
        journalnames= categoriePaper.distinct('metaData.journalTitle')
        print(journalnames)
        response = {'journalnames':journalnames}
        return JsonResponse(response)

@csrf_exempt
def ajaxAuthor (request):
    if request.method == 'POST':
        journales=request.POST.get('journalnames')
        journalPaper = Paper.objects(metaData_journalTitle_exact=journales)
        authornames = journalPaper.distinct('authors.authorList.authorName')
        print(authornames)
        response = {'authornames':authornames}
        return JsonResponse(response)
'''