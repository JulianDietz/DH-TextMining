# -*- coding: utf-8 -*-
from functools import reduce
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from collections import Counter
from mongoengine.queryset.visitor import Q
from django.shortcuts import redirect
from os import listdir, system
from os.path import join
from TextMining import metriken
from TextMining.saveFile import savePaper
from scipy import stats
from TextMining.models import Paper

import nltk
import json
import os
import math
import numpy as np
import statistics

KORPUS1 = None
KORPUS2 = None


def redirect_view(request):
    return redirect('corpusSelection')


def showInfo(request):
    return render(request, 'infopage/info.html')


def corpusSelection(request):
    return render(request, 'corpusSelection/corpusSelection.html')


def readJsonFilesView(request):
    files = os.listdir('./static/uploadFiles')
    numberFiles = len(files)
    numPaper = Paper.objects.all().count()
    context = {'numberFiles': numberFiles, 'numberPaper': numPaper}
    return render(request, 'readJsonFiles.html', context)


def readJsonFiles(request):
    # Wird per AJAX-Request aufgerufen, lädt alle JSON-Dateien und speichert diese in der Datenbank
    readpath = "./static/uploadFiles"
    onlyOne = False
    counter = 0
    for filename in listdir(readpath):
        if not onlyOne:
            if filename != ".DS_Store":
                filepath = join(readpath, filename)
                file = open(filepath, 'r', encoding='utf-8', errors="ignore")
                paperJson = json.load(file)
                paper = savePaper(paperJson)
                counter += 1
                file.close()
                os.remove(filepath)
        onlyOne = False
    return JsonResponse({'sucess': 'Super!!!!!'})


def processPaperView(request):
    numberPaper = Paper.objects.all().count()
    numberRehashed = Paper.objects.all().filter(isRehashed=True).count()
    context = {'numberPaper': numberPaper, 'numberRehashed': numberRehashed}
    return render(request, 'processPaper.html', context)

# Aufbereiten der Texte mit stopwortfiltern oder stemmen
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all().timeout(False)
    for paper in paperlist:
        if not paper.isRehashed:
            print('Paper: ' + paper.titleRaw.text)
            metriken.removeStopwords(paper)
            metriken.stemText(paper)
            metriken.calculateAllMetrics(paper)
    return JsonResponse({'sucess': 'Super!!!!!'})

# Filtert Paper aus der Datenbank je nach gewählten Parametern
def getSelectedPaper(request):
    if (request.method == "POST"):
        corpus1 = {}
        corpus2 = {}
        querydata = request.POST
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
        ####### Filtert DB
        paperCorpus1 = filterDB(corpus1)
        paperCorpus2 = filterDB(corpus2)
        return JsonResponse({'sucess': True, 'corpus1': paperCorpus1, 'corpus2': paperCorpus2})

    if (request.method == "GET"):
        return redirect('corpusSelection')


# http://docs.mongoengine.org/guide/querying.html
# https://stackoverflow.com/questions/8189702/mongodb-using-an-or-clause-in-mongoengine
# Filtert Paper aus der Datenbank je nach gewählten Parametern
def filterDB(querydata):
    if querydata:
        papers = Paper.objects.all()
        for number in querydata:
            query = querydata[number]
            field = query['optionfield']
            searchdata = query['inputfield']
            searchArry = searchdata.split(',')
            searchArry = [x.strip(' ') for x in searchArry]
            for index,entry in enumerate(searchArry):
                entry = [word.capitalize() for word in entry.split(' ')]
                searchArry[index] = ' '.join(entry)
            searchArry = list(filter(None, searchArry))
            if searchArry:
                if field == 'authors':
                    query = reduce(lambda q1, q2: q1.__or__(q2), map(lambda query: Q(authors__name__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'category':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__category__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'organization':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__organization__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'keywords':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__keywords__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'journal':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__journal__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'source':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__source__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'yearOfArticle':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__yearOfArticle__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'language':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__language__icontains=query), searchArry))
                    papers = papers.filter(query)
                if field == 'title':
                    query = reduce(lambda q1, q2: q1.__or__(q2),
                                   map(lambda query: Q(metaData__title__icontains=query), searchArry))
                    papers = papers.filter(query)
        return papers.to_json()
    else:
        return ''

