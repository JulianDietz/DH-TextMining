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
        metriken.calculateAllMetrics(paper)
        '''
        metriken.lemmatize_Paper(paper) #MET_text_to_LEMMA_text
        metriken.char_count_per_section_Paper(paper) #MET_char_Count
        metriken.citation_count_per_section_Paper(paper) #MET_citation_Count
        metriken.punctuation_count_per_section_Paper(paper) #MET_punctuation_Count
        metriken.word_count_per_section_Paper(paper) #MET_word_Count
        metriken.sentencelength_average_per_section_Paper(paper) #MET_average_sentslength
        '''

    print("Papersind aufbereitet und vorberechnet")
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
'''
#TODO brauchen wir so sachen wie distinct über alle, oder sowas wie wieviel Paper pro Uni oder nicht?
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

def testMethode(request):
    getMetriksRaw(Paper.objects, wordCount=True)
    return render(request, 'index.html')

#TODO durchschnittliche Wortlänge, durchschnittliche Satzlänge, häufigste Wörter, Most Present Words (TF), Häufigste Keywords, Readability
#TODO was gemeint mit Größe/Dichte Wortschatz, Anzahl Überschriften (=alle Titles? dann ja nur einfach alle Sektionen?)
#TODO die können alle über den Text berechnet werden => text raw in dict werfen?

#TODO Schauen welche Felder immer in db, und welche mit if abfragen? Alle Liste in db immer mit [] machen wenn leer? Metadata für jedes da? Keywords
#TODO wenn leer []? was wenn zb. Sektion keinen titel hat? None immer abfragen?
#TODO Die einzelnen ifs in den Schleifen raus und immer appenden? Performance dann besser oder nicht?

def getStatisticalValues(inputarray):
    total = np.sum(inputarray)
    average = np.mean(inputarray)
    median = np.median(inputarray)
    mode = stats.mode(inputarray)
    variance = np.var(inputarray)
    return {'total': total,'average': average, 'median': median, 'mode': mode, 'variance': variance}


def newMetriksDictionaire():
    return {'Text': {'charCountWhiteSpace': [], 'charCountNoWhiteSpace': [], 'wordCount': [],
                     'punctCount': [], 'citationCount': [], 'textContent': []},
            'Title': {'charCountWhiteSpace': [], 'charCountNoWhiteSpace': [], 'wordCount': [],
                      'punctCount': [], 'citationCount': [], 'textContent': []},
            'tableCount': [], 'pictureCount': [], 'tableDescLengthCount': [], 'pictureDescLengthCount': []}


def appendFieldMetrik(condition, modelField, dict, title, text):
    if condition:
        dict['Titel'][modelField].append(getattr(title, modelField))
        dict['Text'][modelField].append(getattr(text, modelField))


def getMetriksRaw(corpus, variant, charCountWhiteSpace=False, charCountNoWhiteSpace=False, wordCount=False,
                  punctCount=False, citationCount=False, authorCount=False, referenceCount=False, universityCount=False,
                  countryCount=False, keywordCount=False, tableCount=False, pictureCount=False,
                  tableDescriptionCount=False, pictureDescriptionCount=False, keywordFrequency=False):

    abstracts = newMetriksDictionaire()
    #TODO Abstracts sind tatsächlich Liste
    sections = []
    subsections = []

    #TODO paper-title metriken
    resultsAuthorCount = []
    resultsReferenceCount = []
    resultsUniversityCount = []
    resultsCountryCount = []
    resultsKeywordCount = []
    resultsKeywordText = []

    FieldMetriks = [{'condition': charCountWhiteSpace, 'modelField': "charCountWhiteSpace"},
                    {'condition': charCountNoWhiteSpace, 'modelField': "charCountNoWhiteSpace"},
                    {'condition': wordCount, 'modelField': "wordCount"},
                    {'condition': punctCount, 'modelField': "punctCount"},
                    {'condition': citationCount, 'modelField': "citationCount"}]

    for paper in corpus:
        #Allgemeine Metriken
        #Kein Extraloop für alle drei mehr, oder?
        if authorCount or universityCount or countryCount:
            authors = paper.authors
            universities = []
            countries = []
            for author in authors:
                university = author.university
                if university:
                    if university not in universities:
                        universities.append(university)
                    country = university.country
                    if country:
                        countries.append(country)

            resultsAuthorCount.append(len(authors))
            resultsUniversityCount.append(len(universities))
            resultsCountryCount.append(len(countries))

        keywords = paper.metaData.keywords
        if keywordCount:
            resultsKeywordCount.append(len(keywords))
        if keywordFrequency:
            resultsKeywordText.append(keywords)

        if referenceCount:
            resultsReferenceCount.append(len(paper.references))

        #Feldmetriken Abstract
        abstract = corpus.abstract[0]
        abstractTitle = getattr(abstract, "title" + variant)
        abstractText = getattr(abstract, "text" + variant)
        for FieldMetrik in FieldMetriks:
            appendFieldMetrik(FieldMetrik['condition'], FieldMetrik['modelField'], abstracts, abstractTitle, abstractText)

        for sectionCount, section in enumerate(paper.content):
            if sectionCount == len(sections):
                sections.append(newMetriksDictionaire())
                subsections.append([])

            sectionTitle = getattr(section, "title" + variant)
            sectionText = getattr(section, "text" + variant)

            for FieldMetrik in FieldMetriks:
                appendFieldMetrik(FieldMetrik['condition'], FieldMetrik['modelField'], sections[sectionCount],
                                  sectionTitle, sectionText)

            tables = section.tables
            if tableCount:
                sections[sectionCount]['tableCount'].append(len(tables))
            if tableDescriptionCount:
                # TODO Juli hat den an " " gesplittet, hatte das nen Grund? len(table.tableDescription.split(' '))
                countTableDescription = []
                for table in tables:
                    countTableDescription.append(len(table.description))
                sections[sectionCount]['tableDescLengthCount'].append(countTableDescription)

            pictures = section.pictures
            if pictureCount:
                sections[sectionCount]['pictureCount'].append(len(pictures))
            if pictureDescriptionCount:
                # TODO Juli hat den an " " gesplittet, hatte das nen Grund? len(table.tableDescription.split(' '))
                countPictureDescription = []
                for picture in pictures:
                    countPictureDescription.append(len(picture.description))
                sections[sectionCount]['pictureDescLengthCount'].append(countPictureDescription)


            for subsectionCount, subsection in enumerate(section.subsection):
                if subsectionCount == len(subsections[sectionCount]):
                    subsections[sectionCount].append(newMetriksDictionaire())

                    subsectionTitle = getattr(subsection, "title" + variant)
                    subsectionText = getattr(subsection, "text" + variant)

                    for FieldMetrik in FieldMetriks:
                        appendFieldMetrik(FieldMetrik['condition'], FieldMetrik['modelField'], subsections[sectionCount][subsectionCount],
                                          subsectionTitle, subsectionText)
                    #TODO tables und pictures in subsections auch noch rein? NEIN

            #TODO statistische Werte mit Methode berechnen. results nach subsection/section oder nach Metriken gliedern?
            #Metrik charCountNhiteSpace
            abstracts = newMetriksDictionaire()
            # TODO Abstracts sind tatsächlich Liste
            print(sections)
            print(subsections)

            # TODO paper-title metriken
            print(resultsAuthorCount)
            print(resultsReferenceCount)
            print(resultsUniversityCount)
            print(resultsCountryCount)
            print(resultsKeywordCount)
            print(resultsKeywordText)
            results = {}
    return ""

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