#python app.py 8080

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import web
from datetime import datetime 
import rdlsc_ieeexplorer as ieee
import rdlsc_scopus as scopus
import rdlsc_tf_idf as tfidf
import rdlsc_manager_db as rdlsc_db
from collections import defaultdict 
from rdlsc_util import cfgApp as cfg
import rdlsc_fastText
import rdlsc_util
import rdlsc_nltk
import os

urls = (
  '/', 'index',
  '/slr', 'slr',
  '/updClassification','updClassification',
  '/getWordsSimilar','getWordsSimilar',
  '/generateLogAnalyse', 'generateLogAnalyse'
)

render = web.template.render('templates/', base="layout")

# Process favicon.ico requests
class icon:
    def GET(self): raise web.seeother("/templates/favicon.ico")

def getSLRdb():
    return rdlsc_db.slrDB(cfg.fileDB)

def getResearchs():
    slr = getSLRdb()
    slr.createTables()
    res = slr.getAllResearch()
    slr.closeCon()
    return res

def getResearch(i):
    slr = getSLRdb()
    research = slr.getResearch(i)
    slr.closeCon()
    return research

def getSearch(i):
    slr = getSLRdb()
    searchSLR = slr.findSearch(i)
    slr.closeCon()    
    return searchSLR

def getDocsSearch(i):
    slr = getSLRdb()
    docs = slr.getDocumentsBySearch(i)
    slr.closeCon()
    return docs
            
def delete(table,i):
    slr = getSLRdb()
    
    if table =='research':
        deleted = slr.deleteResearch(i)
    if table == 'search':
        deleted = slr.deleteSearch(i)

    if table == 'document':
        deleted = slr.deleteDocInSearch(i)

    slr.closeCon()
    return deleted

def updDocument(idDoc, classific):
    slr = getSLRdb()
    d = slr.findDocument(idDoc)
    doc = rdlsc_db.DocumentInSearchSLR (d[0], d[1], d[2], d[3], d[4], d[5], classific, d[7], d[8])
    updated = slr.updateDocumentInSearch(doc)
    slr.closeCon()
    return updated

