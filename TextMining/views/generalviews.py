# -*- coding: utf-8 -*-
# Create your views here.
from functools import reduce
from statistics import mean
from django.http import JsonResponse, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from collections import Counter

import nltk
from TextMining.models import Paper, Metadata
import json
from django.shortcuts import redirect
from os import listdir, system
from os.path import join
from TextMining import metriken
from TextMining.saveFile import savePaper
from scipy import stats
import os
import math

import TextMining.models
from mongoengine.queryset.visitor import Q
import numpy as np
import statistics

# currentJsonfiles=[]

'''init ntlk run:
import nltk
nltk.download('stopwords')
nltk.download('punkt')

'''
KORPUS1 = None
KORPUS2 = None


def redirect_view(request):
    return redirect('corpusSelection')


def results(request):
    metricList = {
        "metrics": [{"metric": "authorCount", "dataDisplayType": "numeric-total", "germanTitle": "Autorenanzahl"},
                    {"metric": "punctCount", "dataDisplayType": "numeric-section", "germanTitle": "Satzzeichenanzahl"},
                    {"metric": "referenceCount", "dataDisplayType": "numeric-total", "germanTitle": "Referenzenanzahl"},
                    {"metric": "charCountNoWhiteSpace", "dataDisplayType": "numeric-section", "germanTitle": "Zeichenanzahl"},
                    {"metric": "charCountWhiteSpace", "dataDisplayType": "numeric-section", "germanTitle": "Zeichenanzahl mit Leerzeichen"},
                    {"metric": "wordCount", "dataDisplayType": "numeric-section", "germanTitle": "Wortanzahl"},
                    {"metric": "citationCount", "dataDisplayType": "numeric-total", "germanTitle": "Anzahl der Zitate"},
                    {"metric": "universityCount", "dataDisplayType": "numeric-total", "germanTitle": "Anzahl beteiligter Universitäten"},
                    {"metric": "countryCount", "dataDisplayType": "numeric-total", "germanTitle": "Anzahl beteiligter Länder"},
                    {"metric": "keywordCount", "dataDisplayType": "numeric-total", "germanTitle": "Keywordanzahl"},
                    {"metric": "tableCount", "dataDisplayType": "numeric-total", "germanTitle": "Tabellenanzahl"},
                    {"metric": "pictureCount", "dataDisplayType": "numeric-total", "germanTitle": "Bilderanzahl"},
                    {"metric": "tableDescriptionLengthCount", "dataDisplayType": "numeric-total", "germanTitle": "Tabellenbeschriftungslängen"},
                    {"metric": "pictureDescriptionLengthCount", "dataDisplayType": "numeric-total", "germanTitle": "Bildbeschriftungslängen"},
                    {"metric": "keywordFrequency", "dataDisplayType": "numeric-total", "germanTitle": "Keywordauftreten"},
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
                # TODO file.close dazu, geht unter mac auch noch?
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

    print("Paper sind aufbereitet und vorberechnet")
    return JsonResponse({'sucess': 'Super!!!!!'})


def getSelectedPaper(request):
    if (request.method == "POST"):
        # split requestdata
        corpus1 = {}
        corpus2 = {}
        querydata = request.POST
        print(querydata)
        for key in querydata:
            if 'CorpusID_1' in key and not 'textVarSelect' in key:
                number = key.replace('_CorpusID_1', '').replace('optionfield_', '').replace('inputfield_', '')
                if not corpus1.get(number):
                    corpus1[number] = {}
                if 'optionfield' in key:
                    corpus1[number]['optionfield'] = querydata[key]
                if 'inputfield' in key:
                    corpus1[number]['inputfield'] = querydata[key]
            if 'CorpusID_2' in key and not 'textVarSelect' in key:
                number = key.replace('_CorpusID_2', '').replace('optionfield_', '').replace('inputfield_', '')
                if not corpus2.get(number):
                    corpus2[number] = {}
                if 'optionfield' in key:
                    corpus2[number]['optionfield'] = querydata[key]
                if 'inputfield' in key:
                    corpus2[number]['inputfield'] = querydata[key]
        print(corpus1)
        print(corpus2)
        ####### filterDBs
        paperCorpus1 = filterDB(corpus1)
        paperCorpus2 = filterDB(corpus2)
        return JsonResponse({'sucess': True, 'corpus1': paperCorpus1, 'corpus2': paperCorpus2})

    if (request.method == "GET"):
        return redirect('corpusSelection')


# http://docs.mongoengine.org/guide/querying.html
# https://stackoverflow.com/questions/8189702/mongodb-using-an-or-clause-in-mongoengine
def filterDB(querydata):
    if querydata:
        papers = Paper.objects.all()
        for number in querydata:
            query = querydata[number]
            field = query['optionfield']
            searchdata = query['inputfield']
            print('search for ' + field + " equals " + searchdata)
            # field='metaData__'+field+'__contains'
            # papers = papers.filter(** {field: searchdata})

            searchArry = searchdata.split(',')
            searchArry = [x.strip(' ') for x in searchArry]
            searchArry = list(filter(None, searchArry))
            print(searchArry)
            if searchArry:
                if field == 'authors':
                    query = reduce(lambda q1, q2: q1.__or__(q2), map(lambda query: Q(authors__name__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'category':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__category__in=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__category__in=searchdata)
                if field == 'organization':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__organization__icontains=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__organization__icontains=searchdata)
                if field == 'keywords':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__keywords__in=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__keywords__in=searchdata)
                if field == 'journal':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__journal__icontains=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__journal__icontains=searchdata)
                if field == 'source':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__source__icontains=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__source__icontains=searchdata)
                if field == 'yearOfArticle':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__yearOfArticle__icontains=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__yearOfArticle__icontains=searchdata)
                if field == 'language':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__language__icontains=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__language__icontains=searchdata)
                if field == 'title':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__title__icontains=query), searchArry))
                    papers = papers.filter(query)
                    # papers = papers.filter(metaData__title__icontains=searchdata)
        ##nur titel und id....
        return papers.to_json()
    else:
        return ''


