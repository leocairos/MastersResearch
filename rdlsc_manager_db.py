#http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte1.html
#http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte2.html

import sqlite3
from rdlsc_util import cfgApp as cfg
from datetime import datetime 

class ResearchSLR:
    def __init__(self, i, name, dateTime, r):        
        self.id = i
        self.name = name
        self.dateTime = dateTime
        self.searchs = []
        self.repository = r

    def putSearch(self, search):
        self.searchs.append(search)

    def setSearchs(self, searchs):
        self.searchs = searchs
        
class SearchSLR:
    def __init__(self, i, research, dateTime, searchString,
                 searchIn, urlSearchAPI, nGrams, amountFeatures,
                 amountResults, amountPerPage, amountNone, amountInclude,
                 amountExclude, tfIdfNone, tfIdfInclude, tfIdfExclude):
        self.id = i
        self.research = research
        self.dateTime = dateTime
        self.searchString = searchString
        self.searchIn = searchIn
        self.urlSearchAPI = urlSearchAPI
        self.nGrams = nGrams
        self.amountFeatures = amountFeatures
        self.amountPerPage = amountPerPage
        self.amountResults = amountResults
        self.amountNone = amountNone
        self.amountInclude = amountInclude
        self.amountExclude = amountExclude
        self.tfIdfNone = tfIdfNone
        self.tfIdfInclude = tfIdfInclude
        self.tfIdfExclude = tfIdfExclude

class DocumentInSearchSLR:
    def __init__(self, i, search, idDocument, title, abstract,
                 rankDoc, classification, tfIDF, keywords):
        self.id = i
        self.search = search
        self.idDocument = idDocument
        self.title = title
        self.abstract = abstract
        self.rankDoc = rankDoc
        self.classification = classification #none/include/exclude
        self.tfIDF = tfIDF #[ [word1,score1],[wordn,scoren] ]
        self.keywords = keywords
        
class Connect(object):

    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            #print("Database:", db_name)
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            #print("SQLite version: %s" % self.data)
        except sqlite3.Error:
            print("Error trying to connect to database.")
            return False

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
            #print("Connection closed.")

