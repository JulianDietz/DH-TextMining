from mongoengine import *


connect('textmining')


class Metric(EmbeddedDocument):
    charCountWhiteSpace = IntField()
    charCountNoWhiteSpace = IntField()
    wordCount = IntField()
    punctCount = IntField()
    citationCount = IntField()
    averageWordLength = FloatField()
    averageSentenceLength = FloatField()


class Table(EmbeddedDocument):
    index = IntField()
    rowDim = IntField()
    codDim = IntField()
    description = StringField()


class Picture(EmbeddedDocument):
    index = IntField()
    description = StringField()


class Subsection(EmbeddedDocument):
    titleRaw = EmbeddedDocumentField('TextVariant')
    titleNltkStw = EmbeddedDocumentField('TextVariant')
    titleNltkStem = EmbeddedDocumentField('TextVariant')
    textRaw = EmbeddedDocumentField('TextVariant')
    textNltkStw = EmbeddedDocumentField('TextVariant')
    textNltkStem = EmbeddedDocumentField('TextVariant')
    subsubsection = EmbeddedDocumentListField('Subsection') # Nicht implementiert


class TextVariant(EmbeddedDocument):
    text = StringField()
    metrik = EmbeddedDocumentField('Metric', null=True)

class Section(EmbeddedDocument):
    titleRaw = EmbeddedDocumentField('TextVariant')
    titleNltkStw = EmbeddedDocumentField('TextVariant')
    titleNltkStem = EmbeddedDocumentField('TextVariant')
    textRaw = EmbeddedDocumentField('TextVariant')
    textNltkStw = EmbeddedDocumentField('TextVariant')
    textNltkStem = EmbeddedDocumentField('TextVariant')
    subsection = EmbeddedDocumentListField('Subsection')
    tables = EmbeddedDocumentListField('Table')
    pictures = EmbeddedDocumentListField('Picture')


class Reference(EmbeddedDocument):
    index = IntField()
    name = StringField()
    author = StringField()
    year = StringField()


class University(EmbeddedDocument):
    name = StringField()
    country = StringField()


class Author(EmbeddedDocument):
    name = StringField()
    index = IntField()
    university = EmbeddedDocumentField('University')


class Abstract(EmbeddedDocument):
    titleRaw = EmbeddedDocumentField('TextVariant')
    titleNltkStw = EmbeddedDocumentField('TextVariant')
    titleNltkStem = EmbeddedDocumentField('TextVariant')
    textRaw = EmbeddedDocumentField('TextVariant')
    textNltkStw = EmbeddedDocumentField('TextVariant')
    textNltkStem = EmbeddedDocumentField('TextVariant')


class Metadata(EmbeddedDocument):
    keywords = ListField()
    yearOfArticle = IntField()
    category = ListField()
    source = StringField()
    impactfactor = StringField()
    URL=StringField()
    paperType=StringField()
    language = StringField()
    publicationtype=StringField()
    #Bibtexfelder
    citekey = StringField()
    entrytype = StringField()
    title = StringField()
    year = StringField()
    month = StringField()
    journal = StringField()
    booktitle = StringField()
    publisher = StringField()
    volume = StringField()
    issue = StringField()
    pages = StringField()
    # note = StringField()
    # keywords = StringField()
    url = StringField()
    # code = StringField()
    # pdf = StringField()
    # image = StringField()
    # thumbnail = StringField()
    doi = StringField()
    # external = StringField()
    # abstract = StringField()
    # isbn = StringField()
    editor = StringField()
    series = StringField()
    address = StringField()
    edition = StringField()
    organization = StringField()
    type = StringField()
    chapter = StringField()
    howpublished = StringField()
    location = StringField()


class TotalValues(EmbeddedDocument):
    totalPaper = FloatField()
    totalAbstractTitles = FloatField()
    totalAbstractText = FloatField()
    totalSectionTitles = FloatField()
    totalSectionText = FloatField()
    totalSubsectionTitles = FloatField()
    totalSubsectionText = FloatField()


class TotalValuesForAveragedMetriks(EmbeddedDocument):
    totalsAverageSentenceLengthRaw = EmbeddedDocumentField('TotalValues')
    totalsAverageSentenceLengthNltkStw = EmbeddedDocumentField('TotalValues')
    totalsAverageSentenceLengthNltkStem = EmbeddedDocumentField('TotalValues')
    totalsAverageWordLengthRaw = EmbeddedDocumentField('TotalValues')
    totalsAverageWordLengthNltkStw = EmbeddedDocumentField('TotalValues')
    totalsAverageWordLengthNltkStem = EmbeddedDocumentField('TotalValues')


class Paper(Document):
    titleRaw = EmbeddedDocumentField('TextVariant')
    titleNltkStw = EmbeddedDocumentField('TextVariant')
    titleNltkStem = EmbeddedDocumentField('TextVariant')
    metaData = EmbeddedDocumentField('Metadata')
    authors = EmbeddedDocumentListField('Author')
    references = EmbeddedDocumentListField('Reference')
    abstract = EmbeddedDocumentListField('Abstract')
    content = EmbeddedDocumentListField('Section')
    totalValuesForAveragedMetriks = EmbeddedDocumentField('TotalValuesForAveragedMetriks')
    isRehashed = BooleanField()

