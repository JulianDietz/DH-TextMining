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
import os

import TextMining.models
import numpy as np

#currentJsonfiles=[]

'''init ntlk run:
import nltk
nltk.download('stopwords')
'''

def helloWorld(request):
    return render(request, 'helloWorld.html')

def results(request):
    return render(request, 'results/results.html')


def readJsonFilesView (request):
    files = os.listdir('./static/uploadFiles')
    numberFiles = len(files)
    numPaper=Paper.objects.all().count()
    context = {'numberFiles':numberFiles,'numberPaper':numPaper}
    return render(request, 'readJsonFiles.html', context)

def readJsonFiles(request):
    # loads all Json files....
    readpath = "./static/uploadFiles"
    onlyOne = False
    counter=0
    for filename in listdir(readpath):
        if not onlyOne:
            if filename != ".DS_Store": #file.endswith('.json')
                #print(filename)
                filepath=join(readpath, filename)
                file = open(filepath, 'r', encoding='utf-8', errors="ignore")
                paperJson = json.load(file)
                paper=savePaper(paperJson)
                counter+=1
                os.remove(filepath)
        onlyOne=False

    return JsonResponse({'sucess':'Super!!!!!'})

def processPaperView (request):
    numberPaper = Paper.objects.all().count()
    context = {'numberPaper':numberPaper}
    return render(request, 'processPaper.html', context)

#Aufbereiten der Text Stopwortfiltern und lemmatisieren
def processPaper(request):
    print("Paper werden aufbreitet....")
    paperlist = Paper.objects.all()
    for paper in paperlist:
        print('Paper: '+paper.titleRaw.text)
        metriken.removeStopwords(paper) #MET_text_to_STOP_text
        metriken.stemText(paper) #MET_text_to_STEM_text
        metriken.calculateAllMetrics(paper)

    print("Papersind aufbereitet und vorberechnet")
    return JsonResponse({'sucess': 'Super!!!!!'})


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
    getMetriks(Paper.objects, 'NltkStw', charCountWhiteSpace=True, charCountNoWhiteSpace=True, wordCount=True,
               punctCount=True, citationCount=True, authorCount=True, referenceCount=True, universityCount=True,
               countryCount=True, keywordCount=True, tableCount=True, pictureCount=True,
               tableDescriptionLengthCount=True, pictureDescriptionLengthCount=True, keywordFrequency=True)
    return render(request, 'index.html')


def getStatisticalValues(inputarray):
    total = np.sum(inputarray)
    average = np.mean(inputarray)
    mode = stats.mode(inputarray)
    variance = np.var(inputarray)
    lowerQuartile, median, upperQuartile = np.percentile(inputarray, [25, 50, 75])
    min = np.amin(inputarray)
    max = np.amax(inputarray)
    return {'total': total,'average': average, 'median': median, 'mode': mode, 'variance': variance, 'lowerQuartile': lowerQuartile,
            'upperQuartile': upperQuartile, 'minimum': min, 'maximum': max}

