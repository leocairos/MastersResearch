#http://ieeexplore.ieee.org/gateway/
#http://ieeexplore.ieee.org/Xplorehelp/#/searching-ieee-xplore/search-tips#stemming
#http://ieeexplore.ieee.org/Xplorehelp/#/searching-ieee-xplore/search-tips#stop-words
"""
SEARCH GUIDELINES
  - Operators need to be in all caps – i.e. AND/OR/NOT/NEAR.
  - Asterisk wildcards cannot be used within quotes or with the NEAR/ONEAR operators.
  - There is a maximum of 15 search terms.
"""

import requests
import xml.etree.ElementTree as ET
from rdlsc_util import cfgIEEE as cfg
from requests_toolbelt.threaded import pool

class Paper:  
    def __init__(self, i, t, a, r, k):
        self.id = i
        self.title = t
        self.abstract = a
        self.rank = r
        self.keywords = k

def getFieldValue(v, f):
    try:
        return v.find(f).text
    except:
        if f == 'totalfound' or f == 'totalsearched':
            return '0'
        else:
            return ''

def getTerms(v, f):
    try:
        terms = ''        
        for term in v.findall(f):
            if terms =='':
                terms = term.text
            else:
                terms = terms + ', ' + term.text
        return terms
    except:
        return ''

def getPaper(doc):
    rank = getFieldValue(doc, "rank")
    pid = getFieldValue(doc, "publicationId")
    title = getFieldValue(doc, "title")
    abst = getFieldValue(doc, "abstract")
        
    terms = getTerms(doc, ".//controlledterms//term")
    if terms !='':
        terms = terms + ', ' + getTerms(doc, ".//thesaurusterms//term")
    else:
        terms = getTerms(doc, ".//thesaurusterms//term")
            
    #print (str(rank) + ': ' + str(terms)) 

    return Paper(pid, title, abst, rank, terms)        

def runSearch(searchString, searchIn):
    rpp = cfg.count
    urlSearchApi =  'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'
    urlSearchApi += searchIn +'=(' + searchString + ')&hc=' + str(rpp) + '&rs='

    r = requests.post(urlSearchApi+'1')
    resp = r.text

    root = ET.fromstring(resp)
    docs = root.findall(".//document")

    totalFounds = getFieldValue(root, "totalfound")
    totalSearched = getFieldValue(root, "totalsearched")
    print ('%s document(s) found(s) in %s document(s) searched(s)' % (totalFounds, totalSearched))
    print ('urlSearchApi: ' + urlSearchApi)
    papers = []
    r = 1
    for doc in docs :
        paper = getPaper(doc)        
        papers.insert(r, paper)
        r += 1
        #print ("%d - %s (%s) \n \t %s \n" % (len(papers), paper.title, paper.rank, paper.abstract))

    # Using requests with Threading
    urls = []
    for num in range(rpp, int(totalFounds), rpp):
        urls.insert(len(urls), urlSearchApi+str(num+1) )
    p = pool.Pool.from_urls(urls)
    p.join_all()

    for rA in p.responses():
        respA = rA.text
        #print (resp)
        rootA = ET.fromstring(respA)
        docsA = rootA.findall(".//document")
        for docA in docsA:
            paper = getPaper(docA)
            papers.insert(r, paper)
            r += 1
            #print ("%d - %s (%s) \n \t %s \n" % (len(papers), paper.title, paper.rank, paper.abstract))

        
    '''
    for num in range(rpp, int(totalFounds), rpp):
        #print ('urlSearchApi: ' + urlSearchApi + str(num+1))
        rA = requests.get(urlSearchApi+str(num+1))
        respA = rA.text
        #print (resp)
        rootA = ET.fromstring(respA)
        docsA = rootA.findall(".//document")
        for docA in docsA:
            paper = getPaper(docA)
            papers.insert(r, paper)
            r += 1
            #print ("%d - %s (%s) \n \t %s \n" % (len(papers), paper.title, paper.rank, paper.abstract))
    '''
 
    return [papers, totalFounds, totalSearched, urlSearchApi]

if __name__ == "__main__":
    import datetime
    time_begin = datetime.datetime.now()
    print ("Started in " + str(time_begin) )

    papers, totalFounds, totalSearched, urlSearchApi = runSearch('java AND web', 'md')
    print (len(papers))
        
    time_end = datetime.datetime.now()
    print ("Finished in " + str(time_end-time_begin) )
