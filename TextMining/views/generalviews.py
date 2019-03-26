# -*- coding: utf-8 -*-
# Create your views here.
from functools import reduce

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from TextMining.models import Paper, Metadata
import json
from django.shortcuts import redirect
from os import listdir, system
from os.path import join
from TextMining import metriken
from TextMining.saveFile import savePaper
from scipy import stats
import os

import TextMining.models
from mongoengine.queryset.visitor import Q
import numpy as np

# currentJsonfiles=[]

'''init ntlk run:
import nltk
nltk.download('stopwords')
'''


def helloWorld(request):
    return render(request, 'helloWorld.html')


def results(request):
    metricList = {"metrics": [{"metric": "authorsCount", "dataDisplayType": "numeric-total", "germanTitle": "Autorenanzahl"},
                              {"metric": "punctuationCount", "dataDisplayType": "numeric-section", "germanTitle": "Satzzeichenanzahl"},
                              {"metric": "referencesCount", "dataDisplayType": "numeric-total", "germanTitle": "Referenzenanzahl"},
                              {"metric": "characterCount", "dataDisplayType": "numeric-section", "germanTitle": "Zeichenanzahl"},
                              {"metric": "keywordDisplay", "dataDisplayType": "text-total", "germanTitle": "Keywords"},
                              {"metric": "mostfrequentWordsDisplay", "dataDisplayType": "text-section", "germanTitle": "Häufigste Wörter"}]}

    return render(request, 'results/results.html', metricList)


def corpusSelection(request):
    return render(request, 'corpusSelection/corpusSelection.html')


def readJsonFilesView(request):
    files = os.listdir('./static/uploadFiles')
    numberFiles = len(files)
    numPaper = Paper.objects.all().count()
    context = {'numberFiles': numberFiles, 'numberPaper': numPaper}
    return render(request, 'readJsonFiles.html', context)

def readJsonFiles(request):
    # loads all Json files....
    readpath = "./static/uploadFiles"
    onlyOne = False
    counter = 0
    for filename in listdir(readpath):
        if not onlyOne:
            if filename != ".DS_Store":  # file.endswith('.json')
                # print(filename)
                filepath = join(readpath, filename)
                file = open(filepath, 'r', encoding='utf-8', errors="ignore")
                paperJson = json.load(file)
                paper = savePaper(paperJson)
                counter += 1
                #TODO file.close dazu, geht unter mac auch noch?
                file.close()
                os.remove(filepath)
        onlyOne = False

    return JsonResponse({'sucess': 'Super!!!!!'})


def processPaperView(request):
    numberPaper = Paper.objects.all().count()
    context = {'numberPaper': numberPaper}
    return render(request, 'processPaper.html', context)


# Aufbereiten der Text Stopwortfiltern und lemmatisieren
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all()
    for paper in paperlist:
        print('Paper: ' + paper.titleRaw.text)
        metriken.removeStopwords(paper)  # MET_text_to_STOP_text
        metriken.stemText(paper)  # MET_text_to_STEM_text
        metriken.calculateAllMetrics(paper)

    print("Papersind aufbereitet und vorberechnet")
    return JsonResponse({'sucess': 'Super!!!!!'})

def getSelectedPaper(request):
    if(request.method=="POST"):
        #split requestdata
        corpus1 = {}
        corpus2 = {}
        querydata=request.POST
        for key in querydata:
            if 'CorpusID_1' in key:
                number = key.replace('_CorpusID_1', '').replace('optionfield_', '').replace('inputfield_', '')
                if not corpus1.get(number):
                    corpus1[number]={}
                if 'optionfield' in key:
                    corpus1[number]['optionfield'] = querydata[key]
                if 'inputfield' in key:
                    corpus1[number]['inputfield'] = querydata[key]
            if 'CorpusID_2' in key:
                number = key.replace('_CorpusID_2', '').replace('optionfield_', '').replace('inputfield_', '')
                if not corpus2.get(number):
                    corpus2[number] = {}
                if 'optionfield' in key:
                    corpus2[number]['optionfield'] = querydata[key]
                if 'inputfield' in key:
                    corpus2[number]['inputfield'] = querydata[key]
        #print('korpus1')
        #print(corpus1)
        #print('korpus2')
        #print(corpus2)
        #korpus1= {'2': {'optionfield': 'journal', 'inputfield': '1111'}, '1': {'optionfield': 'authors', 'inputfield': '1111'}}
        #korpus2= {'2': {'optionfield': 'journal', 'inputfield': '2222'}, '1': {'optionfield': 'authors', 'inputfield': '2222'}}

        ####### filterDBs
        paperCorpus1= filterDB(corpus1)
        paperCorpus2 = filterDB(corpus2)
        return JsonResponse({'sucess':True,'corpus1':paperCorpus1,'corpus2':paperCorpus2})

