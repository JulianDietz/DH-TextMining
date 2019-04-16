from bs4 import BeautifulSoup
import requests
import os

# Der Crawler holt nach deren Kategorien geoordnet alle Paper aus dem OMICS-Online Archiv aus dem Jahr 2018
def getJournalsFromCategoriesPage(categoryurl,categoryName):
    r = requests.get(categoryurl)
    journalpage = BeautifulSoup(r.text, 'html.parser')
    for journal in journalpage.findAll('td', attrs={'valign': 'middle'}):
        journallink=journal.find('a')
        if journallink:
            impactFactor=None
            impactFactor=journal.parent.findAll('td')[1]
            if impactFactor:
                impactFactor=impactFactor.contents[0]
            else:
                impactFactor="<<empty>>"
            getArchiveList(journallink['href'],categoryName,impactFactor)

def getArchiveList(journallink,categoryName,impactFactor):
    r = requests.get(journallink)
    journalpage = BeautifulSoup(r.text, 'html.parser')
    for listitem in journalpage.findAll('li',{"class": "nav-item"}):
        link=listitem.find('a')
        if link.text=="Archive":
            getPaperlist(link['href'],categoryName,impactFactor)


def getPaperlist(journalarchive,categoryName,impactFactor):
    r = requests.get(journalarchive)
    journalarchive = BeautifulSoup(r.text, 'html.parser')
    for year in journalarchive.findAll('h6',{"class": "card-header p-2"}):
        card=year.find('strong')
        if card.text=="2018":
            for paperlistlink in year.parent.find('nav').findAll('a'):
                savePaper(paperlistlink['href'],categoryName,impactFactor)


def savePaper(paperlistlink,categoryName,impactFactor):
    r = requests.get(paperlistlink)
    paperlist = BeautifulSoup(r.text, 'html.parser')
    for paperEntry in paperlist.findAll('div',{'class':"row"}):
        for link in paperEntry.findAll('a'):
            if link.text=="Peer-reviewed Full Article":
                global outpath
                r = requests.get(link['href'])
                fullpath=os.path.join(outpath,categoryName)
                if not os.path.exists(fullpath):
                    os.makedirs(fullpath)
                name=link['href'].split('/')[len(link['href'].split('/'))-1]
                file=open(os.path.join(fullpath,name), 'w', encoding="utf-8")
                validHTML=resolveHTMLError(r.text)
                validHTML='<meta name="journal_impact_factor" content='+impactFactor+'/>'+validHTML
                file.write(str(validHTML))
                file.close()

def runCrawler():
    r = requests.get('https://www.omicsonline.org')
    htmlfile = BeautifulSoup(r.text, 'html.parser')
    for titel in htmlfile.findAll('h6'):
        if titel.text == "Journals by Subject":
            for category in titel.parent.parent.findAll('a'):
                getJournalsFromCategoriesPage(category['href'],category['title'])

def resolveHTMLError(invalidHTML):
    validHTML = invalidHTML.replace('</dt>\n</dl>','</div>')
    return validHTML

source='omics'
outdir='CorpusRaw'
outpath=os.path.join(outdir, source)
runCrawler()