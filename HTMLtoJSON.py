from bs4 import BeautifulSoup
from os import listdir,path
from os.path import isfile, join,basename

import json
import re


EMPTYJSONTAG = ""


# Wandelt HTML-Datei in JSON-Datei um
def parseHTML():
    htmlfilesdirectory = 'CorpusRaw'
    outputdirectory = 'OutputJSON'
    source = 'omics'
    categoryArray=[]
    readpathbasic=path.join(htmlfilesdirectory,source)
    for categoryFolder in listdir(readpathbasic):
        if categoryFolder !=".DS_Store":
            test = 0
            readpath=path.join(readpathbasic,categoryFolder)
            for file in listdir(readpath):
                if isfile(join(readpath, file)) and file.endswith('.html') and test<=2:
                    file = open(join(readpath, file))
                    try:
                        htmlfile = BeautifulSoup(file, 'html.parser')
                        output = {}
                        htmlarticle = htmlfile.article
                        if not htmlarticle:
                            continue
                        titel=getTitel(htmlarticle)
                        if titel==EMPTYJSONTAG:
                            continue
                        output['metaData']= getMetadata(htmlfile,categoryFolder,source)
                        output['abstract'] = getAbstract(htmlarticle)
                        output['authors'] = getAuthors(htmlarticle)
                        output['references'] = getallReferences(htmlarticle)
                        text=getSelectionText(htmlfile)
                        if text==EMPTYJSONTAG:
                            continue
                        output['text'] = text
                        name = path.splitext(basename(file.name))[0]
                        with open(join(outputdirectory, name + '.json'), 'w') as f:
                            json.dump(output, f, ensure_ascii=False)
                    except:
                        print("Paper failed!")
        categoryArray.append(categoryFolder)


def readJsonFiles():
    outputdirectory = 'output'
    for file in listdir(outputdirectory):
        name = path.splitext(basename(file))[0]
        file = open(join(outputdirectory, name + '.json'), 'r')
        jsonfile = json.load(file)


def getTitel(htmlArticle):
    if htmlArticle.find("h1"):
        title=htmlArticle.find("h1").text
        return title
    else:
        return EMPTYJSONTAG

def getallReferences(htmlArticle):
    references = {"count": 0, "referencesList": []}
    referencesElement = htmlArticle.find_all("li", id="Reference_Titile_Link")  # .next_element
    if (referencesElement):
        for reference in referencesElement:
            matchYear = re.search(r'[(][0-9]{4}[a-z]?[)]', str(reference))
            refYear = EMPTYJSONTAG
            if matchYear:
                refYear = str(matchYear.group())[1:-1]
            refAuthorName = EMPTYJSONTAG
            for el in reference.contents:
                if "<" not in str(el):
                    refAuthorNameMatch = re.search(r'[A-Za-z,\s]*',str(el))
                    refAuthorName = refAuthorNameMatch.group(0)
            references["count"] += 1
            referenceSubArray = reference.find_all("a")
            referenceIndex = ""
            for a in referenceSubArray:
                if "id" in a:
                    referenceIndex = int(a['d'])
            referenceData ={"referenceIndex": int(reference["value"]), "referenceName": str(reference.contents[-1].string), "referenceAuthor": refAuthorName, "referenceYear": refYear}
            references["referencesList"].append(referenceData)
    return references

def getKeywords(htmlfile):
    keywords=[]
    for div in htmlfile.findAll('strong'):
            if div.text and div.text == "Keywords:":
                text=div.text
                keywordsArray = div.parent.text.replace(text,"").strip()
                keywords=keywordsArray.split(";")
                keywords= [keyword.strip(' ') for keyword in keywords]
                break
            else:
                keywords=[EMPTYJSONTAG]
    return keywords

def getJournalTitle (htmlfile):
    journalTitle = EMPTYJSONTAG
    titleEl = htmlfile.find("meta" ,{"name":"citation_journal_title"})
    if titleEl != None and titleEl != -1:
       journalTitle = titleEl['content']
    return journalTitle