#http://docs.mongoengine.org/guide/querying.html
#https://stackoverflow.com/questions/8189702/mongodb-using-an-or-clause-in-mongoengine
def filterDB(querydata):
    if querydata:
        papers=Paper.objects.all()
        for number in querydata:
            query=querydata[number]
            field=query['optionfield']
            searchdata=query['inputfield']
            print('search for ' + field + " equals " + searchdata)
            #field='metaData__'+field+'__contains'
            #papers = papers.filter(** {field: searchdata})

            searchArry = searchdata.split(',')
            searchArry = [x.strip(' ') for x in searchArry]
            searchArry = list(filter(None, searchArry))
            print(searchArry)
            if searchArry:
                if field=='authors':
                    query = reduce(lambda q1, q2: q1.__or__(q2),map(lambda query: Q(authors__name__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field=='category':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__category__in=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__category__in=searchdata)
                if field=='organization':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__organization__icontains=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__organization__icontains=searchdata)
                if field=='keywords':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__keywords__in=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__keywords__in=searchdata)
                if field == 'journal':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__journal__icontains=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__journal__icontains=searchdata)
                if field=='source':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__source__icontains=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__source__icontains=searchdata)
                if field=='yearOfArticle':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__yearOfArticle__icontains=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__yearOfArticle__icontains=searchdata)
                if field=='language':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__language__icontains=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__language__icontains=searchdata)
                if field=='title':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__title__icontains=query), searchArry))
                    papers = papers.filter(query)
                    #papers = papers.filter(metaData__title__icontains=searchdata)
        ##nur titel und id....
        return papers.to_json()
    else:
        return ''

def startAnalyse(request):
    if(request.method=="POST"):
        print(request.POST)
        testvariante=request.POST.get('textVariante')
        if request.POST.get('Korpus1'):
            korpus1liste =request.POST.getlist('Korpus1')
            korpus1 = Paper.objects.filter(id__in=korpus1liste)
        else:
            korpus1 = None
        if request.POST.get('Korpus2'):
            korpus2liste = request.POST.getlist('Korpus1')
            korpus2 = Paper.objects.filter(id__in=korpus2liste)
        else:
            korpus2 = None

        analyse = analyseCorpora(testvariante, korpus1, korpus2, charCountWhiteSpace=True, charCountNoWhiteSpace=True,
                                 wordCount=True,
                                 punctCount=True, citationCount=True, authorCount=True, referenceCount=True,
                                 universityCount=True,
                                 countryCount=True, keywordCount=True, tableCount=True, pictureCount=True,
                                 tableDescriptionLengthCount=True, pictureDescriptionLengthCount=True,
                                 keywordFrequency=True)
        #print(analyse)

        metricList = {
            "metrics": [{"metric": "authorsCount", "dataDisplayType": "numeric-total", "germanTitle": "Autorenanzahl"},
                        {"metric": "punctuationCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Satzzeichenanzahl"},
                        {"metric": "referencesCount", "dataDisplayType": "numeric-total",
                         "germanTitle": "Referenzenanzahl"},
                        {"metric": "characterCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Zeichenanzahl"},
                        {"metric": "keywordDisplay", "dataDisplayType": "text-total", "germanTitle": "Keywords"},
                        {"metric": "mostfrequentWordsDisplay", "dataDisplayType": "text-section",
                         "germanTitle": "Häufigste Wörter"}]}

        return render(request, 'results/results.html', metricList)


# Testen obs klappt
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
    analyseCorpora('NltkStw', Paper.objects, Paper.objects, charCountWhiteSpace=True, charCountNoWhiteSpace=True, wordCount=True,
               punctCount=True, citationCount=True, authorCount=True, referenceCount=True, universityCount=True,
               countryCount=True, keywordCount=True, tableCount=True, pictureCount=True,
               tableDescriptionLengthCount=True, pictureDescriptionLengthCount=True, keywordFrequency=True)
    return render(request, 'index.html')

