from django.db import models

# Create your models here.
from mongoengine import *

# http://docs.mongoengine.org
connect('textmining')


class Metric(EmbeddedDocument):
    charCountWhiteSpace = IntField()
    charCountNoWhiteSpace = IntField()
    wordCount = IntField()
    punctCount = IntField()
    citationCount = IntField()



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
    textRaw = EmbeddedDocumentField('TextVariant')
    textNltkStw = EmbeddedDocumentField('TextVariant')
    #metrik = EmbeddedDocumentField('Metric', null=True)
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
    textRaw = EmbeddedDocumentField('TextVariant')
    textNltkStw = EmbeddedDocumentField('TextVariant')


class Metadata(EmbeddedDocument):
    keywords = ListField()
    yearOfArticle = IntField()
    category = ListField()
    source = StringField()
    impactfactor = StringField()
    URL=StringField()
    paperType=StringField()
    language = StringField()
    publicationtype=StringField()#online oder paper
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


class Paper(Document):
    titleRaw = EmbeddedDocumentField('TextVariant')
    titleNltkStw = EmbeddedDocumentField('TextVariant')
    metaData = EmbeddedDocumentField('Metadata')
    authors = EmbeddedDocumentListField('Author')
    references = EmbeddedDocumentListField('Reference')
    abstract = EmbeddedDocumentListField('Abstract') # TODO EmbeddedDocumentField machen, oder gibts echt mal mehr als ein Abstract? JA mehr als eins
    content = EmbeddedDocumentListField('Section')
