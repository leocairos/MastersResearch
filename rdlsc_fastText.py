# https://pypi.python.org/pypi/fasttext
# https://radimrehurek.com/gensim/models/wrappers/fasttext.html
# https://codexample.org/questions/762780/how-to-find-similar-words-with-fasttext.c

#   
# https://radimrehurek.com/gensim/models/word2vec.html

import fasttext
from gensim.models import KeyedVectors as modelGensim
import datetime
import os
import sys

class rdlsc_FastText:
    
    def __init__(self, idResearch, idSearch):        
        
        #input_file     training file path (required)
        #output         output file path (required)
        #lr             learning rate [0.05]
        #lr_update_rate change the rate of updates for the learning rate [100]
        #dim            size of word vectors [100]
        #ws             size of the context window [5]
        #epoch          number of epochs [5]
        #min_count      minimal number of word occurences [5]
        #neg            number of negatives sampled [5]
        #word_ngrams    max length of word ngram [1]
        #loss           loss function {ns, hs, softmax} [ns]
        #bucket         number of buckets [2000000]
        #minn           min length of char ngram [3]
        #maxn           max length of char ngram [6]
        #thread         number of threads [12]
        #t              sampling threshold [0.0001]
        #silent         disable the log output from the C++ extension [1]
        #encoding       specify input_file encoding [utf-8]
        
        self.fileData = "./tmp/data_" + str(idResearch)+ "_" + str(idSearch) + ".txt"
        self.fileModelS = "./tmp/modelSkip_" + str(idResearch)+ "_" + str(idSearch) 
        self.fileModelC = "./tmp/modelCbow_" + str(idResearch)+ "_" + str(idSearch) 
        
    def makeModel(self, method):
        print('Creating ' + method +' model...')
        time_begin = datetime.datetime.now()
        if method == 'skip' and not os.path.isfile(self.fileModelS+'.vec'):            
            model = fasttext.skipgram(self.fileData, self.fileModelS, lr=0.2, lr_update_rate=100, dim=600, ws=7,
                                      epoch=5, min_count=3, neg=5, word_ngrams=3,
                                      bucket=2000000, minn=3, maxn=6, thread=12, t=0.0001)
            self.modelSkip = model
        else:
            if method == 'cbow' and not os.path.isfile(self.fileModelC+'.vec'):              
                model = fasttext.cbow(self.fileData, self.fileModelC, lr=0.2, lr_update_rate=100, dim=600, ws=7,
                                      epoch=5, min_count=3, neg=5, word_ngrams=3,
                                      bucket=2000000, minn=3, maxn=6, thread=12, t=0.0001)
                self.modelCbow = model
        time_end = datetime.datetime.now()
         
        ## delete BIN file (not util for this project)
        if os.path.exists(self.fileModelC+'.bin'):
            os.remove(self.fileModelC+'.bin')
        if os.path.exists(self.fileModelS+'.bin'):
            os.remove(self.fileModelS+'.bin')
        
        print ("Finished Training %s in %s" % ( method, str(time_end-time_begin)) )

    def getMGensim(self,method):
        #time_begin = datetime.datetime.now()
        if method == 'skip':
            mGensim = modelGensim.load_word2vec_format(self.fileModelS + '.vec')
        else:
            if method == 'cbow':
                mGensim = modelGensim.load_word2vec_format(self.fileModelC + '.vec')
        #time_end = datetime.datetime.now()
        #print ("Finished load word2vec %s in %s" % ( method, str(time_end-time_begin)) )
        return mGensim

    def getSimilarWords(self, word):
        wRet = []
        try:            
            #time_begin = datetime.datetime.now()
            n = 3
            if not os.path.isfile(self.fileModelS+'.vec'):
                self.makeModel('skip')
            if not os.path.isfile(self.fileModelC+'.vec'):
                self.makeModel('cbow')
            mSkip = self.getMGensim('skip')
            mCbow = self.getMGensim('cbow')
            ws = mSkip.wv.most_similar(word, topn = n)
            wc = mCbow.wv.most_similar(word, topn = n)
            
            for i in ws:
                if i[0].strip() not in wRet:                    
                    wRet.insert(len(wRet),i[0].strip())
            
            for i in wc:
                if i[0].strip() not in wRet:
                    wRet.insert(len(wRet),i[0].strip())

            #print ('{0:<20} {1:<70}'.format(word, str(wRet)))
            #time_end = datetime.datetime.now()
            #print ("Finished Get Similar Words (%s).... in %s" % (word, str(time_end-time_begin)) )
            return wRet
        except:# ZeroDivisionError:
            return wRet

    def wordInVocabulary(self, model, vec):
        aPN = []
        for w in vec:
            try:
                model[w]
                #print(model[w])
                aPN.append(w)
            except:
                next
        return aPN
    
    def getMostSimilarCosmul(self, pos, neg):
        wRet = []
        try:
            #print('Get Most Similar Cosmul.... ')
            #time_begin = datetime.datetime.now()
            aI = set.intersection(set(pos), set(neg))
            for iI in aI:
                pos.remove(iI)
                neg.remove(iI)

            #print('__pos: ' + str(pos) + ' __neg: ' + str(neg))
            #neg=[]
            n = 3
            if not os.path.isfile(self.fileModelS+'.vec'):
                self.makeModel('skip')
            if not os.path.isfile(self.fileModelC+'.vec'):
                self.makeModel('cbow')
            mSkip = self.getMGensim('skip')
            mCbow = self.getMGensim('cbow')


            posS1 = self.wordInVocabulary(mSkip, pos)
            negS1 = self.wordInVocabulary(mSkip, neg)
            posC1 = self.wordInVocabulary(mCbow, pos)
            negC1 = self.wordInVocabulary(mCbow, neg)
            #print(str(posS1) + ' ' + str(negS1))
            #print(str(posC1) + ' ' + str(negC1))
            
            ws= mSkip.wv.most_similar_cosmul(positive=posS1, negative=negS1, topn = n)
            wc= mCbow.wv.most_similar_cosmul(positive=posC1, negative=negC1, topn = n)
                        
            for i in ws:
                if i[0].strip() not in wRet:                    
                    wRet.insert(len(wRet),i[0].strip())
            
            for i in wc:
                if i[0].strip() not in wRet:
                    wRet.insert(len(wRet),i[0].strip())

            #print ('{0:<20} {1:<70} {2:<60}'.format('', str(wRet), str(wRet)))
            #time_end = datetime.datetime.now()
            #print ("Finished Get Most Similar Cosmul.... in %s" % (str(time_end-time_begin)) )
            return wRet
        except:# ZeroDivisionError:
            print ("...:Unexpected error: %s" % (sys.exc_info()[1]))
            return wRet
        
        