#TODO total und min max jetzt ints, rest float... außer mode, das ist array => so lasssen?
def getStatisticalValues(inputarray):
    if inputarray == [] or inputarray is None:
        total = None
        average = None
        modes = None
        variance = None
        lowerQuartile, median, upperQuartile = None, None, None
        min = None
        max = None
    else:
        total = int(np.sum(inputarray))
        average = float(np.mean(inputarray))
        mode = stats.mode(inputarray)
        modes = []
        for item in mode[0]:
            modes.append(int(item))
        variance = float(np.var(inputarray))
        lowerQuartile, median, upperQuartile = np.percentile(inputarray, [25, 50, 75])
        lowerQuartile = float(lowerQuartile)
        median = float(median)
        upperQuartile = float(upperQuartile)
        min = int(np.amin(inputarray))
        max = int(np.amax(inputarray))
        print(total)
        print(average)
        print(mode)
        print(modes)
        print(variance)
        print(lowerQuartile)
        print(median)
        print(upperQuartile)
        print(min)
        print(max)
    return {'total': total,'average': average, 'median': median, 'mode': modes,
            'variance': variance, 'lowerQuartile': lowerQuartile,
            'upperQuartile': upperQuartile, 'minimum': min, 'maximum': max}


#TODO durchschnittliche Wortlänge, durchschnittliche Satzlänge, häufigste Wörter, Most Present Words (TF), Häufigste Keywords, Readability
#TODO was gemeint mit Größe/Dichte Wortschatz, Anzahl Überschriften (=alle Titles? dann ja nur einfach alle Sektionen?)
#TODO die können alle über den Text berechnet werden => text raw in dict werfen?

#TODO Schauen welche Felder immer in db, und welche mit if abfragen? Alle Liste in db immer mit [] machen wenn leer? Metadata für jedes da? Keywords
#TODO wenn leer []? was wenn zb. Sektion keinen titel hat? None immer abfragen?
#TODO Die einzelnen ifs in den Schleifen raus und immer appenden? Performance dann besser oder nicht?

def createNewMetrikDict():
    return {'titles': [], 'totalContentTitles': [], 'totalContentText': [], 'abstractTitles': [], 'abstractText': [],
            'sectionTitles': [], 'sectionText': [], 'subsectionTitles': [], 'subsectionText': []}


def analyseCorpora(variant, corpus1, corpus2,charCountWhiteSpace=False, charCountNoWhiteSpace=False, wordCount=False,
               punctCount=False, citationCount=False, authorCount=False, referenceCount=False,
               universityCount=False,countryCount=False, keywordCount=False, tableCount=False, pictureCount=False,
               tableDescriptionLengthCount=False, pictureDescriptionLengthCount=False, keywordFrequency=False):
    if corpus1:
        metriks1 = getMetriks(corpus1, variant,charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
                   punctCount, citationCount, authorCount, referenceCount,
                   universityCount,countryCount, keywordCount, tableCount, pictureCount,
                   tableDescriptionLengthCount, pictureDescriptionLengthCount, keywordFrequency)
    else:
        metriks1 = None
    if corpus2:
        metriks2 = getMetriks(corpus2, variant,charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
                   punctCount, citationCount, authorCount, referenceCount,
                   universityCount,countryCount, keywordCount, tableCount, pictureCount,
                   tableDescriptionLengthCount, pictureDescriptionLengthCount, keywordFrequency)
    else:
        metriks2 = None
    results = {'Corpus1': metriks1, 'Corpus2': metriks2}
    print(json.dumps(results))
    #with open('data.txt', 'w') as outfile:
    #    json.dump(results, outfile)
    return json.dumps(results)