def getPaperType (htmlArticle):
    paperType = EMPTYJSONTAG
    container = htmlArticle.find("div", {"class": "col-xs-12 col-sm-9"})
    if container != -1 and container != None:
        paperType = str(container.ul.li.contents[0]).strip()
    return paperType

def getPaperURL (htmlfile):
    url = EMPTYJSONTAG
    urlEl = htmlfile.find("link", {"rel":"canonical"})

    if urlEl != None and urlEl != -1:
        url = str(urlEl["href"])

    return url

def getYear(htmlfile):
    year = "2018"
    yearEl=htmlfile.find("meta", {"name": "citation_year"})
    if yearEl != None and yearEl != -1:
        year = str(yearEl["content"])
    return year

def getMonth(htmlfile):
    month = EMPTYJSONTAG
    monthEl=htmlfile.find("meta", {"name": "citation_publication_date"})
    if monthEl != None and monthEl != -1:
        month = str(monthEl["content"]).split("/")[1]
    return month

def getPages(htmlfile):
    pages = EMPTYJSONTAG
    pagesEl1=htmlfile.find("meta", {"name": "citation_firstpage"})
    pagesEl2 = htmlfile.find("meta", {"name": "citation_lastpage"})
    if pagesEl1 != None and pagesEl1 != -1 and pagesEl2 != None and pagesEl2 != -1:
        pages = str(pagesEl1["content"]) + "-" + str(pagesEl2["content"])
    return pages

def getDOI(htmlfile):
    DOI = EMPTYJSONTAG
    DOIEl=htmlfile.find("meta", {"name": "citation_doi"})
    if DOIEl != None and DOIEl != -1:
        DOI = str(DOIEl["content"])
    return DOI

def getVolume(htmlfile):
    Volume = EMPTYJSONTAG
    VolumeEl=htmlfile.find("meta", {"name": "citation_volume"})
    if VolumeEl != None and VolumeEl != -1:
        Volume = str(VolumeEl["content"])
    return Volume

def getIssue(htmlfile):
    Issue = EMPTYJSONTAG
    IssueEl=htmlfile.find("meta", {"name": "citation_doi"})
    if IssueEl != None and IssueEl != -1:
        Issue = str(IssueEl["content"])
    return Issue

def getImpactFactor(htmlfile):
    impactFactor=htmlfile.find('meta' ,{'name':'journal_impact_factor'})['content']
    if impactFactor.strip()=="-" or impactFactor.strip()=="" or impactFactor==None:
        impactFactor=EMPTYJSONTAG
    return impactFactor

def getAbstractText(abstract):
    result = []
    text = ""
    titel = ""
    for tag in abstract.findAll():
        if tag.name=="strong":
            #doppelt conclusion
            if tag.parent.name!="strong":
                if titel == "" and tag.text!=":":
                    titel=tag.text
                    if tag.next_sibling and tag.next_sibling.name != "br" and tag.next_sibling.name != "em" and tag.next_sibling.name != "a": #:
                        text=tag.next_sibling
                elif tag.text!=":" and tag.text!=None:

                    titel=titel.strip().replace(":","")
                    text=text.strip()
                    result.append({"title":titel,"text":text,"depth":1})
                    if tag.find("strong"):
                        tag=tag.find("strong")
                    titel=tag.text
                    if tag.next_sibling:
                        if tag.next_sibling.name != "br" and tag.next_sibling.name != "a":  #:
                            if tag.next_sibling.name!="strong" and tag.text!=":":
                                text = tag.next_sibling
                        elif tag.next_sibling.name == "em" or tag.next_sibling.name == "em" :
                            text=tag.next_sibling.getText()
                        else:
                            text=tag.next_sibling.text
                    else:
                        text = tag.parent.next_sibling
                else:
                    text = tag.next_sibling
        else:
            if tag.name !=None and tag.name !='p' and tag.name !='br':
                if tag.name =="a" or tag.name =="span" or (tag.name=="em" and tag.parent.name!="span") and tag.name!="sup":
                    text=str(text)+str(tag.getText())
                    if tag.next_sibling:
                        text=str(text)+str(tag.next_sibling)
                elif tag.next_sibling and not tag.next_sibling.name:
                    text = str(text) + str(tag.next_sibling)

            #test br im Absatz
            elif tag.name =='br' and tag.next_sibling and tag.next_sibling.name==None:
                text=str(text)+str(tag.next_sibling)
            elif tag.name =='p' and tag.next_sibling and tag.next_sibling.name==None:
                text=str(text)+str(tag.next_sibling)

    result.append({"title": titel, "text": text, "depth": 1})
    return result