# Ruft Ergebnisseite mit den ausgewählten Korpora und initialen Textvarianten auf
def startAnalyse(request):
    if (request.method == "POST"):
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
            "metrics": [{"metric": "authorCount", "dataDisplayType": "numeric-total",
                         "germanTitle": "Autorenanzahl", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "keywordCount", "dataDisplayType": "numeric-total",
                         "germanTitle": "Keywordanzahl", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "referenceCount", "dataDisplayType": "numeric-total",
                         "germanTitle": "Referenzenanzahl", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "countryCount", "dataDisplayType": "numeric-total",
                         "germanTitle": "Anzahl beteiligter Länder", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "universityCount", "dataDisplayType": "numeric-total",
                         "germanTitle": "Anzahl beteiligter Universitäten", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "typeTokenRatio", "dataDisplayType": "numeric-total",
                         "germanTitle": "Type-Token-Ratio", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "charCountWhiteSpace", "dataDisplayType": "numeric-section",
                         "germanTitle": "Zeichenanzahl mit Leerzeichen", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "charCountNoWhiteSpace", "dataDisplayType": "numeric-section",
                         "germanTitle": "Zeichenanzahl ohne Leerzeichen", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "wordCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Wortanzahl", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "punctCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Satzzeichenanzahl", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "citationCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Anzahl der Zitate", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "averageWordLength", "dataDisplayType": "numeric-section",
                         "germanTitle": "Durchschnittliche Wortlänge", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "averageSentenceLength", "dataDisplayType": "numeric-section",
                         "germanTitle": "Durchschnittliche Satzlänge", "graphType": "boxplot",
                         "allowTextVariants": "true", "foundation": "document"},
                        {"metric": "pictureCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Bilderanzahl", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "tableCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Tabellenanzahl", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "pictureDescriptionLengthCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Durchschnittliche Bildbeschriftungslängen", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "tableDescriptionLengthCount", "dataDisplayType": "numeric-section",
                         "germanTitle": "Durchschnittliche Tabellenbeschriftungslängen", "graphType": "boxplot",
                         "allowTextVariants": "false", "foundation": "document"},
                        {"metric": "mostCommonKeywords", "dataDisplayType": "text-total",
                         "germanTitle": "Häufigste Keywords", "graphType": "wordcloud",
                         "allowTextVariants": "false", "foundation": "corpus"},
                        {"metric": "mostCommonWords", "dataDisplayType": "text-total",
                         "germanTitle": "Häufigste Wörter", "graphType": "lollipop",
                         "allowTextVariants": "true", "foundation": "corpus"},
                        {"metric": "mostPresentWords", "dataDisplayType": "text-total", "germanTitle": "Häufigst anwesende Wörter", "graphType": "lollipop", "allowTextVariants": "true",
                         "foundation": "corpus"},
                        ]}

        corpusTextVariants = {"Korpus1": varianteKorpus1, "Korpus2": varianteKorpus2}
        context = {'metricList': metricList, 'corpusTextVariants': corpusTextVariants}
        return render(request, 'results/results.html', context)

    if (request.method == "GET"):
        return redirect('corpusSelection')

# Lädt aud den Filtern resultierenden Korpus herunter
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

# Wird aus der Ergebnisseite heraus über ein AJAX-Request aufgerufen, gibt die Endergebnisse
# für die Analyse einer ausgewählten Metrik zurück
def calculateMetrik(request):
    if request.method == "GET":
        fieldname = request.GET.get('fieldname')
        variante1 = request.GET.get('Korpus1_variante')
        variante2 = request.GET.get('Korpus2_variante')
        if fieldname:
            bool = True
            response = analyseCorpora(variante1, variante2, KORPUS1, KORPUS2, **{fieldname: bool})
        return JsonResponse(response, safe=False)

# Berechnet die statistischen Werte aus den Arrays mit den Einzelwerten bei der Auswertung von Metriken
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


# Teil des Ergebnis-Dictionnaires, übergibt für jeden Einzelwert bei der Auswertung von Metriken eininge Daten
# des zugehörigen Papers
def createNewValueAndPaperDict(value, paper):
    return {'value': value, 'name': paper.titleRaw.text, 'authors': [author.name for author in paper.authors],
            'year': paper.metaData.yearOfArticle, 'paperID': str(paper.id), 'URL': paper.metaData.URL}

# Teil des Ergebnis-Dictionnaires, übergibt für gesamttextuellle Metriken die Wörter und deren zugehörigen Wert
def createNewValueAndWordDict(value, word):
    return {'value': value, 'name': word}

