import requests
import json
from rdlsc_util import cfgScopus as cfg
from requests_toolbelt.threaded import pool
import datetime
import time

class DocScopus:  
    def __init__(self, i, t, a, r, k ):
        self.id = i
        self.title = t
        self.abstract = a
        self.rank = r
        self.keywords = k
        
def getValue(doc, field):
    try:
        return doc[field]
    except:
        return ''

def docToString(doc):
    return (str(doc.rank) + '\t' + str(doc.id) + ' ' + str(doc.title) + '\n' + doc.abstract
            +'\n' + doc.keywords)

def getDoc(doc, r):
       source_id =  getValue(doc,'dc:identifier')[10:]
    title = getValue(doc,'dc:title')
    abstract = getValue(doc,'dc:description')
    keywords = getValue(doc,'authkeywords')
    return DocScopus(source_id, title, abstract, r, keywords)

def runSearch(searchString):
    count = cfg.count 
    apiKey = cfg.apiKey
    insttoken = cfg.insttoken
                  
    urlSearchApi =  'https://api.elsevier.com/content/search/scopus?query='
    urlSearchApi += '&suppressNavLinks=true&httpAccept=application/json'
    if count:
        urlSearchApi += '&count=' + str(count)
    urlSearchApi += '&insttoken=' + insttoken #+ '&subj=COMP'

    if searchString.find('AND  ( LIMIT-TO ( SUBJAREA ,  "COMP" ) )')>=0:
        urlSearchApi += '&subj=COMP'

    #urlSearchApi += '&date=1950-2015'
    urlSearchApi += '&field=dc:identifier,dc:title,dc:description,authkeywords'
    urlSearchApi += '&start='

    #print ('urlSearchApi: ' + urlSearchApi + '0')
    r = requests.get(urlSearchApi+'0')
    resp = r.text
    #print (resp)
    data= json.loads(resp)
    totalResults = int(data['search-results']['opensearch:totalResults'])
    itemsPerPage = int(data['search-results']['opensearch:itemsPerPage'])
    
    print ('totalResults: ' + str(totalResults) + ' itemsPerPage: '+ str(itemsPerPage) +'\n')
    docs = []
    r = 1
    
    for doc in data['search-results']['entry']:
        document = getDoc(doc, r)
        docs.insert(r, document)
        r += 1

    
    # Using requests with Threading
    urls = []
    for num in range(itemsPerPage, int(totalResults), itemsPerPage):
        urls.insert(len(urls), urlSearchApi+str(num) )
    p = pool.Pool.from_urls(urls)
    p.join_all()

    numPages = 1    
    for rA in p.responses():                
        respA = rA.text        
        #print (resp)
        if numPages<5: # limitando paginas/requisições por busca
            numPages += 1
            #print(numPages)
            dataA= json.loads(respA)        
            for docA in dataA['search-results']['entry']:
                documentA = getDoc(docA, r)
                docs.insert(r, documentA)
                r += 1
            #print('Ok in ' + str(numPages))
        
     return [docs, totalResults, itemsPerPage, 'Link hidden for protection of "apiKey" and "insttoken"']

if __name__ == "__main__":
    
    import datetime
    time_begin = datetime.datetime.now()
    print ("Started in " + str(time_begin) )
    
    docs, totalResults, itemsPerPage, url  = runSearch('java AND web')
    print (len(docs))
        
    time_end = datetime.datetime.now()
    print ("Finished in " + str(time_end-time_begin) )
