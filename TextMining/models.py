from django.db import models

# Create your models here.
from mongoengine import *

# http://docs.mongoengine.org
connect('textmining')


class Metric(EmbeddedDocument):
    charCountWhiteSpace = StringField()
    charCountNoWhiteSpace = StringField()
    wordCount = StringField()
    punctCount = StringField()
    citationCount = StringField()



class Tables(EmbeddedDocument):
    index = IntField()
    rowDim = IntField()
    codDim = IntField()
    description = StringField()


class Pictures(EmbeddedDocument):
    index = IntField()
    description = StringField()


class Subsection(EmbeddedDocument):
    titleRaw = EmbeddedDocumentField('TextVariant')
    titleNltkStw = EmbeddedDocumentField('TextVariant')
    textRaw = EmbeddedDocumentField('TextVariant')
    textNltkStw = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null=True)
    subsubsection = EmbeddedDocumentListField('Subsection') # nicht implementiert

class TextVariant(EmbeddedDocument):
    text = StringField()
    metrik = EmbeddedDocumentField('Metric', null=True)

class Section(EmbeddedDocument):
    titleRaw = EmbeddedDocumentField('TextVariant')
    titleNltkStw = EmbeddedDocumentField('TextVariant')
    textRaw = EmbeddedDocumentField('TextVariant')
    textNltkStw = EmbeddedDocumentField('TextVariant')
    subsection = EmbeddedDocumentListField('Subsection')
    tables = EmbeddedDocumentListField('Tables')
    pictures = EmbeddedDocumentListField('Pictures')


class References(EmbeddedDocument):
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
    title = StringField()
    text = StringField()
    stopFilteredText = EmbeddedDocumentField('TextVariant')
    lemmatizedText = EmbeddedDocumentField('TextVariant')
    metrik = EmbeddedDocumentField('Metric', null=True)


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
    title = StringField() # in raw und nltkstw
    metaData = EmbeddedDocumentField('Metadata')
    authors = EmbeddedDocumentListField('Authors')
    references = EmbeddedDocumentListField('References')
    abstract = EmbeddedDocumentListField('Abstract')
    content = EmbeddedDocumentListField('Section')
