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
from scipy import stats

import TextMining.models
import numpy as np

#currentJsonfiles=[]

def helloWorld(request):
    return render(request, 'helloWorld.html')


def processPaperView (request):
    context = {}
    return render(request, 'processPaper.html', context)

#Aufbereiten der Text Stopwortfiltern und lemmatisieren
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all()[4:8]
    for paper in paperlist:
        metriken.removeStopwords(paper) #MET_text_to_STOP_text
        metriken.lemmatize_Paper(paper) #MET_text_to_LEMMA_text
        metriken.char_count_per_section_Paper(paper) #MET_char_Count
        metriken.citation_count_per_section_Paper(paper) #MET_citation_Count
        metriken.punctuation_count_per_section_Paper(paper) #MET_punctuation_Count
        metriken.word_count_per_section_Paper(paper) #MET_word_Count
        metriken.sentencelength_average_per_section_Paper(paper) #MET_average_sentslength

    print("Papersind aufbereitet")
    context = {'paperlist': paperlist}
    return render(request, 'helloWorld.html', context)

def readJsonFilesView (request):
    context = {}
    return render(request, 'readJsonFiles.html', context)

def readJsonFiles(request):
    # loads all Json files....
    readpath = "./output"
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
'''

# corpus : Paper.objects(...)
# fieldPath : Pfad zum jeweiligen Feld, in der Form
# [{'field': 'abstract', 'listIndex': 0}, {'field': 'titleRaw'}, {'field': 'metrik'}, {'field': 'punctCount'}]
# für gewählte section, untersection, abstract etc

#durchschnittliche Wortlänge, urchschnittliche Satzlänge, Größe/Dichte Wortschatz = TTR wie laufen die?
# vorberechnet oder life ausrechnen? wie mit lemmatisiert?


def getStatisticalValues(inputarray):
    average = np.mean(inputarray)
    median = np.median(inputarray)
    mode = stats.mode(inputarray)
    variance = np.var(inputarray)
    return {'average': average, 'median': median, 'mode': mode, 'variance': variance}

#Erzeugt Array mit direktem Wert des gewählten Felds (aktuell noch String-Field) für jedes Paper/gewählte Section
#Anzahl Satzzeichen je Paper
#Anzahl Zeichen (mit und ohne Whitespace) je Paper
#Anzahl Wörter je Paper
#Anzahl Citations? (CitationCount) je Paper
#TODO sind die alle so performant? Allgemein und auf Performance testen
#TODO Läuft jede Metrik immer gleich für alle Sektionen und Subsektionen durch?
#TODO die beiden wieder raus?
def getFieldMetrik(corpus, fieldPath):
    values = []
    for paper in corpus:
        metrik = paper
        for subpath in fieldPath:
            if 'listIndex' in subpath:
                if getattr(metrik, subpath['field'])[subpath['listIndex']]:
                    metrik = getattr(metrik, subpath['field'])[subpath['listIndex']]
                else:
                    break
            else:
                if getattr(metrik, subpath['field']):
                    metrik = getattr(metrik, subpath['field'])
                else:
                    break
        values.append(int(metrik))
    return values

#Erzeugt Array mit Länge der gewählten Liste für jedes Paper/gewählte Section
#Anzahl Autoren je Paper
#Anzahl Referenzen je Paper
#Anzahl Keywords je Paper
#Anzahl Tabellen je Section
#Anzahl Bilder je Section
def getLengthFieldMetrik(corpus, listPath):
    values = []
    for paper in corpus:
        metrik = paper
        for subpath in listPath:
            if 'listIndex' in subpath:
                if getattr(metrik, subpath['field'])[subpath['listIndex']]:
                    metrik = getattr(metrik, subpath['field'])[subpath['listIndex']]
                else:
                    break
            else:
                if getattr(metrik, subpath['field']):
                    metrik = getattr(metrik, subpath['field'])
                else:
                    break
        values.append(len(metrik))
    return values


#TODO aktuell wird für jede Metrik immer über alle Paper geloopt anststatt nur einmal über alle Paper...  Passt?
#Anzahl der verschiedenen Universitäten je Paper
#TODO Brauchen wir nicht nur länge, sondern auch konkrete Namen der Universitäten je paper?
def getLengthDistinctUniversities(corpus):
    values = []
    for paper in corpus:
        distValues = []
        for author in paper.authors:
            if author.university.name not in distValues:
                distValues.append(author.university.name)
        values.append(len(distValues))
    return values

#Anzahl der verschiedenen Länder der Universitäten je Paper
#TODO Brauchen wir nicht nur länge, sondern auch konkrete Länder je paper?
def getLengthDistinctCountries(corpus):
    values = []
    for paper in corpus:
        distValues = []
        for author in paper.authors:
            if author.university.country not in distValues:
                distValues.append(author.university.country)
        values.append(len(distValues))
    return values


def getTotalAmountOfDistinctAuthors(corpus):
    return len(corpus.distinct('authors.name'))


def getTotalAmountOfDistinctReferences(corpus):
    return len(corpus.distinct('references.name'))


def getTotalAmountOfDistinctUniversities(corpus):
    return len(corpus.distinct('authors.university.name'))


def getTotalAmountOfDistinctCountries(corpus):
    return len(corpus.distinct('authors.university.country'))


def getTotalAmountOfDistinctKeywords(corpus):
    return len(corpus.distinct('metaData.keywords'))

#TODO auch anzahl paper je Universität/land berechnen?
#TODO titel jetzt mal rausgelassen, nur für Sectionen/Subsectionen
#TODO anschauen und testen da schon was falsch gehen kann...Ist das zu unperformant?
#TODO schwierig wenn man alle Metriken einzeln und alle Feldvarianten einzeln duchloopen könnnen soll, wär in einem loop sicher performanter?
def getCharCountWhiteSpace(corpus, textVariantField):
    sections = []
    subsections = []
    for paper in corpus:
        for sectionCount, section in enumerate(paper.content):
            #TODO Performanter wenn man statt immer if einfach nen try-except block mit dem Index macht? Macht der in der Schleife nix kaputt?
            #TODO statt charCountWhiteSpace nochmal getattr und in Methode als Parameter übergeben
            if sectionCount == len(sections):
                sections.append([])
                subsections.append([])
            #TODO existieren alle Textvarianten immer? Wenn ja if weg
            if getattr(section, textVariantField):
                textVariant = getattr(section, textVariantField)
                sections[sectionCount].append(textVariant.metrik.charCountWhiteSpace)
            for subsectionCount, subsection in enumerate(section.subsection):
                if subsectionCount == len(subsections[sectionCount]):
                    subsections[sectionCount].append([])
                if getattr(subsection, textVariantField):
                    subTextVariant = getattr(subsection, textVariantField)
                    subsections[sectionCount][subsectionCount].append(subTextVariant.metrik.charCountWhiteSpace)
    return sections, subsections




def getPunctuationCount(request):
    for paper in Paper.objects:
        paper.authors = [TextMining.models.Author(name="jkdsaklfd")]
        paper.metaData = TextMining.models.Metadata(keywords=["dskafakdjlk","dskljfasdkf","skdljlkfads"])
        paper.authors[0].university = TextMining.models.University(name="BLUniversity")
        content1 = TextMining.models.Section()
        content2 = TextMining.models.Section()
        metrik1 = TextMining.models.Metric(charCountWhiteSpace="12")
        metrik2 = TextMining.models.Metric(charCountWhiteSpace="16")
        metrik3 = TextMining.models.Metric(charCountWhiteSpace="17")
        metrik4 = TextMining.models.Metric(charCountWhiteSpace="18")
        metrik5 = TextMining.models.Metric(charCountWhiteSpace="19")
        content1.titleRaw = TextMining.models.TextVariant(metrik=metrik1)
        content2.titleRaw = TextMining.models.TextVariant(metrik=metrik2)
        subsection1 = TextMining.models.Subsection()
        subsection2 = TextMining.models.Subsection()
        subsection3 = TextMining.models.Subsection()
        subsection1.titleRaw = TextMining.models.TextVariant(metrik=metrik3)
        subsection2.titleRaw = TextMining.models.TextVariant(metrik=metrik4)
        subsection3.titleRaw = TextMining.models.TextVariant(metrik=metrik5)
        content1.subsection = [subsection1, subsection2, subsection3]
        content2.subsection = [subsection3, subsection3, subsection3]
        paper.content = [content1,content2]
        paper.save()

    print("hier")
    print(Paper.objects.values_list())

    #Beispiel FieldMetrik
    satzzeichen = [{'field': 'abstract', 'listIndex': 0}, {'field': 'titleRaw'}, {'field': 'metrik'}, {'field': 'punctCount'}]
    satzzeichenArray = getFieldMetrik(Paper.objects, satzzeichen)
    print("Satzzeichen:")
    print(getStatisticalValues(satzzeichenArray))

    #Beispiel ListMetrik
    keywords = [{'field': 'metaData'}, {'field': 'keywords'}]
    keywordsArray = getLengthFieldMetrik(Paper.objects, keywords)
    print("Keywords:")
    print(getStatisticalValues(keywordsArray))

    #Beispiel verschiedene Unis
    b = getLengthDistinctUniversities(Paper.objects)
    print("unis")
    print(b)

    a = getTotalAmountOfDistinctUniversities(Paper.objects)
    print(a)


    f,g = getCharCountWhiteSpace(Paper.objects, 'titleRaw')
    print("Hier:")
    print(f)
    print(g)




    return render(request, 'index.html')


'''
#TODO anderes funktioniert
def showResults(request):
    #1. getCorpora filterdata should be in the request
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