class slrDB(object):

    def __init__(self, dbName):
        self.db = Connect(dbName)        

    def closeCon(self):
        self.db.close_db()

    def createTables(self, schema_name='slrDB_schema.sql'):
        #print("Creating tables...")
        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)
                #print(schema)
        except :
            print("Error when creating tables")
            return False
        #print("Tables created successfully")

    def insertResearch(self, research):
        try:
            self.db.cursor.execute("""
            INSERT INTO researchSLR (name, date_time, repository)
            VALUES (?,?, ?)
            """, (research.name, research.dateTime, research.repository))
            self.db.commit_db()
            #print("Research inserted successfully.")
            return True
        except:
            print("Error when inserting research")
            return False

    def insertSearch(self, search):
        try:
            self.db.cursor.execute("""
            INSERT INTO searchSLR (idResearch, date_time, searchString, searchIn, urlSearchApi,
            nGrams, amountFeatures, amountResults, amountPerPage, amountNone, amountInclude,
            amountExclude, tfIdfNone, tfIdfInclude, tfIdfExclude)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (search.research, search.dateTime, search.searchString, search.searchIn,
                  search.urlSearchAPI, search.nGrams, search.amountFeatures, search.amountPerPage,
                  search.amountResults, search.amountNone, search.amountInclude,
                  search.amountExclude, search.tfIdfNone, search.tfIdfInclude,
                  search.tfIdfExclude))
            self.db.commit_db()
            #print("Search inserted successfully.")
            return True
        except NameError:
            print("Error when inserting search")
            return False

    def insertDocumentInSearch(self, doc, idResearch):
        try:
            classific = doc.classification
            #search = self.findSearch(doc.search)
            d = self.lastClassificDocByResearch(doc.idDocument, idResearch)
            #print(d)
            if d: # if exists, then get classification
                classific = d[6] 
            
            self.db.cursor.execute("""
            INSERT INTO documentInSearchSLR (idSearch, idDocument, title,
            abstract, rankDoc, classification, tfIDF, keywords)
            VALUES (?,?,?,?,?,?,?,?)
            """, (doc.search, doc.idDocument, doc.title, doc.abstract,
                  doc.rankDoc, classific, str(doc.tfIDF), doc.keywords))
            self.db.commit_db()
            #self.updAmountInSearch(doc.search)
            #print("Document inserted successfully.")
            return True
        except NameError:
            print("Error when inserting documentInSearch" )
            return False

    def updateDocumentInSearch(self, doc):
        try:
            d = self.findDocument(doc.id)
            if d: 
                self.db.cursor.execute("""
                UPDATE documentInSearchSLR SET classification = ?, tfIDF = ? WHERE id = ?""",
                                       (doc.classification, doc.tfIDF, doc.id))
                self.db.commit_db()
                self.updAmountInSearch(doc.search)
                #print("Document was updating sucess" )
                return True
            else:
                print("Document was no updating" )
                return False
        except:
            print("Error when updating document" )
            return False

    def updAmountInSearch(self, idSearch):
        sql = "SELECT count(*) FROM documentInSearchSLR WHERE idSearch = ? AND classification="

        cN = self.db.cursor.execute(sql+"'N'", (idSearch,)).fetchone()
        cI = self.db.cursor.execute(sql+"'I'", (idSearch,)).fetchone()
        cE = self.db.cursor.execute(sql+"'E'", (idSearch,)).fetchone()    

        #sql2 = "SELECT count(*) FROM documentInSearchSLR WHERE idSearch = ?"

        #cAr = self.db.cursor.execute(sql2, (idSearch,)).fetchone()
        
        '''self.db.cursor.execute("""
                UPDATE searchSLR SET amountNone = ?, amountInclude = ?, amountExclude = ?, amountResults = ?
                WHERE id = ?""", (int(cN[0]), int(cI[0]), int(cE[0]), int(cAr[0]), idSearch))'''

        self.db.cursor.execute("""
                UPDATE searchSLR SET amountNone = ?, amountInclude = ?, amountExclude = ? 
                WHERE id = ?""", (int(cN[0]), int(cI[0]), int(cE[0]), idSearch))
        self.db.commit_db()

        #print (cN)
        #print (cI)
        #print (cE)

    def updTfIdfInSearch(self, idSearch, tfIDF):        
        self.db.cursor.execute("""
                UPDATE searchSLR SET tfIdfNone = ?, tfIdfInclude = ?, tfIdfExclude = ? WHERE id = ?""",
                               (str(tfIDF[0]), str(tfIDF[1]), str(tfIDF[2]), idSearch))
        self.db.commit_db()

        
    def getAllResearch(self):
        sql = 'SELECT * FROM researchSLR ORDER BY id'
        r = self.db.cursor.execute(sql)
        researchs = []
        for res in r.fetchall():
            researchSLR = ResearchSLR(res[0], res[1], datetime.strptime(res[2], '%Y-%m-%d %H:%M:%S.%f'), res[3] )
            researchSLR.setSearchs(self.getSearchByResearch(res[0]))
            researchs.append(researchSLR)
        return researchs

    def getSearchByResearch(self, idResearch):
        sql = 'SELECT * FROM searchSLR WHERE idResearch = ? ORDER BY id'
        r = self.db.cursor.execute(sql, (idResearch,))
        searchs = []
        for res in r.fetchall():
            searchSLR = SearchSLR(res[0], res[1],
                                             datetime.strptime(res[2], '%Y-%m-%d %H:%M:%S.%f'),
                                             res[3], res[4], res[5], res[6], res[7], res[8], res[9],
                                             res[10], res[11], res[12], res[13], res[14], res[15])
            searchs.append(searchSLR)
        return searchs

    def getDocumentsBySearch(self, idSearch):
        sql = 'SELECT * FROM documentInSearchSLR WHERE idSearch = ? ORDER BY ' + cfg.orderDoc
        r = self.db.cursor.execute(sql, (idSearch,))
        docs = []
        for res in r.fetchall():
            documentInSearchSLR = DocumentInSearchSLR(res[0], res[1], res[2],
                                             res[3], res[4], res[5], res[6], eval(res[7]), res[8])
            docs.append(documentInSearchSLR)
        return docs
    
    def findResearch(self, i):
        r = self.db.cursor.execute('SELECT * FROM researchSLR WHERE id = ?', (i,))
        return r.fetchone()

    def findSearch(self, i):
        r = self.db.cursor.execute('SELECT * FROM searchSLR WHERE id = ?', (i,))
        res = r.fetchone()
        if res:
            searchSLR = SearchSLR(res[0], res[1],
                                             datetime.strptime(res[2], '%Y-%m-%d %H:%M:%S.%f'),
                                             res[3], res[4], res[5], res[6], res[7], res[8],
                                             res[9], res[10], res[11], res[12], res[13], res[14],
                                             res[15])
        
            return searchSLR
        else:
            return ''

    def findSearchStringInSearch(self, idResearch, searchString):
        r = self.db.cursor.execute('SELECT * FROM searchSLR WHERE idResearch = ? AND searchString = ?', (idResearch, searchString,))
        return r.fetchone()
    
    def findDocumentInSearch(self, doc, search):
        r = self.db.cursor.execute('''SELECT * FROM documentInSearchSLR doc
                                    WHERE idDocument = ? AND idSearch = ? ''', (doc, search, ))
        #print (r.fetchone())
        return r.fetchone()

    def findDocument(self, doc):
        r = self.db.cursor.execute('''SELECT * FROM documentInSearchSLR doc
                                    WHERE id = ? ''', (doc, ))        
        return r.fetchone()
    
    def lastSearchByResearch(self, i):
        r = self.db.cursor.execute('SELECT  * FROM searchSLR WHERE idResearch = ? ORDER BY ID DESC LIMIT 1', (i,))        
        return r.fetchone()

    def lastClassificDocByResearch(self, idDoc, idResearch):
        r = self.db.cursor.execute('''SELECT  * FROM documentInSearchSLR
                                    WHERE idDocument = ? and idSearch in (
                                        SELECT id from searchSLR where idResearch = ?) 
                                    ORDER BY ID DESC LIMIT 1''', (idDoc, idResearch,))        
        return r.fetchone()
    
    def getResearch(self, i):
        try:
            c = self.findResearch(i)            
            if c:
                return ResearchSLR(c[0],c[1], c[2], c[3])
            else:
                return None
        except e:
            raise e

    def deleteResearch(self, i):
        try:
            c = self.findResearch(i)            
            if c:
                self.db.cursor.execute('DELETE FROM researchSLR WHERE id = ?', (i,))                
                self.db.commit_db()
                for s in self.getAllSearchsByResearch(i):
                    self.deleteSearch(s[0])
                
                #print("Research '%d' deleted successfully." % i)
                return True
            else:
                print("There is no research with the code '%d'." % i)
                return False
        except e:
            print (e)
            return False
            raise e

    def getAllSearchsByResearch(self, i):
        sql = 'SELECT id FROM searchSLR WHERE idResearch = ?'
        r = self.db.cursor.execute(sql, (i,))
        return r.fetchall()
        
    def deleteSearch(self, i):
        try:
            c = self.findSearch(i)            
            if c:                
                self.db.cursor.execute('DELETE FROM searchSLR WHERE id = ?', (i,))                
                self.db.commit_db()
                self.db.cursor.execute('DELETE FROM documentInSearchSLR WHERE idSearch = ?', (i,))                
                self.db.commit_db()
                #print("Search '%d' deleted successfully." % i)
                return True
            else:
                print("There is no search with the code '%d'." % i)
                return False
        except e:
            print (e)
            return False
            raise e

    def deleteDocInSearch(self, idDoc):
        try:                                      
            self.db.cursor.execute('DELETE FROM documentInSearchSLR WHERE id = ? ', (idDoc,))
            self.db.commit_db()
            #print("Search '%d' deleted successfully." % i)
            print('deleteDocInSearch')
            return True            
        except e:
            print (e)
            return False
            raise e

if __name__ == '__main__':
    slr = slrDB('slr_tes.db')
    slr.createTables()
    #researchSLR = ResearchSLR(0,'Research Include Now', datetime.now())
    #slr.insertResearch(researchSLR)
    lista = slr.getAllResearch()
    for c in lista:
        print(str(c.id) + " " + c.name + " " + str(c.dateTime))
    '''slr.deleteResearch(2)
    lista = slr.getAllResearch()
    for c in lista:
        print(c)'''
    print()
    #print (slr.getResearch(1).name)
    #searchSLR = SearchSLR(0,1, datetime.now(), 'Java', 2, 5, 2345, 5, 7)
    #slr.insertSearch(searchSLR)
    #print( slr.findResearch(1))
    listaS = slr.getSearchByResearch(1)
    #for c in listaS:
    #    print(c.searchString)
    #print (slr.lastSearchByResearch(1)[0])
    
    slr.updAmountInSearch(45)
    slr.closeCon()
    