#Erster Ansatz Ergebnisse, Ergebnisse noch nach Paperaufbau anstatt Metriken gegliedert
'''
def newMetriksDictionaire():
    return {'Text': {'charCountWhiteSpace': [], 'charCountNoWhiteSpace': [], 'wordCount': [],
                     'punctCount': [], 'citationCount': [], 'textContent': []},
            'Title': {'charCountWhiteSpace': [], 'charCountNoWhiteSpace': [], 'wordCount': [],
                      'punctCount': [], 'citationCount': [], 'textContent': []},
            'tableCount': [], 'pictureCount': [], 'tableDescLengthCount': [], 'pictureDescLengthCount': []}


def appendFieldMetrik(condition, modelField, dict, titleMetrik, textMetrik):
    if condition:
        dict['Title'][modelField].append(getattr(titleMetrik, modelField))
        dict['Text'][modelField].append(getattr(textMetrik, modelField))

def appendFieldMetrikForTitle(condition, modelField, dict, title):
    if condition:
        dict[modelField].append(getattr(title, modelField))

#TODO if Abfragen für existenz von Feldern
def getMetriksRawTest(corpus, variant, charCountWhiteSpace=False, charCountNoWhiteSpace=False, wordCount=False,
                  punctCount=False, citationCount=False, authorCount=False, referenceCount=False, universityCount=False,
                  countryCount=False, keywordCount=False, tableCount=False, pictureCount=False,
                  tableDescriptionCount=False, pictureDescriptionCount=False, keywordFrequency=False):

    print('start!!!!!!!!')
    titles = {'charCountWhiteSpace': [], 'charCountNoWhiteSpace': [], 'wordCount': [],
              'punctCount': [], 'citationCount': [], 'textContent': []}
    abstracts = []
    sections = []
    subsections = []

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

        #Feldmetriken Titel
        paperTitle = getattr(paper, "title" + variant)
        paperTitleMetrik = getattr(paperTitle, 'metrik')
        for FieldMetrik in FieldMetriks:
            appendFieldMetrikForTitle(FieldMetrik['condition'], FieldMetrik['modelField'], titles, paperTitleMetrik)

        #Feldmetriken Abstracts
        for abstractCount, abstract in enumerate(paper.abstract):
            if abstractCount == len(abstracts):
                abstracts.append(newMetriksDictionaire())

            abstractTitle = getattr(abstract, "title" + variant)
            abstractTitleMetrik = getattr(abstractTitle, 'metrik')
            abstractText = getattr(abstract, "text" + variant)
            abstractTextMetrik = getattr(abstractText, 'metrik')
            for FieldMetrik in FieldMetriks:
                appendFieldMetrik(FieldMetrik['condition'], FieldMetrik['modelField'], abstracts,
                                  abstractTitleMetrik, abstractTextMetrik)

        #Feldmetriken Sectionen und Subsectionen
        for sectionCount, section in enumerate(paper.content):
            if sectionCount == len(sections):
                sections.append(newMetriksDictionaire())
                subsections.append([])

            sectionTitle = getattr(section, "title" + variant)
            sectionTitleMetrik = getattr(sectionTitle, 'metrik')
            sectionText = getattr(section, "text" + variant)
            sectionTextMetrik = getattr(sectionText, 'metrik')
            for FieldMetrik in FieldMetriks:
                appendFieldMetrik(FieldMetrik['condition'], FieldMetrik['modelField'], sections[sectionCount],
                                  sectionTitleMetrik, sectionTextMetrik)

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
                    subsectionTitleMetrik = getattr(subsectionTitle, 'metrik')
                    subsectionText = getattr(subsection, "text" + variant)
                    subsectionTextMetrik = getattr(subsectionText, 'metrik')

                    for FieldMetrik in FieldMetriks:
                        appendFieldMetrik(FieldMetrik['condition'], FieldMetrik['modelField'], subsections[sectionCount][subsectionCount],
                                          subsectionTitleMetrik, subsectionTextMetrik)


    print('Titles:')
    print(titles)
    print('Abstracts:')
    print(abstracts)
    print('Sections:')
    print(sections)
    print('Subsections:')
    print(subsections)

    print(resultsAuthorCount)
    print(resultsReferenceCount)
    print(resultsUniversityCount)
    print(resultsCountryCount)
    print(resultsKeywordCount)
    print(resultsKeywordText)
    #TODO Hier noch nicht Metriken ausgerechnet da nicht sicher ob nicht doch noch wertereihen gebruacht, falls wir zB doch Boxplot machen wollen
    #TODO statistische Werte mit Methode berechnen. results nach subsection/section oder nach Metriken gliedern?
    results = {}

    #title
    #abstracts
    #sectionen
    #subsectionen
    #gesamt (Abstracts + Sectionen + Subsectionen)
    return ""
'''


#TODO durchschnittliche Wortlänge, durchschnittliche Satzlänge, häufigste Wörter, Most Present Words (TF), Häufigste Keywords, Readability
#TODO was gemeint mit Größe/Dichte Wortschatz, Anzahl Überschriften (=alle Titles? dann ja nur einfach alle Sektionen?)
#TODO die können alle über den Text berechnet werden => text raw in dict werfen?

