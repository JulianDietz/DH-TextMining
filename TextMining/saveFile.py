#from .models import Metric,Text, Subsection, Reference, References, Paper, Author, Metadata, Authors, University, Abstract, \
#    Picture, Pictures, Table, Tables
from .models import Paper, Metadata, Author, University, Abstract, Table, Picture, TextVariant, Subsection, Section, \
    Reference


#mongo
#show dbs
#use textmining
#db.dropDatabase()

#db.paper.find()


def savePaper(paperJson):
    print('Paper in der Datenbank speichern')
    print(paperJson)

    paperDB = Paper()
    paperDB.title = paperJson['title']
    #AutorenListe
    if paperJson.get('authors'):
        for autor in paperJson['authors']['authorList']:
            paperDB.authors.append(Author(name=autor['authorName'], index=autor['authorIndex'],
                                           university=University(name=autor['university']['universityName'],
                                                        country=autor['university']['universityCountry'])))

    #Metadaten
    if paperJson['metaData']:
        if paperJson['metaData'].get('keywords'):
            keywords = paperJson['metaData']['keywords']
        else:
            keywords = []

        paperDB.metaData = Metadata(yearOfArticle=paperJson['metaData']['yearOfArticle'],
                                    category=paperJson['metaData']['category'],
                                    source=paperJson['metaData']['source'],
                                    journalTitle=paperJson['metaData']['journaltitle'],
                                    impactfactor=paperJson['metaData']['impactFactor'],
                                    URL=paperJson['metaData']['URL'],
                                    paperType=paperJson['metaData']['paperType'],
                                    keywords=keywords)

    #Abstract
    # TODO <<empty>>?
    for abstractPart in paperJson['abstract']:
        paperDB.abstract.append(Abstract(titleRaw=TextVariant(text=abstractPart['title']), textRaw=TextVariant(text=abstractPart['text'])))

    #References
    #TODO year integer?
    if paperJson.get('references'):
        for reference in paperJson['references']['referencesList']:
            paperDB.references.append(Reference(index=reference['referenceIndex'],
                                                               name=reference['referenceName'],
                                                               author=reference['referenceAuthor'],
                                                               year=str(reference['referenceYear'])))

    #Content
    for textsection in paperJson['text']:
        #TABLEs
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

        #Subsections
        subTextArray = []
        if textsection['subsection']:
            for subsection in textsection['subsection']:
                subTextArray.append(Subsection(titleRaw=TextVariant(text=subsection['title']),
                                               textRaw=TextVariant(text=subsection['text'])))

        paperDB.content.append(Section(titleRaw=TextVariant(text=textsection['title']), textRaw=TextVariant(text=textsection['text'])))#,
                                     #subsection=subTextArray,tables=arrayTables, pictures=arrayPictures))

    paperDB.save()
    return paperDB