# TODO if Abfragen für existenz von Feldern
# TODO wenn Werte leeres Dict-... "0" bisher appendet!
# TODO werte auch in totalContent werfen
# TODO empty tag
def getMetriks(corpus, variant, charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
               punctCount, citationCount, authorCount, referenceCount,
               universityCount, countryCount, keywordCount, tableCount, pictureCount,
               tableDescriptionLengthCount, pictureDescriptionLengthCount, keywordFrequency):

    print('start!!!!!!!!')
    abstractHelper = []
    sectionHelper = []
    subsectionHelper = []

    resultsAuthorCount = []
    resultsReferenceCount = []
    resultsUniversityCount = []
    resultsCountryCount = []
    resultsKeywordCount = []
    #Enthält die keyword-liste aus den models, frequenz muss noch berechnet werden
    resultsKeywordText = []

    #liste für jede Sektion mit Werten Anzahl Tables/Pictures
    resultsTableCount = []
    resultsPictureCount = []
    #liste für jede Sektion mit Liste an Werten der Beschreibungslänge
    resultsTableDescLengthCount = []
    resultsPictureDescLengthCount = []

    FieldMetriks = [{'condition': charCountWhiteSpace, 'modelField': "charCountWhiteSpace", 'values': createNewMetrikDict()},
                    {'condition': charCountNoWhiteSpace, 'modelField': "charCountNoWhiteSpace", 'values': createNewMetrikDict()},
                    {'condition': wordCount, 'modelField': "wordCount", 'values': createNewMetrikDict()},
                    {'condition': punctCount, 'modelField': "punctCount", 'values': createNewMetrikDict()},
                    {'condition': citationCount, 'modelField': "citationCount", 'values': createNewMetrikDict()}]

    UsedFieldMetriks = []
    for possibleFieldMetrik in FieldMetriks:
        if possibleFieldMetrik['condition']:
            UsedFieldMetriks.append(possibleFieldMetrik)

    for paper in corpus:
        # Allgemeine Metriken
        # Kein Extraloop für alle drei mehr, oder?
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
                        if country not in countries:
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

        # Feldmetriken Titel
        paperTitle = getattr(paper, "title" + variant)
        if paperTitle:
            paperTitleMetrik = getattr(paperTitle, 'metrik')
            for fieldMetrik in UsedFieldMetriks:
        #TODO für jede Textvariante existieren Metriken immer, oder auch abfragen?
                fieldMetrik['values']['titles'].append(getattr(paperTitleMetrik, fieldMetrik['modelField']))


        # Feldmetriken Abstracts
        for abstractCount, abstract in enumerate(paper.abstract):
            if abstractCount == len(abstractHelper):
                abstractHelper.append([])
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['abstractTitles'].append([])
                    fieldMetrik['values']['abstractText'].append([])

            abstractTitle = getattr(abstract, "title" + variant)
            if abstractTitle:
                abstractTitleMetrik = getattr(abstractTitle, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['abstractTitles'][abstractCount].append(
                        getattr(abstractTitleMetrik, fieldMetrik['modelField']))
            abstractText = getattr(abstract, "text" + variant)
            if abstractText:
                abstractTextMetrik = getattr(abstractText, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['abstractText'][abstractCount].append(
                        getattr(abstractTextMetrik, fieldMetrik['modelField']))

        # Feldmetriken Sectionen und Subsectionen
        for sectionCount, section in enumerate(paper.content):
            if sectionCount == len(sectionHelper):
                sectionHelper.append([])
                subsectionHelper.append([])
                resultsTableCount.append([])
                resultsPictureCount.append([])
                resultsTableDescLengthCount.append([])
                resultsPictureDescLengthCount.append([])
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectionTitles'].append([])
                    fieldMetrik['values']['sectionText'].append([])
                    fieldMetrik['values']['subsectionTitles'].append([])
                    fieldMetrik['values']['subsectionText'].append([])

            sectionTitle = getattr(section, "title" + variant)
            if sectionTitle:
                sectionTitleMetrik = getattr(sectionTitle, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectionTitles'][sectionCount].append(
                        getattr(sectionTitleMetrik, fieldMetrik['modelField']))
            sectionText = getattr(section, "text" + variant)
            if sectionText:
                sectionTextMetrik = getattr(sectionText, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectionText'][sectionCount].append(
                        getattr(sectionTextMetrik, fieldMetrik['modelField']))

            tables = section.tables
            if tableCount:
                resultsTableCount[sectionCount].append(len(tables))
            if tableDescriptionLengthCount:
                # TODO Juli hat den an " " gesplittet, hatte das nen Grund? len(table.tableDescription.split(' '))
                countTableDescription = []
                for table in tables:
                    countTableDescription.append(len(table.description))
                resultsTableDescLengthCount[sectionCount].append(countTableDescription)

            pictures = section.pictures
            if pictureCount:
                resultsPictureCount[sectionCount].append(len(pictures))
            if pictureDescriptionLengthCount:
                # TODO Juli hat den an " " gesplittet, hatte das nen Grund? len(table.tableDescription.split(' '))
                countPictureDescription = []
                for picture in pictures:
                    countPictureDescription.append(len(picture.description))
                resultsPictureDescLengthCount[sectionCount].append(countPictureDescription)

            for subsectionCount, subsection in enumerate(section.subsection):
                if subsectionCount == len(subsectionHelper[sectionCount]):
                    subsectionHelper[sectionCount].append([])
                    for fieldMetrik in UsedFieldMetriks:
                        fieldMetrik['values']['subsectionTitles'][sectionCount].append([])
                        fieldMetrik['values']['subsectionText'][sectionCount].append([])

                    subsectionTitle = getattr(subsection, "title" + variant)
                    if subsectionTitle:
                        subsectionTitleMetrik = getattr(subsectionTitle, 'metrik')
                        for fieldMetrik in UsedFieldMetriks:
                            fieldMetrik['values']['subsectionTitles'][sectionCount][subsectionCount].append(
                                getattr(subsectionTitleMetrik, fieldMetrik['modelField']))
                    subsectionText = getattr(subsection, "text" + variant)
                    if subsectionText:
                        subsectionTextMetrik = getattr(subsectionText, 'metrik')
                        for fieldMetrik in UsedFieldMetriks:
                            fieldMetrik['values']['subsectionText'][sectionCount][subsectionCount].append(
                                getattr(subsectionTextMetrik, fieldMetrik['modelField']))

    results = {}
    if authorCount:
        results['authorCount'] = {'rawValues': resultsAuthorCount, 'statisticalValues': getStatisticalValues(resultsAuthorCount)}
    if referenceCount:
        results['referenceCount'] = {'rawValues': resultsReferenceCount, 'statisticalValues': getStatisticalValues(resultsReferenceCount)}
    if universityCount:
        results['universityCount'] = {'rawValues': resultsUniversityCount, 'statisticalValues': getStatisticalValues(resultsUniversityCount)}
    if countryCount:
        results['countryCount'] = {'rawValues': resultsCountryCount, 'statisticalValues': getStatisticalValues(resultsCountryCount)}
    if keywordCount:
        results['keywordCount'] = {'rawValues': resultsKeywordCount, 'statisticalValues': getStatisticalValues(resultsKeywordCount)}
    #TODO aus keyword-listen die tatsächliche Frequenz berechnen
    if keywordFrequency:
        results['keywordFrequency'] = resultsKeywordText
    if tableCount:
        #TableCount ist Liste an Sektionen, wird für statistische Werte zusammengefasst
        #TODO flat list auch mit übergeben?
        #TODO testen ob alle gehen
        #TODO erste Sektionen, zweite Sektionen etc auch?
        flatTableCount = [item for sublist in resultsTableCount for item in sublist]
        results['tableCount'] = {'rawValues': resultsTableCount,
                                 'statisticalValues': getStatisticalValues(flatTableCount)}
    if tableDescriptionLengthCount:
        flatTableDescriptionCount = [item for sublist in resultsTableDescLengthCount for subsublist in sublist for item in subsublist]
        results['tableDescriptionLengthCount'] = {'rawValues': resultsTableDescLengthCount,
                                                  'statisticalValues': getStatisticalValues(flatTableDescriptionCount)}
    if pictureCount:
        flatPictureCount = [item for sublist in resultsPictureCount for item in sublist]
        results['pictureCount'] = {'rawValues': resultsPictureCount,
                                   'statisticalValues': getStatisticalValues(flatPictureCount)}
    if pictureDescriptionLengthCount:
        flatTableDescriptionCount = [item for sublist in resultsPictureDescLengthCount for subsublist in sublist for item in subsublist]
        results['pictureDescriptionLengthCount'] = {'rawValues': resultsPictureDescLengthCount,
                                                    'statisticalValues': getStatisticalValues(flatTableDescriptionCount)}
    for fieldMetrik in UsedFieldMetriks:
        if fieldMetrik['modelField'] == 'charCountWhiteSpace' and charCountWhiteSpace:
            results['charCountWhiteSpace'] = {'rawValues': fieldMetrik['values'],
                                              'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values'])}

        if fieldMetrik['modelField'] == 'charCountNoWhiteSpace' and charCountNoWhiteSpace:
            results['charCountNoWhiteSpace'] = {'rawValues': fieldMetrik['values'],
                                                'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values'])}
        if fieldMetrik['modelField'] == 'wordCount' and wordCount:
            results['wordCount'] = {'rawValues': fieldMetrik['values'],
                                    'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values'])}
        if fieldMetrik['modelField'] == 'punctCount' and punctCount:
            results['punctCount'] = {'rawValues': fieldMetrik['values'],
                                     'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values'])}
        if fieldMetrik['modelField'] == 'citationCount' and citationCount:
            results['citationCount'] = {'rawValues': fieldMetrik['values'],
                                        'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values'])}

    return results