#TODO Schauen welche Felder immer in db, und welche mit if abfragen? Alle Liste in db immer mit [] machen wenn leer? Metadata für jedes da? Keywords
#TODO wenn leer []? was wenn zb. Sektion keinen titel hat? None immer abfragen?
#TODO Die einzelnen ifs in den Schleifen raus und immer appenden? Performance dann besser oder nicht?

def createNewMetrikDict():
    return {'titles': [], 'totalContentTitles': [], 'totalContentText': [], 'abstractTitles': [], 'abstractText': [],
            'sectionTitles': [], 'sectionText': [], 'subsectionTitles': []}


def analyseCorpora(variant, corpus1, corpus2,charCountWhiteSpace=False, charCountNoWhiteSpace=False, wordCount=False,
               punctCount=False, citationCount=False, authorCount=False, referenceCount=False,
               universityCount=False,countryCount=False, keywordCount=False, tableCount=False, pictureCount=False,
               tableDescriptionLengthCount=False, pictureDescriptionLengthCount=False, keywordFrequency=False):

    metriks1 = getMetriks(corpus1, variant,charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
               punctCount, citationCount, authorCount, referenceCount,
               universityCount,countryCount, keywordCount, tableCount, pictureCount,
               tableDescriptionLengthCount, pictureDescriptionLengthCount, keywordFrequency)
    metriks2 = getMetriks(corpus2, variant,charCountWhiteSpace, charCountNoWhiteSpace, wordCount,
               punctCount, citationCount, authorCount, referenceCount,
               universityCount,countryCount, keywordCount, tableCount, pictureCount,
               tableDescriptionLengthCount, pictureDescriptionLengthCount, keywordFrequency)
    results = {'Corpus1': metriks1, 'Corpus2': metriks2}
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
                fieldMetrik['values']['titles'].append(getattr(paperTitleMetrik, fieldMetrik['modelField']))

        # Feldmetriken Abstracts
        for abstractCount, abstract in enumerate(paper.abstract):
            if abstractCount == len(abstractHelper):
                abstractHelper.append([])
                for fieldMetrik in UsedFieldMetriks:
                    fieldMetrik['values']['abstractTitles'].append([])
                    fieldMetrik['values']['abstractText'].append([])

            abstractTitle = getattr(abstract, "title" + variant)
            abstractTitleMetrik = getattr(abstractTitle, 'metrik')
            abstractText = getattr(abstract, "text" + variant)
            abstractTextMetrik = getattr(abstractText, 'metrik')
            for fieldMetrik in UsedFieldMetriks:
                fieldMetrik['values']['abstractTitles'][abstractCount].append(
                    getattr(abstractTitleMetrik, fieldMetrik['modelField']))
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
            sectionTitleMetrik = getattr(sectionTitle, 'metrik')
            sectionText = getattr(section, "text" + variant)
            sectionTextMetrik = getattr(sectionText, 'metrik')
            for fieldMetrik in UsedFieldMetriks:
                fieldMetrik['values']['sectionTitles'][sectionCount].append(
                    getattr(sectionTitleMetrik, fieldMetrik['modelField']))
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
                    subsectionTitleMetrik = getattr(subsectionTitle, 'metrik')
                    subsectionText = getattr(subsection, "text" + variant)
                    subsectionTextMetrik = getattr(subsectionText, 'metrik')

                    for fieldMetrik in UsedFieldMetriks:
                        fieldMetrik['values']['subsectionTitles'][sectionCount][subsectionCount].append(
                            getattr(subsectionTitleMetrik, fieldMetrik['modelField']))
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
    print(results)
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
    #TODO subsectionen hier jetzt nicht nach zugehöriger Sektion (1.,2.,...), sondern nur nach erste, zweite,... Subsection gegliedert
    #subsection titles
    totalSubsectionsForTitles = 0
    for list in input['subsectionTitles']:
        subsectionCount = len(max(list, key=len))
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
        subsectionCount = len(max(list, key=len))
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