def getAbstract(htmlArticle):
    div=None
    for div in htmlArticle.findAll('div'):
        if div.find('h3'):
            container=div.find('h3')
            if container.text and container.text=="Abstract":
                break
    if div and div.find('p'):
        abstract = div.find('p').find('p')
    else:
        return [{'title': EMPTYJSONTAG, 'text': EMPTYJSONTAG}]

    if abstract:
        #Absätze mit überschriften
        list = []
        if abstract.find('strong'):
            list = getAbstractText(abstract)
        #Absätze ohne überschriften
        else:
            list.append({'title':EMPTYJSONTAG,'text':abstract.getText(),'depth':1})
    else:
        list = [{'title': EMPTYJSONTAG, 'text': EMPTYJSONTAG}]
    return list

def getMetadata(htmlfile,category,source):
    output={}
    output['keywords']=getKeywords(htmlfile)
    output['yearOfArticle']=getYear(htmlfile)
    output['journaltitle']=getJournalTitle(htmlfile)
    output['impactFactor'] = getImpactFactor(htmlfile)
    output['category']=[category]
    output['source']={"sourceName": source, "URL": getPaperURL(htmlfile)}
    output['paperType'] = getPaperType(htmlfile)
    output['title'] = getTitel(htmlfile.article)
    output['month'] = getMonth(htmlfile)
    output['language'] = "english"
    output['volume'] = getVolume(htmlfile)
    output['issue'] = getIssue(htmlfile)
    output['pages'] = getPages(htmlfile)
    output['edition'] = 1
    output['publisher'] = "OMICS International"
    output['booktitle'] = EMPTYJSONTAG
    output['location'] = "Online"
    output['organisation'] = "OMICS International"
    output['address'] = EMPTYJSONTAG
    output['id'] = 1
    output['publicationtype'] = "Online"
    output['chapter'] = EMPTYJSONTAG
    output['doi'] = getDOI(htmlfile)
    return output

def getAuthors(htmlArticle):
    authorsOutput = {'count': None, 'authorList': []}
    authorListHTML = htmlArticle.dl.dt.find_all('a')

    index = 0
    for authorEl in authorListHTML:
        author = {}
        if authorEl.has_attr('title'):
            author['authorName'] = authorEl['title'].strip()
            author['authorIndex'] = index = index + 1

            finding = authorEl.next_element.next_element.find('a')

            #Autoren sind nummeriert
            if finding != None and finding != -1 and authorEl.next_sibling and "contents" in finding and str(finding.contents[0]) != '*':
                universityIndex = authorEl.next_element.next_element.a.string
                university = htmlArticle.dl.find('dd', id="a" + universityIndex)
                universityCountry = str(university.contents[-1]).split(',')[-1].strip()
                if university.find('a', title=True):
                    universityName = str(university.find('a', href=True)['title'])
                else:
                    universityName = str(university.contents[-1].split(',')[0] + ", " + str(university.contents[-1].split(',')[1]))
            # All authors are from the same university therefore no numbers
            else:
                university = htmlArticle.dl.find('dd', id="a1")
                universityCountry = str(university.contents[-1]).replace(",","").strip()
                if university.find('a', title=True) != None and university.find('a', title=True) != -1:
                    if university.find('a', href=True).has_attr("title"):
                        universityName = str(university.find('a', href=True)['title'])
                    else:
                        universityName = str(university.find('a', href=True).contents)

                else:
                    universityName = str(university.contents[0]).split(',')[0]

            author['university'] = {"universityName": universityName, "universityCountry": universityCountry}
            authorsOutput['authorList'].append(author)
            authorsOutput['count'] = index

    return authorsOutput