# Teil des Ergebnis-Dictionnaires, übergibt für die einzelnen Teile eines Papers jeweils ein Array
# mit Einzelwerten im Korpus, und ein Array mit Durchschnitts-Werten für die gesamten Abschnitte
def createNewMetrikDict():
    totals = {'paperTitles': [], 'paperText': [], 'abstractTitles': [], 'abstractText': [],
              'sectionTitles': [], 'sectionText': [], 'subsectionTitles': [], 'subsectionText': []}
    sectioned = {'abstractTitles': [], 'abstractText': [],
                 'sectionTitles': [], 'sectionText': [], 'subsectionTitles': [], 'subsectionText': []}
    return {'totals': totals, 'sectioned': sectioned}


# Tables und Pictures sind nur für jede Sektion gespeichert, und daher eine "abgespeckte" Variante der FieldMetriks
# ohne Abstracts und Subsections sowie ohne Titel
def createNewTableOrPicturesMetrikDict():
    totals = {'sectionText': []}
    sectioned = {'sectionText': []}
    return {'totals': totals, 'sectioned': sectioned}


# Berechnet alle übergebenen Metriken. Wird aktuell immer nur mit einer übergebenen Metrik aufgerufen.
# Wurde allerdings so konzipiert, dass man nur einen Loop über alle Paper-Objects braucht, falls man schon zu Beginn
# angeben könnte, welche Metriken man alle ausgerechnet haben will, falls das Programm irgendwann
# um diese Funktionalität erweitert werden sollte.
def analyseCorpora(variant1, variant2, corpus1, corpus2, charCountWhiteSpace=False, charCountNoWhiteSpace=False, wordCount=False,
                   punctCount=False, citationCount=False, authorCount=False, referenceCount=False,
                   universityCount=False, countryCount=False, keywordCount=False, tableCount=False, pictureCount=False,
                   tableDescriptionLengthCount=False, pictureDescriptionLengthCount=False,
                   averageWordLength=False, averageSentenceLength=False, mostCommonWords=False, mostCommonKeywords=False,
                   mostPresentWords=False, typeTokenRatio=False):

    # Alle Metriken, welche für Abschnitte des Papers berechnet werden
    sectionedMetriks = {('charCountWhiteSpace', charCountWhiteSpace), ('charCountNoWhiteSpace', charCountNoWhiteSpace),
                        ('wordCount', wordCount), ('punctCount', punctCount), ('citationCount', citationCount),
                        ('averageWordLength', averageWordLength), ('averageSentenceLength', averageSentenceLength)}
    # Abschnitte des Papers
    sectionedParts = {'abstractTitles', 'abstractText', 'sectionTitles', 'sectionText', 'subsectionTitles', 'subsectionText'}

    # Tables und Pictures werden nur für Sektionen erfasst, und dort nur im Text => abgespeckte Variante der sectionedMetriks
    partiallySectionedMetriks = {('tableCount', tableCount), ('pictureCount', pictureCount),
                                 ('tableDescriptionLengthCount', tableDescriptionLengthCount),
                                 ('pictureDescriptionLengthCount', pictureDescriptionLengthCount)}

    valueParts = {'rawValues', 'statisticalValues'}
    # Zu berechnende Metriken werden leer dem Ergebnis zugeführt
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

    # Berechnet gewählte Metriken für die existierenden Korpora
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
    # Gleicht Länge der Ausgabe bei 2 Korpora aneinander an indem es nichtexistente Abschnitte mit leeren Arrays auffüllt,
    # da dies die spätere Anzeige erleichtert
    if corpus1 and corpus2:
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
        for metrik in partiallySectionedMetriks:
            if metrik[1]:
                for valuePart in valueParts:
                    while len(results[metrik[0]]['Corpus1'][valuePart]['sectioned']['sectionText']) < \
                            len(results[metrik[0]]['Corpus2'][valuePart]['sectioned']['sectionText']):
                        results[metrik[0]]['Corpus1'][valuePart]['sectioned']['sectionText'].append([])
                    while len(results[metrik[0]]['Corpus2'][valuePart]['sectioned']['sectionText']) < \
                            len(results[metrik[0]]['Corpus1'][valuePart]['sectioned']['sectionText']):
                        results[metrik[0]]['Corpus2'][valuePart]['sectioned']['sectionText'].append([])
    return json.dumps(results)