def startAnalyse(request):
    if (request.method == "POST"):
        print(request.POST)
        global KORPUS1
        global KORPUS2
        if request.POST.get('Korpus1'):
            varianteKorpus1 = request.POST.get('Korpus1_textVariante')
            korpus1liste = request.POST.getlist('Korpus1')
            KORPUS1 = Paper.objects.filter(id__in=korpus1liste)
        else:
            varianteKorpus1 = None
            KORPUS1 = None
        if request.POST.get('Korpus2'):
            varianteKorpus2 = request.POST.get('Korpus2_textVariante')
            korpus2liste = request.POST.getlist('Korpus2')
            KORPUS2 = Paper.objects.filter(id__in=korpus2liste)
        else:
            KORPUS2 = None
            varianteKorpus2 = None

        metricList = {
            "metrics": [{"metric": "authorCount", "dataDisplayType": "numeric-total", "germanTitle": "Autorenanzahl", "graphType": "boxplot", "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "typeTokenRatio", "dataDisplayType": "numeric-total", "germanTitle": "Type-Toke-Ratio", "graphType": "boxplot", "allowTextVariants": "true",
                         "foundation": "document"},
                        {"metric": "referenceCount", "dataDisplayType": "numeric-total", "germanTitle": "Referenzenanzahl", "graphType": "boxplot", "allowTextVariants": "false",
                         "foundation": "document"},
                        {"metric": "universityCount", "dataDisplayType": "numeric-total", "germanTitle": "Anzahl beteiligter Universitäten", "graphType": "boxplot", "allowTextVariants": "false",
                         "foundation": "document"},
                        {"metric": "countryCount", "dataDisplayType": "numeric-total", "germanTitle": "Anzahl beteiligter Länder", "graphType": "boxplot", "allowTextVariants": "false",
                         "foundation": "document"},
                        {"metric": "keywordCount", "dataDisplayType": "numeric-total", "germanTitle": "Keywordanzahl", "graphType": "boxplot", "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "charCountNoWhiteSpace", "dataDisplayType": "numeric-section", "germanTitle": "Zeichenanzahl ohne Leerzeichen", "graphType": "boxplot", "allowTextVariants": "true",
                         "foundation": "document"},
                        {"metric": "charCountWhiteSpace", "dataDisplayType": "numeric-section", "germanTitle": "Zeichenanzahl mit Leerzeichen", "graphType": "boxplot", "allowTextVariants": "true",
                         "foundation": "document"},
                        {"metric": "wordCount", "dataDisplayType": "numeric-section", "germanTitle": "Wortanzahl", "graphType": "boxplot", "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "punctCount", "dataDisplayType": "numeric-section", "germanTitle": "Satzzeichenanzahl", "graphType": "boxplot", "allowTextVariants": "true",
                         "foundation": "document"},
                        {"metric": "citationCount", "dataDisplayType": "numeric-section", "germanTitle": "Anzahl der Zitate", "graphType": "boxplot", "allowTextVariants": "true",
                         "foundation": "document"},
                        {"metric": "tableCount", "dataDisplayType": "numeric-section", "germanTitle": "Tabellenanzahl", "graphType": "boxplot", "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "pictureCount", "dataDisplayType": "numeric-section", "germanTitle": "Bilderanzahl", "graphType": "boxplot", "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "tableDescriptionLengthCount", "dataDisplayType": "numeric-section", "germanTitle": "Durchschnittliche Tabellenbeschriftungslängen", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "pictureDescriptionLengthCount", "dataDisplayType": "numeric-section", "germanTitle": "Durchschnittliche Bildbeschriftungslängen", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "averageWordLength", "dataDisplayType": "numeric-section", "germanTitle": "Durchschnittliche Wortlänge", "graphType": "boxplot", "allowTextVariants": "true",
                         "foundation": "document"},
                        {"metric": "averageSentenceLength", "dataDisplayType": "numeric-section", "germanTitle": "Durchschnittliche Satzlänge", "graphType": "boxplot", "allowTextVariants": "true",
                         "foundation": "document"},
                        {"metric": "mostCommonKeywords", "dataDisplayType": "text-total", "germanTitle": "Häufigste Keywords", "graphType": "wordcloud", "allowTextVariants": "false",
                         "foundation": "corpus"},
                        {"metric": "mostCommonWords", "dataDisplayType": "text-total", "germanTitle": "Häufigste Wörter", "graphType": "lollipop", "allowTextVariants": "true", "foundation": "corpus"},
                        {"metric": "mostPresentWords", "dataDisplayType": "text-total", "germanTitle": "Häufigst anwesende Wörter", "graphType": "lollipop", "allowTextVariants": "true",
                         "foundation": "corpus"},
                        ]}

        corpusTextVariants = {"Korpus1": varianteKorpus1, "Korpus2": varianteKorpus2}
        context = {'metricList': metricList, 'corpusTextVariants': corpusTextVariants}
        return render(request, 'results/results.html', context)

    if (request.method == "GET"):
        return redirect('corpusSelection')


# Testen obs klappt
def startDB(request):
    system('mongod')


