# http://www.markhneedham.com/blog/2015/02/15/pythonscikit-learn-calculating-tfidf-on-how-i-met-your-mother-transcripts/
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
from collections import defaultdict 

def getCorpus(docs):
    corpus = []
    doc_id = 0
    for d in docs:
        corpus.insert( doc_id, d.title + ' ' + d.abstract + ' ' + d.keywords)
        doc_id += 1        
    return corpus

def getCorpusUnique(docs):
    txt = ''
    for d in docs:
        txt +=  d.title + ' ' + d.abstract + ' ' + d.keywords
    return [txt]

from sklearn.feature_extraction.text import TfidfVectorizer
def getTFidf(corpus, ngramMax):
    #tf = TfidfVectorizer(analyzer='word', ngram_range=(1,ngramMax), stop_words = 'english')

    tf =TfidfVectorizer(input='content', encoding='utf-8', decode_error='replace',
                        strip_accents='ascii', lowercase=True, preprocessor=None, tokenizer=None,
                        analyzer='word', stop_words='english',
                        ngram_range=(1, ngramMax), max_df=1.0, min_df=1, max_features=None,
                        vocabulary=None, binary=False,
                        norm=None, use_idf=True, smooth_idf=True, sublinear_tf=True)

    tfidf_matrix =  tf.fit_transform(corpus)
    feature_names = tf.get_feature_names()
    dense = tfidf_matrix.todense()
    return [tfidf_matrix, feature_names, dense]


def getScores (pos, dense, feature_names, count):
    paper = dense[pos].tolist()[0] # select the document for phrase_score
    phrase_scores = [pair for pair in zip(range(0, len(paper)), paper) if pair[1] > 0]
     
    sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
    phraseScore = []
    for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:count]:
       #print('{0: <40} {1}'.format(phrase, score))
       phraseScore.append([phrase, score])

    return phraseScore

def getTFIDF(corpus, nGramMax, numFeatures):        
    tf_idf = []
    if len(corpus)>0:
        #Gerar TF-IDF do corpus
        tfIdf_rec = getTFidf(corpus, nGramMax)
        tfidf_matrix = tfIdf_rec[0]
        feature_names = tfIdf_rec[1]
        dense = tfIdf_rec[2]

        #get score
        doc_id = 0        
        for doc in tfidf_matrix.todense():
            #print ("-------------------------------------------------------------\nDoc " + str(doc_id+1))
            phrasesScores = getScores (doc_id, dense, feature_names, numFeatures)
            #for phraseScore in phrasesScores:
                #print('{0: <40} {1}'.format(phraseScore[0], phraseScore[1])) 
            tf_idf.insert( doc_id, phrasesScores)
            doc_id += 1
            
        return tf_idf
    else:
        return tf_idf

#getTFIDF ('systematic AND review AND software', 100, 'md', False, 3, 15)
