# from .models import Metric,Text, Subsection, Reference, References, Paper, Author, Metadata, Authors, University, Abstract, \
#    Picture, Pictures, Table, Tables
from .models import Paper, Metadata, Author, University, Abstract, Table, Picture, TextVariant, Subsection, Section, \
    Reference


# mongo
# show dbs
# use textmining
# db.dropDatabase()

# db.paper.find()


def savePaper(paperJson):
    print('Paper in der Datenbank speichern')
    print(paperJson)

    paperDB = Paper()
    paperDB.titleRaw=TextVariant(text=paperJson['metaData']['title'])
    # AutorenListe
    if paperJson.get('authors'):
        for autor in paperJson['authors']['authorList']:
            paperDB.authors.append(Author(name=autor['authorName'], index=autor['authorIndex'],
                                          university=University(name=autor['university']['universityName'],
                                                                country=autor['university']['universityCountry'])))

    # Metadaten
    if paperJson['metaData']:
        if paperJson['metaData'].get('keywords'):
            keywords = paperJson['metaData']['keywords']
        else:
            keywords = []

        paperDB.metaData = Metadata(yearOfArticle=paperJson['metaData']['yearOfArticle'],
                                    journalTitle=paperJson['metaData']['journaltitle'],
                                    impactfactor=paperJson['metaData']['impactFactor'],
                                    paperType=paperJson['metaData']['paperType'],
                                    keywords=keywords,
                                    #TODO source jetzt in dict???
                                    #URL=paperJson['metaData']['URL'],
                                    #source=paperJson['metaData']['source'],
                                    URL=paperJson['metaData']['source']['URL'],
                                    source=paperJson['metaData']['source']['sourceName'],
                                    # TODO auch in array?? wann mehrere?
                                    category=paperJson['metaData']['category'][0],
                                    entrytype=paperJson['metaData']['paperType'],
                                    #TODO titel doppelt speichern?
                                    title=paperJson['metaData']['title'],
                                    month=paperJson['metaData']['month'],
                                    language=paperJson['metaData']['language'],
                                    volume = paperJson['metaData']['volume'],
                                    issue = paperJson['metaData']['issue'],
                                    pages =paperJson['metaData']['pages'],
                                    edition=str(paperJson['metaData']['edition']),# only String
                                    publisher=paperJson['metaData']['publisher'],
                                    booktitle=paperJson['metaData']['booktitle'],
                                    location=paperJson['metaData']['location'],
                                    organisation=paperJson['metaData']['organisation'],
                                    address=paperJson['metaData']['organisation'],
                                    citekey=str(paperJson['metaData']['id']),#id=citekey?
                                    publicationtype=paperJson['metaData']['publicationtype'],
                                    chapter=paperJson['metaData']['chapter'],
                                    doi=paperJson['metaData']['doi']
                                    )

    # Abstract
    # TODO <<empty>>?
    for abstractPart in paperJson['abstract']:
        paperDB.abstract.append(
            Abstract(titleRaw=TextVariant(text=abstractPart['title']), textRaw=TextVariant(text=abstractPart['text'])))

    # References
    # TODO year integer?
    if paperJson.get('references'):
        for reference in paperJson['references']['referencesList']:
            paperDB.references.append(Reference(index=reference['referenceIndex'],
                                                name=reference['referenceName'],
                                                author=reference['referenceAuthor'],
                                                year=str(reference['referenceYear'])))

    # Content
    for textsection in paperJson['text']:
        # TABLEs
        arrayTables = []
        if textsection['tables']:
            for table in textsection['tables']['tablesList']:
                arrayTables.append(
                    Table(index=table['index'], rowDim=table['tableRowDim'], codDim=table['tableColDim'],
                          description=table['tableDescription']))
        else:
            arrayTables = []

        # pictures
        arrayPictures = []
        if textsection['pictures']:
            for picture in textsection['pictures']['picturesList']:
                arrayPictures.append(Picture(index=picture['index'], description=picture['pictureDescription']))
        else:
            arrayPictures = []

        # Subsections
        subTextArray = []
        if textsection['subsection']:
            for subsection in textsection['subsection']:
                subTextArray.append(Subsection(titleRaw=TextVariant(text=subsection['title']),
                                               textRaw=TextVariant(text=subsection['text'])))

        paperDB.content.append(Section(titleRaw=TextVariant(text=textsection['title']),
                                       textRaw=TextVariant(text=textsection['text']),
                                       subsection=subTextArray,tables=arrayTables, pictures=arrayPictures))

    paperDB.save()
    return paperDB
