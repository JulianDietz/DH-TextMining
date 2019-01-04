from django.db import models

# Create your models here.
from mongoengine import *

# http://docs.mongoengine.org
connect('textmining')

# TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!! TEXT VARIANT !!!
class TextVariant(EmbeddedDocument):
    text = StringField()
    method = StringField()

# METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!! METRIK RESULTS !!!


class ResCharSegmentCount(EmbeddedDocument):
    charCountWhiteSpace = StringField(default= "0")
    charCountNoWhiteSpace = StringField(default = "0")

class ResWordSegmentCount(EmbeddedDocument):
    wordCount = StringField(default= "0")

class ResPunctSegmentCount(EmbeddedDocument):
    punctCount = StringField(default= "0")

class ResCitationSegmentCount(EmbeddedDocument):
    citationCount = StringField(default= "0")



class Metric(EmbeddedDocument):
    charCountResults = EmbeddedDocumentField('ResCharSegmentCount')
    wordCountResults = EmbeddedDocumentField('ResWordSegmentCount')
    punctCountResults = EmbeddedDocumentField('ResPunctSegmentCount')
    citationCountResults = EmbeddedDocumentField('ResCitationSegmentCount')
    sentslengthAverage = FloatField()


class Tables(EmbeddedDocument):
    count = IntField()
    tablesList = EmbeddedDocumentListField('Table')


class Table(EmbeddedDocument):
    tableIndex = IntField()
    tableRowDim = IntField()
    tableCodDim = IntField()
    tableDescription = StringField()


class Pictures(EmbeddedDocument):
    count = IntField()
    picturesList = EmbeddedDocumentListField('Picture')


class Picture(EmbeddedDocument):
    pictureIndex = IntField()
    pictureDescription = StringField()


class Subsection(EmbeddedDocument):
    title = StringField()
    text = StringField()
    stopFilteredText = EmbeddedDocumentField('TextVariant')
    lemmatizedText = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null = True)
    subsubsection = ListField()


class Text(EmbeddedDocument):
    title = StringField()
    text = StringField()
    stopFilteredText = EmbeddedDocumentField('TextVariant')
    lemmatizedText = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null = True)
    subsection = EmbeddedDocumentListField('Subsection')
    tables = EmbeddedDocumentField('Tables')
    pictures = EmbeddedDocumentField('Pictures')
    formulas = StringField()  # String weil leer und nicht 0



class Reference(EmbeddedDocument):
    referenceIndex = IntField()
    referenceName = StringField()
    referenceAuthor = StringField()
    referenceYear = StringField()


class References(EmbeddedDocument):
    count = IntField()
    referencesList = EmbeddedDocumentListField('Reference')


class University(EmbeddedDocument):
    university_universityName = StringField()
    university_universityCountry = StringField()


class Author(EmbeddedDocument):
    authorName = StringField()
    authorIndex = IntField()
    university = EmbeddedDocumentField('University')


class Authors(EmbeddedDocument):
    count = IntField()
    authorList = EmbeddedDocumentListField('Author')


class Abstract(EmbeddedDocument):
    title = StringField()
    text = StringField()
    stopFilteredText = EmbeddedDocumentField('TextVariant')
    lemmatizedText = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null = True)


class Metadata(EmbeddedDocument):
    keywords = ListField()
    yearOfArticle = IntField()
    category = StringField()
    source = StringField()
    journalTitle = StringField()
    impactfactor = StringField()
    URL=StringField()
    paperType=StringField()
    # Erweiterungen
    documenttype = StringField()
    publisher = StringField()
    publishingCompany = StringField()
    pages = IntField()
    excerptPages = StringField()
    publicationLocation = StringField()


class Paper(Document):
    title = StringField()
    metaData = EmbeddedDocumentField('Metadata')
    abstract = EmbeddedDocumentListField('Abstract')
    authors = EmbeddedDocumentField('Authors')
    references = EmbeddedDocumentField('References')
    text = EmbeddedDocumentListField('Text')