def getStatisticalValuesForFieldMetriks(input):
    flatAbstractTitles  = []
    flatAbstractText  = []
    flatSectionTitles  = []
    flatSectionText  = []
    flatSubsectionTitles = []
    flatSubsectionText = []
    flattenedSubsectionTitles = []
    flattenedSubsectionText = []

    resultsArrayAbstractTitles = []
    resultsArrayAbstractText = []
    resultsArraySectionTitles = []
    resultsArraySectionText = []
    resultsArraySubsectionTitles = []
    resultsArraySubsectionText = []

    for list in input['abstractTitles']:
        resultsArrayAbstractTitles.append(getStatisticalValues(list))
        for item in list:
            flatAbstractTitles.append(item)
    for list in input['abstractText']:
        resultsArrayAbstractText.append(getStatisticalValues(list))
        for item in list:
            flatAbstractText.append(item)
    for list in input['sectionTitles']:
        resultsArraySectionTitles.append(getStatisticalValues(list))
        for item in list:
            flatSectionTitles.append(item)
    for list in input['sectionText']:
        resultsArraySectionText.append(getStatisticalValues(list))
        for item in list:
            flatSectionText.append(item)
    #subsection titles
    totalSubsectionsForTitles = 0
    for list in input['subsectionTitles']:
        subsectionCount = len(list)
        if subsectionCount > totalSubsectionsForTitles:
            totalSubsectionsForTitles = subsectionCount
    for i in range(totalSubsectionsForTitles):
        flattenedSubsectionTitles.append([])
    for list in input['subsectionTitles']:
        for sublistCount, sublist in enumerate(list):
            for item in sublist:
                flatSubsectionTitles.append(item)
                flattenedSubsectionTitles[sublistCount].append(item)
    for list in flattenedSubsectionTitles:
        resultsArraySubsectionTitles.append(getStatisticalValues(list))
    #subscection text
    totalSubsectionsForText = 0
    for list in input['subsectionText']:
        subsectionCount = len(list)
        if subsectionCount > totalSubsectionsForText:
            totalSubsectionsForText = subsectionCount
    for i in range(totalSubsectionsForText):
        flattenedSubsectionText.append([])
    for list in input['subsectionText']:
        for sublistCount, sublist in enumerate(list):
            for item in sublist:
                flatSubsectionText.append(item)
                flattenedSubsectionText[sublistCount].append(item)
    for list in flattenedSubsectionText:
        resultsArraySubsectionText.append(getStatisticalValues(list))


    results =  {'totalTitles': getStatisticalValues(input['titles']),
            'totalAbstractTitles': getStatisticalValues(flatAbstractTitles), 'totalAbstractText': getStatisticalValues(flatAbstractText),
            'totalSectionTitles': getStatisticalValues(flatSectionTitles), 'totalSectionText': getStatisticalValues(flatSectionText),
            'totalSubsectionTitles': getStatisticalValues(flatSubsectionTitles), 'totalSubsectionText': getStatisticalValues(flatSubsectionText),
            'arrayAbstractTitles': resultsArrayAbstractTitles, 'arrayAbstractText': resultsArrayAbstractText,
            'arraySectionTitles': resultsArraySectionTitles, 'arraySectionText': resultsArraySectionText,
            'arraySubsectionTitles': resultsArraySubsectionTitles, 'arraySubsectionText': resultsArraySubsectionText}
    return results