if __name__ == "__main__":    
    time_begin = datetime.datetime.now()
    rdlsc_ft = rdlsc_FastText(1,1)

    tGeneral = ['analytics', 'approach', 'based', 'data', 'information', 'language', 'learning', 'literature',
                'machine', 'mapping', 'method', 'mining', 'natural', 'nlp', 'processing', 'research', 'retrieval',
                'review', 'reviews', 'selection', 'slr', 'software', 'studies', 'study', 'systematic', 'text']

    tIncludes = ['systematic', 'review', 'studies', 'text', 'literature', 'reviews', 'selection', 'approach', 'slr', 'method']
    tExcludes = ['systematic', 'review', 'data', 'information', 'learning', 'based', 'research', 'studies', 'literature', 'recognition']

    #print(rdlsc_ft.getSimilarWords('systematic'))
    #for g in tGeneral:        
    #    rdlsc_ft.getSimilarWords(g)

    rdlsc_ft.getMostSimilarCosmul(tIncludes, tExcludes)
    
    time_end = datetime.datetime.now()
    
    #print ("Finished in " + str(time_end-time_begin) )

    '''
most_similar_cosmul(positive=None, negative=None, topn=10)
Find the top-N most similar words, using the multiplicative combination objective proposed by Omer Levy and Yoav Goldberg. Positive words still contribute positively towards the similarity, negative words negatively, but with less susceptibility to one large distance dominating the calculation.

In the common analogy-solving case, of two positive and one negative examples, this method is equivalent to the “3CosMul” objective (equation (4)) of Levy and Goldberg.

Additional positive or negative examples contribute to the numerator or denominator, respectively – a potentially sensible but untested extension of the method. (With a single positive example, rankings will be the same as in the default most_similar.)

Example:

>>> trained_model.most_similar_cosmul(positive=['baghdad', 'england'], negative=['london'])
[(u'iraq', 0.8488819003105164), ...]

====================================================================================

most_similar(positive=None, negative=None, topn=10, restrict_vocab=None, indexer=None)
Find the top-N most similar words. Positive words contribute positively towards the similarity, negative words negatively.

This method computes cosine similarity between a simple mean of the projection weight vectors of the given words and the vectors for each word in the model. The method corresponds to the word-analogy and distance scripts in the original word2vec implementation.

Parameters:	
positive – List of words that contribute positively.
negative – List of words that contribute negatively.
topn (int) – Number of top-N similar words to return.
restrict_vocab (int) – Optional integer which limits the range of vectors which are searched for most-similar values. For example, restrict_vocab=10000 would only check the first 10000 word vectors in the vocabulary order. (This may be meaningful if you’ve sorted the vocabulary by descending frequency.)
Returns:	
Returns a list of tuples (word, similarity)

Return type:	
obj: list of :obj: tuple

Examples

>>> trained_model.most_similar(positive=['woman', 'king'], negative=['man'])
[('queen', 0.50882536), ...]
'''