def getSelectionText(htmlArticle):
    h4array=[]
    subsection=[]
    title=""
    text=""
    if htmlArticle.find("h4"):
        for section in htmlArticle.findAll("h4"):
            if section.text=="References":
                continue
            if title!="":
                dataImages=getImages(section.findNext())
                dataTables = getTables(section.findNext())
                h4array.append({"title": title, "text": text, 'depth': 1, 'subsection':subsection,'tables':dataTables,'pictures':dataImages})
            subsection = []
            title = section.text
            text = ""
            innertitle = ""
            innertext = ""
            subsectionfound=False

            for element in section.findNext():
                if element.name == 'p' and not element.find("strong"):
                    if subsectionfound:
                        innertext+=element.get_text()
                    else:
                        text=text+element.get_text()

                elif element.name == 'p' and element.find("strong") and not element.find("strong")==-1:
                    # none wenns vorkommt -1 wenn nicht
                    if element.contents[0].find("strong")!=-1 :
                        if "Table" not in element.find("strong").text and "Figure" not in element.find("strong").text:
                            subsectionfound = True
                            if innertitle != "" and innertext != "":
                                subsection.append({"title": innertitle, "text": innertext, 'depth':2,'subsection': []})
                            innertitle = element.find("strong").text
                            innertext = ""
                        else:
                            if ":" not in element.find("strong").text:
                                if subsectionfound:
                                    innertext += element.get_text()
                                else:
                                    text += element.get_text()

                    else:
                        if subsectionfound:
                            innertext += element.get_text()
                        else:
                            text += element.get_text()
            if innertitle!="" or innertext!="":
                subsection.append({"title": innertitle, "text": innertext, 'depth': 2, 'subsection': []})


        dataImages = getImages(section.findNext())
        dataTables = getTables(section.findNext())
        h4array.append({"title": title, "text": text, 'depth': 1, 'subsection': subsection, 'tables': dataTables,
                        'pictures': dataImages})
    else:
        #Artikel hat keine Überschift!
        #soll nicht in datenbank
        return EMPTYJSONTAG
    return h4array

def getTables(section):
    sectionTableData = {"count": 0, "tablesList": []}
    tableListHTML = section.find_all("div", class_="table-responsive")
    for table in tableListHTML:
        if table != None:
            sectionTableData['count'] += 1
            description = EMPTYJSONTAG

            rows = len(table.find_all("tr"))

            cols = 0
            if table.find("tr") != None and table.find("tr")!= -1:
                colsArray = table.find("tr").contents

                while '\n' in colsArray:
                    colsArray.remove('\n')

                cols = len(colsArray)

            tableData = {"index": sectionTableData['count'], "tableRowDim": rows, "tableColDim": cols, "tableDescription": description}
            sectionTableData['tablesList'].append(tableData)

    return sectionTableData

def getImages(section):
    sectionPictureData = {"count": 0, "picturesList": []}
    regex = re.compile("<[\/]*[a-z]+>", re.IGNORECASE)
    pictureListHTML = section.find_all("div", class_="card card-block card-header mb-2")

    for picture in pictureListHTML:
        sectionPictureData['count'] += 1
        description = EMPTYJSONTAG

        descriptionEl = picture.find("div", class_="col-xs-12 col-sm-10 col-md-9")
        if descriptionEl != None and descriptionEl != -1:
            description = str(descriptionEl.p)


            while re.search(regex, description) != None:
                description = regex.sub("", description)

        pictureData = {"index": sectionPictureData['count'], "pictureDescription": description}
        sectionPictureData['picturesList'].append(pictureData)
    return sectionPictureData

def getFormula(section):
    sectionFormulaData = {"count": 0, "formulaList": []}

    formulaListHTML = section.find_all("img")
    for formula in formulaListHTML:
        sectionFormulaData['count'] += 1
        sourceLink = EMPTYJSONTAG

        pictureData = {"index": sectionFormulaData['count'], "formulaSource": sourceLink}
        sectionFormulaData['formulaList'].append(pictureData)

    return sectionFormulaData

parseHTML()