# Berechnet die Metriken aus den in der DB hinterlegten Werten
def getMetriks(corpus, variant, corpusIdentifier, resultDict, charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
               punctCount, citationCount, authorCount, referenceCount,
               universityCount, countryCount, keywordCount, tableCount, pictureCount,
               tableDescriptionLengthCount, pictureDescriptionLengthCount,
               averageWordLength, averageSentenceLength, mostCommonWords, mostCommonKeywords,
               mostPresentWords, typeTokenRatio):

    # Hilfsvariablen für die Länge der Abstracts, Sectionen und Subsectionen
    abstractHelper = []
    sectionHelper = []
    subsectionHelper = []

    resultsAuthorCount = []
    resultsReferenceCount = []
    resultsUniversityCount = []
    resultsCountryCount = []
    resultsKeywordCount = []

    # Speichert aller Paper und Keywords in einem Array
    paperContents = []
    keywordContents = []
    nonWords = ['.', ',', '\\', '/', '#', '!', '?', '^', '&', '*', ';', ':', '{', '}', '=', '-', '_', '`', '~',
                '“', '”', '"', '(', ')', "'", '""', "''", '<', '>', '[', ']', ' ', '%', '&', '§', "’", "", '']

    resultsMostCommonWords = []
    resultsMostCommonKeywords = []
    resultsMostPresentWords = []
    resultsTypeTokenRatio = []

    # Liste für jede Sektion mit Werten Anzahl Tables/Pictures
    resultsTableCount = createNewTableOrPicturesMetrikDict()
    resultsPictureCount = createNewTableOrPicturesMetrikDict()
    # Liste für jede Sektion mit Liste an Werten der Beschreibungslänge
    resultsTableDescLengthCount = createNewTableOrPicturesMetrikDict()
    resultsPictureDescLengthCount = createNewTableOrPicturesMetrikDict()

    # Normale (Count)-Metriken, deren durchschnittlicher Wert in allen Sektionen
    # aus den Werten der einzelnen Sektionen berechnet werden kann
    FieldMetriks = [{'condition': charCountWhiteSpace, 'modelField': "charCountWhiteSpace", 'values': createNewMetrikDict()},
                    {'condition': charCountNoWhiteSpace, 'modelField': "charCountNoWhiteSpace", 'values': createNewMetrikDict()},
                    {'condition': wordCount, 'modelField': "wordCount", 'values': createNewMetrikDict()},
                    {'condition': punctCount, 'modelField': "punctCount", 'values': createNewMetrikDict()},
                    {'condition': citationCount, 'modelField': "citationCount", 'values': createNewMetrikDict()}]

    # Durchschnittsmetriken, deren durchschnittlicher Wert in allen Sektionen
    # nicht aus den Werten der einzelnen Sektionen berechnet werden kann, und deshalb aus der DB kommt
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
        # Hilfsvariablen zum Berechnen des gesamten Durchschnitts für sektionierte Metriken
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
        # Gesamter Text des Papers zum Berechnen der häufigsten Wörter, Most Present Words, TTR
        paperContent = ""

        # Allgemeine Metriken, bezogen auf ganzes Paper
        if authorCount or universityCount or countryCount:
            authors = paper.authors
            universities = []
            countries = []
            for author in authors:
                university = author.university
                if university:
                    if university.name not in universities:
                        universities.append(university.name)
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

        # Sektionierte Metriken, bezogen auf dei jeweils zugehörigen Abschnitte
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
            # Addiert metriken für alle Bereiche des Papers um für gesamtes Paper zu berechnen
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
        # Type-Token-Ratio für das Paper berechnen
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
    if mostCommonKeywords:
        keywordContents = [keyword for keyword in keywordContents if keyword not in nonWords]
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


# Loop und fügt statistische Werte für Bilder un Tabellen, welche nur auf Sektions-Level existieren, zum Ergebnis hinzu
def getStatisticalValuesForTableAndPictureMetriks(input):
    resultsArraySectionText = []

    for list in input['sectioned']['sectionText']:
        resultsArraySectionText.append(getStatisticalValues(list))

    totals = {'sectionText': getStatisticalValues(input['totals']['sectionText']), }
    sectioned = {'sectionText': resultsArraySectionText}
    results = {'totals': totals, 'sectioned': sectioned}
    return results

# Loop und fügt statistische Werte für normale Feld-Metriken zum Ergebnis hinzu
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