def getDocumentById(idDoc):
    slr = getSLRdb()
    d = slr.findDocument(idDoc)
    doc = rdlsc_db.DocumentInSearchSLR (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
    slr.closeCon()
    return doc

def termsSearch(docs, ngram, amount):
    docsNone = ''
    docsInclude = ''
    docsExclude = ''
    for dC in docs:
        if dC.classification == 'N':
            docsNone = docsNone + ' ' + dC.title + ' ' + dC.abstract + ' ' + dC.keywords
        else:
            if dC.classification == 'I':
                docsInclude = docsInclude + ' ' + dC.title + ' ' + dC.abstract + ' ' + dC.keywords
            else:
                if dC.classification == 'E':
                    docsExclude = docsExclude + ' ' + dC.title + ' ' + dC.abstract + ' ' + dC.keywords

    corpusDocsClassific = [docsNone, docsInclude, docsExclude]  
    terms = tfidf.getTFIDF (corpusDocsClassific, ngram, amount)
    return terms

def updTfIdfSearch(docs, search):
    if search:
        slr = getSLRdb()
        terms = termsSearch(docs, search.nGrams, search.amountFeatures)
        slr.updTfIdfInSearch(search.id, terms)
        slr.closeCon()

def getHTMLamount(sText, nCount, aCol):
    msg = ''
    par = "'',"
    if nCount >0:
        if sText == 'Exclude':
            par = "'NOT',"
        msg += '<p><b>TF-IDF (' + str(nCount) + " " + sText + "(s)): </b>"
        for t in eval(aCol):            
            msg += '<span class="word-tfIDF"><b> <a href="javascript:updInput(\'' + par + t[0] +'\')">'
            msg += t[0] + ' ' + "{0:12,.3f}".format(float(t[1])) + '</a></span>&nbsp';                        
        msg += '</p>'
    return msg


class index(object):
    
    def GET(self):        
        data = web.input()
        deleted = False
        try:
            delR = int(data.delR)
            if delR > 0:
                deleted = delete('research',delR)
        except:
            delR = 0
            
        try:
            delS = int(data.delS)
            if delS >= 0:
                deleted = delete('search',delS)
        except:
            delS = 0
        
        if deleted:
            msg = "Record deleted successfully."
        else:
            msg = ''

        researchs = getResearchs()
        return render.index(researchs = researchs, msg = msg )

    def POST(self):
        form = web.input(name="newResearch")
        nameNewResearch = "%s" % (form.nameNewResearch)
        repositoryNewResearch = "%s" % (form.repositoryNewResearch)

        slr = getSLRdb()
        researchSLR = rdlsc_db.ResearchSLR(0,nameNewResearch, datetime.now(), repositoryNewResearch)
        inserted = slr.insertResearch(researchSLR)
        slr.closeCon()
        if inserted:
            msg = "Research inserted successfully."
        else:
            msg = ''                
        return render.index(researchs = getResearchs(), msg = msg)

def getFT(idResearch, idSearch):
    fileData = "./tmp/data_" + str(idResearch)+ "_" + str(idSearch) + ".txt"
    if os.path.isfile(fileData):
        rdlsc_ft = rdlsc_fastText.rdlsc_FastText(idResearch, idSearch)
        rdlsc_ft.makeModel('skip')
        rdlsc_ft.makeModel('cbow')
        return rdlsc_ft

def makeDataFile(idResearch, idSearch, docs):
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')
    #Create file for FastText
    with open("./tmp/data_" + str(idResearch)+ "_" + str(idSearch) + ".txt", "wb") as arq:
        line = ''
        for doc in docs:
            line += doc.title + '. ' + doc.abstract + '. ' + doc.keywords + '. '
        #print ('------abstract: ' + doc.abstract + '----------------\n\n')
        line = rdlsc_util.normalize_text(line)
        line = " ".join(line.split())
        arq.write(str(line).encode('utf-8', 'strict'))
        arq.close()

        #getFT(idResearch, idSearch)        
        
class slr(object):
    
    def GET(self):

        data = web.input()
        msg = ''
        
        deleted = False
        try:
            delDoc = int(data.delDoc)            
            if delDoc > 0:
                deleted = delete('document',delDoc)                
        except:
            delDoc = 0
                    
        if deleted:
            msg = "Document deleted successfully."        

        #data = web.input()
        idResearch = int(data.id)
        idSearch = int(data.idSearch)
        updSearchAfterDelete(idSearch)
        try:            
            search = getSearch(idSearch)
            docs = getDocsSearch(idSearch)            
            updTfIdfSearch(docs, search)
            search = getSearch(idSearch)
            search.tfIdfNone = eval(search.tfIdfNone)
            search.tfIdfInclude = eval(search.tfIdfInclude)
            search.tfIdfExclude = eval(search.tfIdfExclude)

            makeDataFile(idResearch, idSearch, docs) #Create file for FastText
            
        #except ZeroDivisionError:
        except:
            search = rdlsc_db.SearchSLR(0, 0, '', '', 'md', '', cfg.nGrams, cfg.features,
                                          0, 0, 0, 0, 0, '', '', '')
            docs = []
        
        return render.slr(search, docs, getResearch(idResearch), msg)
    
    def POST(self):
        form = web.input(name="search")
        form2 = web.input(name="settingsRDLSC")
        sS = "%s" % (form.searchString)
        searchIn = "%s" % (form.searchIn)                
        #ngram = int(form2.ngramsMax)
        #amount = int(form2.amountResources)
        ngram = cfg.nGrams
        amount = cfg.features
        idResearch = int(form.idResearch)
        research = getResearch(idResearch)
        msg = ''
        
        if research.repository == 'IEEE':
            resSearch = ieee.runSearch(sS, searchIn)
        else:
            if research.repository == 'Scopus':
                try:
                    resSearch = scopus.runSearch(sS)
                except:
                    resSearch = [[], 0, 0, 'Error in the Scopus Service. Try again later.']

        slr = getSLRdb()
        searchSLR = rdlsc_db.SearchSLR(0, idResearch, datetime.now(), sS, searchIn, resSearch[3],
                                         ngram, amount, resSearch[1], int(resSearch[1]), 0, 0, 0, '', '', '')
        slr.insertSearch(searchSLR)
        idSearch = slr.lastSearchByResearch(idResearch)[0]            
        slr.closeCon()
        terms = []
        search = getSearch(idSearch)

        if len(resSearch[0])>0:
            slr = getSLRdb()            
            ind = 0
            termsDoc = tfidf.getTFIDF (tfidf.getCorpus(resSearch[0]), ngram, amount)
            for d in resSearch[0]:
                doc = rdlsc_db.DocumentInSearchSLR (0, idSearch, d.id, d.title, d.abstract,
                                                      d.rank, 'N', termsDoc[ind], d.keywords)                                
                ind += 1
                slr.insertDocumentInSearch(doc, idResearch)
            
            docs = slr.getDocumentsBySearch(idSearch)

            slr.updAmountInSearch(idSearch)
            
            updTfIdfSearch(docs, search)
            slr.closeCon()

            search = getSearch(idSearch)
            search.tfIdfNone = eval(search.tfIdfNone)
            search.tfIdfInclude = eval(search.tfIdfInclude)
            search.tfIdfExclude = eval(search.tfIdfExclude)
            
            makeDataFile(idResearch, idSearch, docs) #Create file for FastText
        else:
            docs = []

        return render.slr(search, docs, research, msg)

def updSearch(idDoc):
    doc = getDocumentById(idDoc)
    slr = getSLRdb()
    docs = slr.getDocumentsBySearch(doc.search)            
    slr.updAmountInSearch(doc.search)
    slr.closeCon()
    search = getSearch(doc.search)
    updTfIdfSearch(docs, search)
    search = getSearch(doc.search)
    return search

def updSearchAfterDelete(idSearch):
    slr = getSLRdb()
    docs = slr.getDocumentsBySearch(idSearch)            
    slr.updAmountInSearch(idSearch)
    slr.closeCon()
    search = getSearch(idSearch)
    updTfIdfSearch(docs, search)    

class updClassification(object):
    
    def POST(self):                
        
        data = web.input()
        try: 
            idDoc = int(data.document)            
        except:
            idDoc = None
        try:    
            classific = str(data.classific)
        except:
            classific = None
            
        if idDoc and classific:
            updated = updDocument(idDoc, classific)
            msg = ''

            search = updSearch(idDoc)

            msg += getHTMLamount('None', search.amountNone, search.tfIdfNone)
            msg += getHTMLamount('Include', search.amountInclude, search.tfIdfInclude)
            msg += getHTMLamount('Exclude', search.amountExclude, search.tfIdfExclude)
	
        return msg

def arrayUnique(terms):
    termsUnique = []
    specialChar = '–ç!"#$%&\'()*+,./:;<=>?@©®-[\\]^_`{|}~“”1234567890ï¿½'
    #Remove duplicates
    for i in terms:
        # Replace specialChar                
        for c in list(specialChar):                    
            i = i.replace(c, ' ')
        i = i.rstrip()
        i = i.lstrip()
        if (i not in termsUnique) and (not i.isnumeric()) and (i.strip()!='') and (len(i.strip())>1):
            termsUnique.append(i)
    return termsUnique

def arrayWithoutNumber(array):
    newArray = []
    for i in array:
        if not i.isnumeric():
            newArray.append(i)
    return newArray

def htmlWords(txt, term, words):
    htmlAux = ''
    htmlAux += '<div class="dropdown"> <span class="word-normal">' 
    htmlAux += '<a href="javascript:updInput(\'\', \'' + txt + '\')">' + term + '</a>' + '</spam>&nbsp;'
    htmlAux += '<div class="dropdown-content"> '
    for w in words:
        htmlAux += '<a href="javascript:updInput(\'\', \'' + w+ '\')">' + w + '</a>'            

    htmlAux +=  '</div></div>'
    return htmlAux

def printForAnalisys(search, searchString, words2, wAux, wordsMF, wordsMFs):
    aNone = []
    aInclude = []
    aExclude = []            
    for w in eval(search.tfIdfNone):
        #if w in tNone_:
        aNone.append(w[0].strip()+' '+("{0:12,.3f}".format(float(w[1]))).strip())
    
    for w in eval(search.tfIdfInclude):
        #if w in tInclude_:
        aInclude.append(w[0].strip()+' '+("{0:12,.3f}".format(float(w[1]))).strip())

    for w in eval(search.tfIdfExclude):
        #if w in tExclude_:
        aExclude.append(w[0].strip()+' '+("{0:12,.3f}".format(float(w[1]))).strip())
        
    print ("\n\nResearch: " + getResearch(search.research).name + '\n')
    print ("Search String: \n" + searchString + '\n')
    print (str(search.amountResults) + " result(s): " + str(search.amountNone) + " none(s), " +
           str(search.amountInclude) + " include(s), " + str(search.amountExclude) + " exclude(s).\n")
    print ("TF-IDF (none): " + str(aNone))
    print ("TF-IDF (include): " + str(aInclude))
    print ("TF-IDF (exclude): " + str(aExclude))
    print ("\nTOP TRENDS: " + str(words2))
    print ("WORDS MOST FREQUENTS: " + str(wordsMF))
    print ("WORDS MOST FREQUENTS (STEMMER): " + str(wordsMFs) +'\n')
    print ("\nALL TERMS: ")
    for w in wAux:
        print('\t' + w)
    print('\n\n')
    

def getWordsMF(allWords):
    wT = []
    cWT = []            
    for w in allWords:
        if w not in wT:
            wT.insert(len(wT),w)
            cWT.insert(len(cWT),allWords.count(w))

    #Words Most Frequent
    wordsMF = []
    for i in range(6):
        maxI = max(cWT)                
        wTindex = cWT.index(maxI)                
        wordsMF.append(wT[wTindex])
        del(wT[wTindex])
        del(cWT[wTindex])

    return wordsMF

class generateLogAnalyse(object):

    def POST(self):
        try:
            data = web.input()                        
            searchString = str(data.searchString)
            search = getSearch(int(data.idSearch))
            printForAnalisys(search, searchString, [], [], [], [])
            return ''
        except ZeroDivisionError:
            return '...error...'
        
class getWordsSimilar(object):

    def POST(self):
        try:
            operators = ['AND', 'OR', 'NOT', 'NEAR', 'PUBYEAR', 'TITLE ABS KEY', 'COMP',
                         'LIMIT TO', 'SUBJAREA', 'LANGUAGE', 'ENGLISH' ]

            data = web.input()
            idResearch = int(data.idResearch)
            idSearch = int(data.idSearch)
            searchString = str(data.searchString)
            search = getSearch(idSearch)
            
            rdlsc_ft = getFT(idResearch, idSearch)        
            terms = searchString.split(' ')
            
            tfIDFs = eval(search.tfIdfNone) + eval(search.tfIdfInclude) + eval(search.tfIdfExclude)        
            for t in tfIDFs:
                terms.append(t[0])

            allWords = []
            
            pos = []
            for p in eval(search.tfIdfInclude):
                pos.append(p[0])
            neg = []
            for n in eval(search.tfIdfExclude):
                neg.append(n[0])
            
            termsUnique = arrayUnique(terms)            
            termsUnique = sorted(termsUnique)            

            html = ''

            #Words by positive (include) and negative (exclude) examples
            print('Get Most Similar Cosmul (Tops trends).... ')
            time_begin = datetime.now()
            words2 = rdlsc_ft.getMostSimilarCosmul(pos, neg)
            for w in words2:
                allWords.append(w)
            words2 = arrayUnique(words2)            
            time_end = datetime.now()
            print ("Finished Get Most Similar Cosmul (Tops trends) in %s" % (str(time_end-time_begin)) )

            wAux = []

            print('Get similar words to terms....', end='')
            time_begin = datetime.now()
            for term in termsUnique:            
                if (term.upper() not in operators) and term.replace(" ", "")!='':                    
                    words = rdlsc_ft.getSimilarWords(term)                    

                    for w in words:
                        allWords.append(w)
                        
                    words = arrayUnique(words)
                    html += htmlWords(term, term, arrayWithoutNumber(words))
                    wAux.insert(len(wAux), '{0:<20} {1:<70}'.format(term, str(words)))
                    print('.', end="")
            time_end = datetime.now()
            print ("\nFinished get similar words to terms in %s" % (str(time_end-time_begin)) )            
            
            allWordsSt = []            
            for w in allWords:
                allWordsSt.append(rdlsc_nltk.stemmer(w))

            wordsMF = getWordsMF(allWords)
            wordsMFst = getWordsMF(allWordsSt)

            html += '&nbsp;&nbsp;&nbsp;&nbsp;'
            html += htmlWords(' ','TOP TRENDS (TERMS)', arrayWithoutNumber(words2))
            html += htmlWords(' ', 'WORD MOST FRENQUENT', arrayWithoutNumber(wordsMF))
            html += htmlWords(' ', 'WORD MOST FRENQUENT (STEMMER)', arrayWithoutNumber(wordsMFst))

            printForAnalisys(search, searchString, arrayWithoutNumber(words2),
                             arrayWithoutNumber(wAux), arrayWithoutNumber(wordsMF),
                             arrayWithoutNumber(wordsMFst))
            
            return html
        except ZeroDivisionError:
            return '...'

    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
