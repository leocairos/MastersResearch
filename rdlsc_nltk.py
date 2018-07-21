# http://minerandodados.com.br/index.php/2017/06/22/mineracao-de-textos-7-tecnicas/#NLTK-Wins
import nltk
from nltk.corpus import wordnet

#Stemming - consiste na redução da palavra até o seu radical.
#Remover afixos e vogais temáticas das palavras.
def stemmer(word):
    stemmer = nltk.stem.RSLPStemmer()
    return stemmer.stem(word)

