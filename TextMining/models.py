from django.db import models

# Create your models here.
from mongoengine import *

# http://docs.mongoengine.org
connect('textmining')

class BibtexFields(EmbeddedDocument):
    citekey = StringField()
    entrytype = StringField()
    title = StringField()
    #author = StringField()
    year = StringField()
    month = StringField()
    journal = StringField()
    booktitle = StringField()
    publisher = StringField()
    volume = StringField()
    number = StringField()
    pages = StringField()
    #note = StringField()
    #keywords = StringField()
    url = StringField()
    #code = StringField()
    #pdf = StringField()
    #image = StringField()
    #thumbnail = StringField()
    #doi = StringField()
    #external = StringField()
    #abstract = StringField()
    #isbn = StringField()
    editor = StringField()
    series = StringField()
    address = StringField()
    edition = StringField()
    organization = StringField()
    type = StringField()
    chapter = StringField()
    howpublished = StringField()
    location = StringField()


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
    bibtexData = EmbeddedDocumentField('BibtexFields')


class Paper(Document):
    title = StringField() # in raw und nltkstw
    metaData = EmbeddedDocumentField('Metadata')
    authors = EmbeddedDocumentListField('Authors')
    references = EmbeddedDocumentListField('References')
    abstract = EmbeddedDocumentListField('Abstract')
    content = EmbeddedDocumentListField('Section')