def downloadResults(request, Corpus):
    if request.method == 'GET':
        global KORPUS1
        global KORPUS2
        korpusname = Corpus
        if korpusname == 'Korpus1':
            response = KORPUS1.to_json()
        elif korpusname == 'Korpus2':
            response = KORPUS2.to_json()
        else:
            response = {'fehler': 'Fehler aufgetreten'}
        response = HttpResponse(response, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="' + korpusname + '.json"'
        return response


def calculateMetrik(request):
    if request.method == "GET":
        print(request.GET)
        fieldname = request.GET.get('fieldname')
        variante1 = request.GET.get('Korpus1_variante')
        variante2 = request.GET.get('Korpus2_variante')
        print('fieldname:' + fieldname)
        if fieldname:
            bool = True
            response = analyseCorpora(variante1, variante2, KORPUS1, KORPUS2, **{fieldname: bool})
        return JsonResponse(response, safe=False)


# TODO brauchen wir so sachen wie distinct über alle, oder sowas wie wieviel Paper pro Uni oder nicht?
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
    print(analyseCorpora('Raw', 'Raw', Paper.objects.all(), Paper.objects.all(), charCountWhiteSpace=False, charCountNoWhiteSpace=False,
                         wordCount=False, punctCount=False, citationCount=False, authorCount=False, referenceCount=False,
                         universityCount=False, countryCount=False, keywordCount=False, tableCount=False,
                         pictureCount=False, tableDescriptionLengthCount=False, pictureDescriptionLengthCount=False,
                         averageWordLength=False, averageSentenceLength=False, mostCommonWords=False,
                         mostCommonKeywords=True, mostPresentWords=False, typeTokenRatio=False))
    return render(request, 'index.html')


def getStatisticalValues(inputarray):
    if inputarray == [] or inputarray is None:
        sum = None
        average = None
        modes = None
        variance = None
        lowerQuartile, median, upperQuartile = None, None, None
        min = None
        max = None
        count = 0
        std = None
    else:
        inputarray = [entry['value'] for entry in inputarray]
        sum = float(np.sum(inputarray))
        average = float(np.mean(inputarray))
        mode = stats.mode(inputarray, axis=None)
        modes = []
        for item in mode[0]:
            modes.append(float(item))
        variance = float(np.var(inputarray))
        lowerQuartile, median, upperQuartile = np.percentile(inputarray, [25, 50, 75])
        lowerQuartile = float(lowerQuartile)
        median = float(median)
        upperQuartile = float(upperQuartile)
        min = float(np.amin(inputarray))
        max = float(np.amax(inputarray))
        count = len(inputarray)
        std = math.sqrt(variance)
    return {'sum': sum, 'average': average, 'median': median, 'mode': modes,
            'variance': variance, 'lowerQuartile': lowerQuartile,
            'upperQuartile': upperQuartile, 'minimum': min, 'maximum': max, 'count': count, 'std': std}


# TODO durchschnittliche Wortlänge, durchschnittliche Satzlänge, häufigste Wörter, Most Present Words (TF), Häufigste Keywords, Readability, TTR
def createNewValueAndPaperDict(value, paper):
    return {'value': value, 'name': paper.titleRaw.text, 'authors': [author.name for author in paper.authors],
            'year': paper.metaData.yearOfArticle, 'paperID': str(paper.id)}


def createNewValueAndWordDict(value, word):
    return {'value': value, 'name': word}


def createNewMetrikDict():
    totals = {'paperTitles': [], 'paperText': [], 'abstractTitles': [], 'abstractText': [],
              'sectionTitles': [], 'sectionText': [], 'subsectionTitles': [], 'subsectionText': []}
    sectioned = {'abstractTitles': [], 'abstractText': [],
                 'sectionTitles': [], 'sectionText': [], 'subsectionTitles': [], 'subsectionText': []}
    return {'totals': totals, 'sectioned': sectioned}


# Tables und Pictures sind nur für jede Sektion gespeichert, und daher eine "abgespeckte" Variante der FieldMetriks ohne
# Abstracts und Subsections sowie ohne Titel
def createNewTableOrPicturesMetrikDict():
    totals = {'sectionText': []}
    sectioned = {'sectionText': []}
    return {'totals': totals, 'sectioned': sectioned}


def analyseCorpora(variant1, variant2, corpus1, corpus2, charCountWhiteSpace=False, charCountNoWhiteSpace=False, wordCount=False,
                   punctCount=False, citationCount=False, authorCount=False, referenceCount=False,
                   universityCount=False, countryCount=False, keywordCount=False, tableCount=False, pictureCount=False,
                   tableDescriptionLengthCount=False, pictureDescriptionLengthCount=False,
                   averageWordLength=False, averageSentenceLength=False, mostCommonWords=False, mostCommonKeywords=False,
                   mostPresentWords=False, typeTokenRatio=False):
    sectionedMetriks = {('charCountWhiteSpace', charCountWhiteSpace), ('charCountNoWhiteSpace', charCountNoWhiteSpace),
                        ('wordCount', wordCount), ('punctCount', punctCount), ('citationCount', citationCount),
                        ('averageWordLength', averageWordLength), ('averageSentenceLength', averageSentenceLength)}
    sectionedParts = {'abstractTitles', 'abstractText', 'sectionTitles', 'sectionText', 'subsectionTitles', 'subsectionText'}

    # Tables und Pictures werden nur für Sektionen erfasst, und dort nur im Text => abgespeckte Variante der sectionedMetriks
    partiallySectionedMetriks = {('tableCount', tableCount), ('pictureCount', pictureCount),
                                 ('tableDescriptionLengthCount', tableDescriptionLengthCount),
                                 ('pictureDescriptionLengthCount', pictureDescriptionLengthCount)}

    valueParts = {'rawValues', 'statisticalValues'}

    results = {}
    if charCountWhiteSpace:
        results['charCountWhiteSpace'] = {}
    if charCountNoWhiteSpace:
        results['charCountNoWhiteSpace'] = {}
    if wordCount:
        results['wordCount'] = {}
    if punctCount:
        results['punctCount'] = {}
    if citationCount:
        results['citationCount'] = {}
    if authorCount:
        results['authorCount'] = {}
    if referenceCount:
        results['referenceCount'] = {}
    if universityCount:
        results['universityCount'] = {}
    if countryCount:
        results['countryCount'] = {}
    if keywordCount:
        results['keywordCount'] = {}
    if tableCount:
        results['tableCount'] = {}
    if pictureCount:
        results['pictureCount'] = {}
    if tableDescriptionLengthCount:
        results['tableDescriptionLengthCount'] = {}
    if pictureDescriptionLengthCount:
        results['pictureDescriptionLengthCount'] = {}
    if averageWordLength:
        results['averageWordLength'] = {}
    if averageSentenceLength:
        results['averageSentenceLength'] = {}
    if mostCommonWords:
        results['mostCommonWords'] = {}
    if mostCommonKeywords:
        results['mostCommonKeywords'] = {}
    if mostPresentWords:
        results['mostPresentWords'] = {}
    if typeTokenRatio:
        results['typeTokenRatio'] = {}

    if corpus1:
        corpusIdentifier = "Corpus1"
        results = getMetriks(corpus1, variant1, corpusIdentifier, results, charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
                             punctCount, citationCount, authorCount, referenceCount,
                             universityCount, countryCount, keywordCount, tableCount, pictureCount,
                             tableDescriptionLengthCount, pictureDescriptionLengthCount,
                             averageWordLength, averageSentenceLength, mostCommonWords, mostCommonKeywords,
                             mostPresentWords, typeTokenRatio)

    if corpus2:
        corpusIdentifier = "Corpus2"
        results = getMetriks(corpus2, variant2, corpusIdentifier, results, charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
                             punctCount, citationCount, authorCount, referenceCount,
                             universityCount, countryCount, keywordCount, tableCount, pictureCount,
                             tableDescriptionLengthCount, pictureDescriptionLengthCount,
                             averageWordLength, averageSentenceLength, mostCommonWords, mostCommonKeywords,
                             mostPresentWords, typeTokenRatio)
        # Gleicht Länge der Ausgabe bei 2 Corpora aneinander an
        for metrik in sectionedMetriks:
            if metrik[1]:
                for part in sectionedParts:
                    for valuePart in valueParts:
                        while len(results[metrik[0]]['Corpus1'][valuePart]['sectioned'][part]) < \
                                len(results[metrik[0]]['Corpus2'][valuePart]['sectioned'][part]):
                            results[metrik[0]]['Corpus1'][valuePart]['sectioned'][part].append([])
                        while len(results[metrik[0]]['Corpus2'][valuePart]['sectioned'][part]) < \
                                len(results[metrik[0]]['Corpus1'][valuePart]['sectioned'][part]):
                            results[metrik[0]]['Corpus2'][valuePart]['sectioned'][part].append([])
        ##Gleicht Länge der Ausgabe bei 2 Corpora aneinander an
        for metrik in partiallySectionedMetriks:
            if metrik[1]:
                for valuePart in valueParts:
                    while len(results[metrik[0]]['Corpus1'][valuePart]['sectioned']['sectionText']) < \
                            len(results[metrik[0]]['Corpus2'][valuePart]['sectioned']['sectionText']):
                        results[metrik[0]]['Corpus1'][valuePart]['sectioned']['sectionText'].append([])
                    while len(results[metrik[0]]['Corpus2'][valuePart]['sectioned']['sectionText']) < \
                            len(results[metrik[0]]['Corpus1'][valuePart]['sectioned']['sectionText']):
                        results[metrik[0]]['Corpus2'][valuePart]['sectioned']['sectionText'].append([])
    with open('data.txt', 'w') as outfile:
        json.dump(results, outfile)
    return json.dumps(results)


# TODO raw values wie autoren mit rawValues : [{'wort': x, 'Häufigkeit':y},{...}] siehe mail
def getMetriks(corpus, variant, corpusIdentifier, resultDict, charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
               punctCount, citationCount, authorCount, referenceCount,
               universityCount, countryCount, keywordCount, tableCount, pictureCount,
               tableDescriptionLengthCount, pictureDescriptionLengthCount,
               averageWordLength, averageSentenceLength, mostCommonWords, mostCommonKeywords,
               mostPresentWords, typeTokenRatio):
    abstractHelper = []
    sectionHelper = []
    subsectionHelper = []

    resultsAuthorCount = []
    resultsReferenceCount = []
    resultsUniversityCount = []
    resultsCountryCount = []
    resultsKeywordCount = []

    paperContents = []
    keywordContents = []
    nonWords = ['.', ',', '\\', '/', '#', '!', '?', '^', '&', '*', ';', ':', '{', '}', '=', '-', '_', '`', '~',
                '“', '”', '"', '(', ')', "'", '""', "''", '<', '>', '[', ']', ' ', '%', '&', '§', "’"]

    resultsMostCommonWords = []
    resultsMostCommonKeywords = []
    resultsMostPresentWords = []
    resultsTypeTokenRatio = []

    # liste für jede Sektion mit Werten Anzahl Tables/Pictures
    resultsTableCount = createNewTableOrPicturesMetrikDict()
    resultsPictureCount = createNewTableOrPicturesMetrikDict()
    # liste für jede Sektion mit Liste an Werten der Beschreibungslänge
    resultsTableDescLengthCount = createNewTableOrPicturesMetrikDict()
    resultsPictureDescLengthCount = createNewTableOrPicturesMetrikDict()

    # normale (Count)-Metriken, deren durchschnittlicher Wert in allen Sektionen
    # aus den Werten der einzelnen Sektionen berechnet werden kann
    FieldMetriks = [{'condition': charCountWhiteSpace, 'modelField': "charCountWhiteSpace", 'values': createNewMetrikDict()},
                    {'condition': charCountNoWhiteSpace, 'modelField': "charCountNoWhiteSpace", 'values': createNewMetrikDict()},
                    {'condition': wordCount, 'modelField': "wordCount", 'values': createNewMetrikDict()},
                    {'condition': punctCount, 'modelField': "punctCount", 'values': createNewMetrikDict()},
                    {'condition': citationCount, 'modelField': "citationCount", 'values': createNewMetrikDict()}]

    # Durchschnittsmetriken, deren durchschnittlicher Wert in allen Sektionen
    # nicht aus den Werten der einzelnen Sektionen berechnet werden kann und deshalb aus der db kommt
    FieldMetriksWithTotalsInDB = [
        {'condition': averageWordLength, 'modelField': "averageWordLength",
         'values': createNewMetrikDict(), 'totalsDBField': 'totalsAverageWordLength'},
        {'condition': averageSentenceLength, 'modelField': "averageSentenceLength",
         'values': createNewMetrikDict(), 'totalsDBField': 'totalsAverageSentenceLength'}]

    UsedFieldMetriks = []
    for possibleFieldMetrik in FieldMetriks:
        if possibleFieldMetrik['condition']:
            UsedFieldMetriks.append(possibleFieldMetrik)

    UsedFieldMetriksWithTotalsInDB = []
    for possibleFieldMetrik in FieldMetriksWithTotalsInDB:
        if possibleFieldMetrik['condition']:
            UsedFieldMetriksWithTotalsInDB.append(possibleFieldMetrik)

    if mostCommonWords or mostPresentWords or typeTokenRatio:
        textualMetriks = True
    else:
        textualMetriks = False

    for paper in corpus:
        # Helper zum berechnen des gesamten durchschnitts für sektionierte Metriken
        totalHelperSectionTitles = {}
        totalHelperSectionText = {}
        totalHelperSubsectionTitles = {}
        totalHelperSubsectionText = {}
        totalHelperAbstractTitles = {}
        totalHelperAbstractText = {}
        totalHelperTableCount = []
        totalHelperPictureCount = []
        totalHelperTableDescCount = []
        totalHelperPictureDescCount = []
        # Gesamter Text des Papers zum berechnen der häufigsten Wörter, Most Present Words, TTR
        paperContent = ""

        # Allgemeine Metriken, bezogen auf ganzes Paper
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

            resultsAuthorCount.append(createNewValueAndPaperDict(len(authors), paper))
            resultsUniversityCount.append(createNewValueAndPaperDict(len(universities), paper))
            resultsCountryCount.append(createNewValueAndPaperDict(len(countries), paper))

        keywords = paper.metaData.keywords
        if keywordCount:
            resultsKeywordCount.append(createNewValueAndPaperDict(len(keywords), paper))
        if mostCommonKeywords:
            for keyword in keywords:
                keywordContents.append(keyword)

        if referenceCount:
            resultsReferenceCount.append(createNewValueAndPaperDict(len(paper.references), paper))

        paperTitle = getattr(paper, "title" + variant)
        if paperTitle:
            paperTitleMetrik = getattr(paperTitle, 'metrik')
            for fieldMetrik in UsedFieldMetriks:
                fieldMetrik['values']['totals']['paperTitles'].append(createNewValueAndPaperDict(
                    getattr(paperTitleMetrik, fieldMetrik['modelField']), paper))
            for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                fieldMetrik['values']['totals']['paperTitles'].append(createNewValueAndPaperDict(
                    getattr(paperTitleMetrik, fieldMetrik['modelField']), paper))
            if textualMetriks:
                paperContent = paperContent + " " + paperTitle.text

        for fieldMetrik in UsedFieldMetriks:
            totalHelperAbstractTitles[fieldMetrik['modelField']] = []
            totalHelperAbstractText[fieldMetrik['modelField']] = []
            totalHelperSectionTitles[fieldMetrik['modelField']] = []
            totalHelperSectionText[fieldMetrik['modelField']] = []
            totalHelperSubsectionTitles[fieldMetrik['modelField']] = []
            totalHelperSubsectionText[fieldMetrik['modelField']] = []

        for abstractCount, abstract in enumerate(paper.abstract):
            if abstractCount == len(abstractHelper):
                abstractHelper.append([])
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectioned']['abstractTitles'].append([])
                    fieldMetrik['values']['sectioned']['abstractText'].append([])
                for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                    fieldMetrik['values']['sectioned']['abstractTitles'].append([])
                    fieldMetrik['values']['sectioned']['abstractText'].append([])

            abstractTitle = getattr(abstract, "title" + variant)
            if abstractTitle:
                abstractTitleMetrik = getattr(abstractTitle, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectioned']['abstractTitles'][abstractCount].append(createNewValueAndPaperDict(
                        getattr(abstractTitleMetrik, fieldMetrik['modelField']), paper))
                    totalHelperAbstractTitles[fieldMetrik['modelField']].append(
                        getattr(abstractTitleMetrik, fieldMetrik['modelField']))
                for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                    fieldMetrik['values']['sectioned']['abstractTitles'][abstractCount].append(createNewValueAndPaperDict(
                        getattr(abstractTitleMetrik, fieldMetrik['modelField']), paper))
                if textualMetriks:
                    paperContent = paperContent + " " + abstractTitle.text

            abstractText = getattr(abstract, "text" + variant)
            if abstractText:
                abstractTextMetrik = getattr(abstractText, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectioned']['abstractText'][abstractCount].append(createNewValueAndPaperDict(
                        getattr(abstractTextMetrik, fieldMetrik['modelField']), paper))
                    totalHelperAbstractText[fieldMetrik['modelField']].append(
                        getattr(abstractTextMetrik, fieldMetrik['modelField']))
                for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                    fieldMetrik['values']['sectioned']['abstractText'][abstractCount].append(createNewValueAndPaperDict(
                        getattr(abstractTextMetrik, fieldMetrik['modelField']), paper))
                if textualMetriks:
                    paperContent = paperContent + " " + abstractText.text

        for sectionCount, section in enumerate(paper.content):
            if sectionCount == len(sectionHelper):
                sectionHelper.append([])
                resultsTableCount['sectioned']['sectionText'].append([])
                resultsPictureCount['sectioned']['sectionText'].append([])
                resultsTableDescLengthCount['sectioned']['sectionText'].append([])
                resultsPictureDescLengthCount['sectioned']['sectionText'].append([])
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectioned']['sectionTitles'].append([])
                    fieldMetrik['values']['sectioned']['sectionText'].append([])
                for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                    fieldMetrik['values']['sectioned']['sectionTitles'].append([])
                    fieldMetrik['values']['sectioned']['sectionText'].append([])

            sectionTitle = getattr(section, "title" + variant)
            if sectionTitle:
                sectionTitleMetrik = getattr(sectionTitle, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectioned']['sectionTitles'][sectionCount].append(createNewValueAndPaperDict(
                        getattr(sectionTitleMetrik, fieldMetrik['modelField']), paper))
                    totalHelperSectionTitles[fieldMetrik['modelField']].append(
                        getattr(sectionTitleMetrik, fieldMetrik['modelField']))
                for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                    fieldMetrik['values']['sectioned']['sectionTitles'][sectionCount].append(createNewValueAndPaperDict(
                        getattr(sectionTitleMetrik, fieldMetrik['modelField']), paper))
                if textualMetriks:
                    paperContent = paperContent + " " + sectionTitle.text

            sectionText = getattr(section, "text" + variant)
            if sectionText:
                sectionTextMetrik = getattr(sectionText, 'metrik')
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['sectioned']['sectionText'][sectionCount].append(createNewValueAndPaperDict(
                        getattr(sectionTextMetrik, fieldMetrik['modelField']), paper))
                    totalHelperSectionText[fieldMetrik['modelField']].append(
                        getattr(sectionTextMetrik, fieldMetrik['modelField']))
                for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                    fieldMetrik['values']['sectioned']['sectionText'][sectionCount].append(createNewValueAndPaperDict(
                        getattr(sectionTextMetrik, fieldMetrik['modelField']), paper))
                if textualMetriks:
                    paperContent = paperContent + " " + sectionText.text

            tables = section.tables
            if tableCount:
                resultsTableCount['sectioned']['sectionText'][sectionCount].append(createNewValueAndPaperDict(
                    len(tables), paper))
                totalHelperTableCount.append(len(tables))
            if tableDescriptionLengthCount:
                # TODO Juli hat den an " " gesplittet, hatte das nen Grund? len(table.tableDescription.split(' '))
                countTableDescription = []
                for table in tables:
                    countTableDescription.append(len(table.description))
                    totalHelperTableDescCount.append(len(table.description))
                if countTableDescription != []:
                    resultsTableDescLengthCount['sectioned']['sectionText'][sectionCount].append(createNewValueAndPaperDict(
                        statistics.mean(countTableDescription), paper))

            pictures = section.pictures
            if pictureCount:
                resultsPictureCount['sectioned']['sectionText'][sectionCount].append(createNewValueAndPaperDict(len(pictures),
                                                                                                                paper))
                totalHelperPictureCount.append(len(pictures))
            if pictureDescriptionLengthCount:
                # TODO Juli hat den an " " gesplittet, hatte das nen Grund? len(table.tableDescription.split(' '))
                countPictureDescription = []
                for picture in pictures:
                    countPictureDescription.append(len(picture.description))
                    totalHelperPictureDescCount.append(len(picture.description))
                if countPictureDescription != []:
                    resultsPictureDescLengthCount['sectioned']['sectionText'][sectionCount].append(
                        createNewValueAndPaperDict(statistics.mean(countPictureDescription), paper))

            for subsectionCount, subsection in enumerate(section.subsection):
                if subsectionCount == len(subsectionHelper):
                    subsectionHelper.append([])
                    for fieldMetrik in UsedFieldMetriks:
                        fieldMetrik['values']['sectioned']['subsectionTitles'].append([])
                        fieldMetrik['values']['sectioned']['subsectionText'].append([])
                    for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                        fieldMetrik['values']['sectioned']['subsectionTitles'].append([])
                        fieldMetrik['values']['sectioned']['subsectionText'].append([])

                subsectionTitle = getattr(subsection, "title" + variant)
                if subsectionTitle:
                    subsectionTitleMetrik = getattr(subsectionTitle, 'metrik')
                    for fieldMetrik in UsedFieldMetriks:
                        fieldMetrik['values']['sectioned']['subsectionTitles'][subsectionCount].append(createNewValueAndPaperDict(
                            getattr(subsectionTitleMetrik, fieldMetrik['modelField']), paper))
                        totalHelperSubsectionTitles[fieldMetrik['modelField']].append(
                            getattr(subsectionTitleMetrik, fieldMetrik['modelField']))
                    for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                        fieldMetrik['values']['sectioned']['subsectionTitles'][subsectionCount].append(createNewValueAndPaperDict(
                            getattr(subsectionTitleMetrik, fieldMetrik['modelField']), paper))
                    if textualMetriks:
                        paperContent = paperContent + " " + subsectionTitle.text

                subsectionText = getattr(subsection, "text" + variant)
                if subsectionText:
                    subsectionTextMetrik = getattr(subsectionText, 'metrik')
                    for fieldMetrik in UsedFieldMetriks:
                        fieldMetrik['values']['sectioned']['subsectionText'][subsectionCount].append(createNewValueAndPaperDict(
                            getattr(subsectionTextMetrik, fieldMetrik['modelField']), paper))
                        totalHelperSubsectionText[fieldMetrik['modelField']].append(
                            getattr(subsectionTextMetrik, fieldMetrik['modelField']))
                    for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
                        fieldMetrik['values']['sectioned']['subsectionText'][subsectionCount].append(createNewValueAndPaperDict(
                            getattr(subsectionTextMetrik, fieldMetrik['modelField']), paper))
                    if textualMetriks:
                        paperContent = paperContent + " " + subsectionText.text

        # Totals-Werte aus den Helpern berechnen
        for fieldMetrik in UsedFieldMetriks:
            if totalHelperAbstractTitles[fieldMetrik['modelField']] != []:
                fieldMetrik['values']['totals']['abstractTitles'].append(createNewValueAndPaperDict(
                    statistics.mean(totalHelperAbstractTitles[fieldMetrik['modelField']]), paper))
            if totalHelperAbstractText[fieldMetrik['modelField']] != []:
                fieldMetrik['values']['totals']['abstractText'].append(createNewValueAndPaperDict(
                    statistics.mean(totalHelperAbstractText[fieldMetrik['modelField']]), paper))

            if totalHelperSectionTitles[fieldMetrik['modelField']] != []:
                fieldMetrik['values']['totals']['sectionTitles'].append(createNewValueAndPaperDict(
                    statistics.mean(totalHelperSectionTitles[fieldMetrik['modelField']]), paper))
            if totalHelperSectionText[fieldMetrik['modelField']] != []:
                fieldMetrik['values']['totals']['sectionText'].append(createNewValueAndPaperDict(
                    statistics.mean(totalHelperSectionText[fieldMetrik['modelField']]), paper))

            if totalHelperSubsectionTitles[fieldMetrik['modelField']] != []:
                fieldMetrik['values']['totals']['subsectionTitles'].append(createNewValueAndPaperDict(
                    statistics.mean(totalHelperSubsectionTitles[fieldMetrik['modelField']]), paper))
            if totalHelperSubsectionText[fieldMetrik['modelField']] != []:
                fieldMetrik['values']['totals']['subsectionText'].append(createNewValueAndPaperDict(
                    statistics.mean(totalHelperSubsectionText[fieldMetrik['modelField']]), paper))

            totalContent = [] + totalHelperAbstractTitles[fieldMetrik['modelField']] + \
                           totalHelperAbstractText[fieldMetrik['modelField']] + \
                           totalHelperSectionTitles[fieldMetrik['modelField']] + \
                           totalHelperSectionText[fieldMetrik['modelField']] + \
                           totalHelperSubsectionTitles[fieldMetrik['modelField']] + \
                           totalHelperSubsectionText[fieldMetrik['modelField']]
            # addiert metriken für alle Bereiche des Papers um für gesamtes Paper zu berechnen
            if totalContent != []:
                fieldMetrik['values']['totals']['paperText'].append(createNewValueAndPaperDict(
                    sum(totalContent), paper))

        # Totals-Werte aus der Datenbank für average word und average sentence length
        for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
            totalValuesForAveragedMetriks = paper.totalValuesForAveragedMetriks
            totalValues = getattr(totalValuesForAveragedMetriks, fieldMetrik['totalsDBField'] + variant)
            fieldMetrik['values']['totals']['abstractTitles'].append(createNewValueAndPaperDict(
                totalValues.totalAbstractTitles, paper))
            fieldMetrik['values']['totals']['abstractText'].append(createNewValueAndPaperDict(
                totalValues.totalAbstractText, paper))
            fieldMetrik['values']['totals']['sectionTitles'].append(createNewValueAndPaperDict(
                totalValues.totalSectionTitles, paper))
            fieldMetrik['values']['totals']['sectionText'].append(createNewValueAndPaperDict(
                totalValues.totalSectionText, paper))
            fieldMetrik['values']['totals']['subsectionTitles'].append(createNewValueAndPaperDict(
                totalValues.totalSubsectionTitles, paper))
            fieldMetrik['values']['totals']['subsectionText'].append(createNewValueAndPaperDict(
                totalValues.totalSubsectionText, paper))
            fieldMetrik['values']['totals']['paperText'].append(createNewValueAndPaperDict(
                totalValues.totalPaper, paper))

        # Totals-Werte für Tables und Pictures, jeweils nur sectionText ausgefüllt, da diese nur dafür eingelesen werden
        if totalHelperTableCount != []:
            resultsTableCount['totals']['sectionText'].append(createNewValueAndPaperDict(
                statistics.mean(totalHelperTableCount), paper))

        if totalHelperPictureCount != []:
            resultsPictureCount['totals']['sectionText'].append(createNewValueAndPaperDict(
                statistics.mean(totalHelperPictureCount), paper))
        # Totals-Werte für durchschnittliche Beschreibungslänge
        if totalHelperTableDescCount != []:
            resultsTableDescLengthCount['totals']['sectionText'].append(createNewValueAndPaperDict(
                statistics.mean(totalHelperTableDescCount), paper))

        if totalHelperPictureDescCount != []:
            resultsPictureDescLengthCount['totals']['sectionText'].append(createNewValueAndPaperDict(
                statistics.mean(totalHelperPictureDescCount), paper))
        # Text speichern falls Textmetriken berechnet werden müssen
        if textualMetriks:
            paperContents.append(paperContent)
        # typeTokenRatio für das Paper berechnen
        # TODO Statt gesamtes Paper auch sectioned machen?
        if typeTokenRatio:
            wordTokens = nltk.word_tokenize(paperContent)
            wordTokensWithoutNonWords = [item.capitalize() for item in wordTokens if item not in nonWords]
            amountOfTokens = len(wordTokensWithoutNonWords)
            amountOfTypes = len(set(wordTokensWithoutNonWords))
            if amountOfTokens != 0:
                TTR = amountOfTypes / amountOfTokens
                resultsTypeTokenRatio.append(createNewValueAndPaperDict(TTR, paper))

    # Ausgeben der berechneten Ergebnisse
    if authorCount:
        resultDict['authorCount'][corpusIdentifier] = {'rawValues': resultsAuthorCount,
                                                       'statisticalValues': getStatisticalValues(resultsAuthorCount), 'variant': variant}
    if referenceCount:
        resultDict['referenceCount'][corpusIdentifier] = {'rawValues': resultsReferenceCount,
                                                          'statisticalValues': getStatisticalValues(resultsReferenceCount), 'variant': variant}
    if universityCount:
        resultDict['universityCount'][corpusIdentifier] = {'rawValues': resultsUniversityCount,
                                                           'statisticalValues': getStatisticalValues(resultsUniversityCount), 'variant': variant}
    if countryCount:
        resultDict['countryCount'][corpusIdentifier] = {'rawValues': resultsCountryCount,
                                                        'statisticalValues': getStatisticalValues(resultsCountryCount), 'variant': variant}
    if keywordCount:
        resultDict['keywordCount'][corpusIdentifier] = {'rawValues': resultsKeywordCount,
                                                        'statisticalValues': getStatisticalValues(resultsKeywordCount), 'variant': variant}

    if tableCount:
        resultDict['tableCount'][corpusIdentifier] = {'rawValues': resultsTableCount,
                                                      'statisticalValues': getStatisticalValuesForTableAndPictureMetriks(resultsTableCount),
                                                      'variant': variant}
    if tableDescriptionLengthCount:
        resultDict['tableDescriptionLengthCount'][corpusIdentifier] = {'rawValues': resultsTableDescLengthCount,
                                                                       'statisticalValues': getStatisticalValuesForTableAndPictureMetriks(resultsTableDescLengthCount),
                                                                       'variant': variant}
    if pictureCount:
        resultDict['pictureCount'][corpusIdentifier] = {'rawValues': resultsPictureCount,
                                                        'statisticalValues': getStatisticalValuesForTableAndPictureMetriks(resultsPictureCount),
                                                        'variant': variant}
    if pictureDescriptionLengthCount:
        resultDict['pictureDescriptionLengthCount'][corpusIdentifier] = {'rawValues': resultsPictureDescLengthCount,
                                                                         'statisticalValues': getStatisticalValuesForTableAndPictureMetriks(resultsPictureDescLengthCount),
                                                                         'variant': variant}
    if typeTokenRatio:
        resultDict['typeTokenRatio'][corpusIdentifier] = {'rawValues': resultsTypeTokenRatio,
                                                          'statisticalValues': getStatisticalValues(resultsTypeTokenRatio), 'variant': variant}
    for fieldMetrik in UsedFieldMetriks:
        if fieldMetrik['modelField'] == 'charCountWhiteSpace' and charCountWhiteSpace:
            resultDict['charCountWhiteSpace'][corpusIdentifier] = {'rawValues': fieldMetrik['values'],
                                                                   'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values']), 'variant': variant}
        if fieldMetrik['modelField'] == 'charCountNoWhiteSpace' and charCountNoWhiteSpace:
            resultDict['charCountNoWhiteSpace'][corpusIdentifier] = {'rawValues': fieldMetrik['values'],
                                                                     'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values']), 'variant': variant}
        if fieldMetrik['modelField'] == 'wordCount' and wordCount:
            resultDict['wordCount'][corpusIdentifier] = {'rawValues': fieldMetrik['values'],
                                                         'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values']), 'variant': variant}
        if fieldMetrik['modelField'] == 'punctCount' and punctCount:
            resultDict['punctCount'][corpusIdentifier] = {'rawValues': fieldMetrik['values'],
                                                          'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values']), 'variant': variant}
        if fieldMetrik['modelField'] == 'citationCount' and citationCount:
            resultDict['citationCount'][corpusIdentifier] = {'rawValues': fieldMetrik['values'],
                                                             'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values']), 'variant': variant}
    for fieldMetrik in UsedFieldMetriksWithTotalsInDB:
        if fieldMetrik['modelField'] == 'averageWordLength' and averageWordLength:
            resultDict['averageWordLength'][corpusIdentifier] = {'rawValues': fieldMetrik['values'],
                                                                 'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values']), 'variant': variant}
        if fieldMetrik['modelField'] == 'averageSentenceLength' and averageSentenceLength:
            resultDict['averageSentenceLength'][corpusIdentifier] = {'rawValues': fieldMetrik['values'],
                                                                     'statisticalValues': getStatisticalValuesForFieldMetriks(fieldMetrik['values']), 'variant': variant}

    # Berechnen und Ausgeben der Ergebnisse für Textmetriken über den gesamten Korpus
    # TODO Keywords als ganzes betrachten, oder sowas wie "Area of Interest" in drei aufspalten wie aktuell?
    # TODO wenn so wie jetzt dann Stoppwortfiltern, wenn zusammen dann statt nltk tokenizer liste und Counter verwenden
    # TODO paperCount ist länge corpus, bei sektionsmetriken ist nicht immer alles len corpus sondern len existente sektionszahl...passt?
    # TODO Statt gesamtes Paper sectioned machen?
    if mostCommonKeywords:
        '''''
        keywordContents = "" + (" ".join(keywordContents))
        wordTokens = nltk.word_tokenize(keywordContents)
        wordTokenFreqDist = nltk.FreqDist(item.capitalize() for item in wordTokens if item not in nonWords).most_common()
        for wordFreq in wordTokenFreqDist:
            resultsMostCommonKeywords.append(createNewValueAndWordDict(wordFreq[1], wordFreq[0]))
        resultDict['mostCommonKeywords'][corpusIdentifier] = {'rawValues': resultsMostCommonKeywords, 'variant': variant,
                                                              'paperCount': len(corpus)}
        '''''
        counterMostCommonKeywords = Counter(keywordContents).most_common()
        for wordFreq in counterMostCommonKeywords:
            resultsMostCommonKeywords.append(createNewValueAndWordDict(wordFreq[1], wordFreq[0]))
        resultDict['mostCommonKeywords'][corpusIdentifier] = {'rawValues': resultsMostCommonKeywords, 'variant': variant,
                                                              'paperCount': len(corpus)}
    if mostCommonWords:
        paperContentsString = "" + (" ".join(paperContents))
        wordTokens = nltk.word_tokenize(paperContentsString)
        wordTokenFreqDist = nltk.FreqDist(item.capitalize() for item in wordTokens if item not in nonWords and not item.isdigit()).most_common()
        for wordFreq in wordTokenFreqDist:
            resultsMostCommonWords.append(createNewValueAndWordDict(wordFreq[1], wordFreq[0]))
        resultDict['mostCommonWords'][corpusIdentifier] = {'rawValues': resultsMostCommonWords, 'variant': variant,
                                                           'paperCount': len(corpus)}
    # TODO absolute oder prozentuale Häufigkeit?
    if mostPresentWords:
        paperContentsArray = [nltk.word_tokenize(item) for item in paperContents]
        combinedUniqueWordLists = []
        for paperContent in paperContentsArray:
            uniqueWordList = list(set([item.capitalize() for item in paperContent if item not in nonWords and not item.isdigit()]))
            combinedUniqueWordLists = combinedUniqueWordLists + uniqueWordList
        counterMostPresentWords = Counter(combinedUniqueWordLists).most_common()
        for wordFreq in counterMostPresentWords:
            resultsMostPresentWords.append(createNewValueAndWordDict(wordFreq[1], wordFreq[0]))
        resultDict['mostPresentWords'][corpusIdentifier] = {'rawValues': resultsMostPresentWords, 'variant': variant,
                                                            'paperCount': len(corpus)}
    return resultDict


