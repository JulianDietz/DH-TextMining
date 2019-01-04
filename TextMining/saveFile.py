from .models import Metric,Text, Subsection, Reference, References, Paper, Author, Metadata, Authors, University, Abstract, \
    Picture, Pictures, Table, Tables

def savePaper(paperJson):
    paperDB = Paper()
    paperDB.title = paperJson['title']
    # create Authors
    if paperJson.get('authors'):
        paperDB.authors = Authors(count=paperJson['authors']['count'], authorList=[])
        for autor in paperJson['authors']['authorList']:
            paperDB.authors.authorList.append(
                Author(authorName=autor['authorName'], authorIndex=autor['authorIndex'],
                       university=University(
                           university_universityName=autor['university']['universityName'],
                           university_universityCountry=autor['university'][
                               'universityCountry'])))
        # authors = Authors.objects.create(count=paperJson['authors']['count'], authorList=arrayAutoren)
    else:
        paperDB.authors = Authors(count=0, authorList=[])

    # metadata
    if paperJson['metaData']:
        paperDB.metaData = Metadata(yearOfArticle=paperJson['metaData']['yearOfArticle'],
                                    category=paperJson['metaData']['category'],
                                    source=paperJson['metaData']['source'],
                                    journalTitle=paperJson['metaData']['journaltitle'],
                                    impactfactor=paperJson['metaData']['impactFactor'],
                                    URL=paperJson['metaData']['URL'],
                                    paperType=paperJson['metaData']['paperType'])
        if paperJson['metaData'].get('keywords'):
            paperDB.metaData.keywords = paperJson['metaData']['keywords']
        else:
            paperDB.metaData.keywords = []
            # paperDB.metaData.yearOfArticle=paperJson['metaData']['yearOfArticle'],
            # paperDB.metaData.category=paperJson['metaData']['category'],
            # paperDB.metaData.source=paperJson['metaData']['source'],
            # paperDB.metaData.journalTitle = paperJson['metaData']['journaltitle'],
            # paperDB.metaData.impactfactor = paperJson['metaData']['impactFactor'],
            # paperDB.metaData.URL=paperJson['metaData']['URL'],
            # paperDB.metaData.paperType=paperJson['metaData']['paperType']

    # create Abstract
    # Todo paper sollte immer Array sein( auch bei titel=empty and text=empty) <<empty>>
    paperDB.abstract = []
    if isinstance(paperJson['abstract'], list):
        for abstractPart in paperJson['abstract']:
            paperDB.abstract.append(Abstract(title=abstractPart['title'], text=abstractPart['text'], metrik=Metric()))
    else:
        if not paperJson['abstract'] == '<<empty>>':
            paperDB.abstract.append(
                Abstract(title=paperJson['abstract']['title'], text=paperJson['abstract']['title'], metrik=Metric()))

    if paperJson.get('references'):
        # create Reference
        paperDB.references = References(referencesList=[], count=paperJson['references']['count'])
        arrayReferences = []
        for reference in paperJson['references']['referencesList']:
            paperDB.references.referencesList.append(Reference(referenceIndex=reference['referenceIndex'],
                                                               referenceName=reference['referenceName'],
                                                               referenceAuthor=reference['referenceAuthor'],
                                                               referenceYear=str(reference['referenceYear'])))
    else:
        paperDB.references = References(referencesList=[], count=0)

    # createText todo tabellen und bilder an models anpassen!
    paperDB.text = []
    for textsection in paperJson['text']:
        # tables
        subTextArray = []
        arrayTables = []
        if textsection['tables']:
            for table in textsection['tables']['tablesList']:
                arrayTables.append(
                    Table(tableIndex=table['index'], tableRowDim=table['tableRowDim'],
                          tableCodDim=table['tableColDim'],
                          tableDescription=table['tableDescription']))
            tables = Tables(count=textsection['tables']['count'], tablesList=arrayTables)
        else:
            tables = None
        # pictures
        arrayPictures = []
        if textsection['pictures']:
            for picture in textsection['pictures']['picturesList']:
                arrayTables.append(
                    Picture(pictureIndex=picture['index'], pictureDescription=picture[
                        'pictureDescription']))
            pictures = Pictures(count=textsection['pictures']['count'], picturesList=arrayPictures)
        else:
            pictures = None

        if textsection['subsection']:
            for subsection in textsection['subsection']:
                subTextArray.append(Subsection(title=subsection['title'], text=subsection['text'], metrik=Metric()))

        paperDB.text.append(
            Text(title=textsection['title'], text=textsection['text'], metrik=Metric(), subsection=subTextArray,
                 tables=tables, pictures=pictures,
                 # formula=textsection['formula']
                 ))
    paperDB.save()
    return paperDB