def getStatisticalValuesForTableAndPictureMetriks(input):
    resultsArraySectionText = []

    for list in input['sectioned']['sectionText']:
        resultsArraySectionText.append(getStatisticalValues(list))

    totals = {'sectionText': getStatisticalValues(input['totals']['sectionText']), }
    sectioned = {'sectionText': resultsArraySectionText}
    results = {'totals': totals, 'sectioned': sectioned}
    return results


def getStatisticalValuesForFieldMetriks(input):
    resultsArrayAbstractTitles = []
    resultsArrayAbstractText = []
    resultsArraySectionTitles = []
    resultsArraySectionText = []
    resultsArraySubsectionTitles = []
    resultsArraySubsectionText = []

    for list in input['sectioned']['abstractTitles']:
        resultsArrayAbstractTitles.append(getStatisticalValues(list))
    for list in input['sectioned']['abstractText']:
        resultsArrayAbstractText.append(getStatisticalValues(list))
    for list in input['sectioned']['sectionTitles']:
        resultsArraySectionTitles.append(getStatisticalValues(list))
    for list in input['sectioned']['sectionText']:
        resultsArraySectionText.append(getStatisticalValues(list))
    for list in input['sectioned']['subsectionTitles']:
        resultsArraySubsectionTitles.append(getStatisticalValues(list))
    for list in input['sectioned']['subsectionText']:
        resultsArraySubsectionText.append(getStatisticalValues(list))

    totals = {'paperTitles': getStatisticalValues(input['totals']['paperTitles']),
              'paperText': getStatisticalValues(input['totals']['paperText']),
              'abstractTitles': getStatisticalValues(input['totals']['abstractTitles']),
              'abstractText': getStatisticalValues(input['totals']['abstractText']),
              'sectionTitles': getStatisticalValues(input['totals']['sectionTitles']),
              'sectionText': getStatisticalValues(input['totals']['sectionText']),
              'subsectionTitles': getStatisticalValues(input['totals']['subsectionTitles']),
              'subsectionText': getStatisticalValues(input['totals']['subsectionText'])}
    sectioned = {'abstractTitles': resultsArrayAbstractTitles, 'abstractText': resultsArrayAbstractText,
                 'sectionTitles': resultsArraySectionTitles, 'sectionText': resultsArraySectionText,
                 'subsectionTitles': resultsArraySubsectionTitles, 'subsectionText': resultsArraySubsectionText}
    results = {'totals': totals, 'sectioned': sectioned}
    return results
