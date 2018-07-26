#-----------------------------------------------------------
# Configutations of my application
#-----------------------------------------------------------

# https://dev.elsevier.com/api_key_settings.html
class cfgScopus:
    count = 25 # maximum number of results to be returned for the search. Default 25 results Max 200
    apiKey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    insttoken = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    
class cfgIEEE:
    count = 1000 # maximum number of results to be returned for the search MAX=1000
    apiKey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'    
    
class cfgApp:
    fileDB = 'slr_tes.db' 
    nGrams = 1 # default amount nGrams to TF-IDF
    features = 5 # default amount features for TF-IDF
    orderDoc = 'rankDoc' #order documents in view (rankDoc, title, classification)

#-----------------------------------------------------------
# Some functions utils of my application
#-----------------------------------------------------------   
# Normalize text
def normalize_text(texts):    

    # Lower case
    texts = texts.lower()
    
    # Replace specialChar
    #specialChar = '–ç!"#$%&\'()*+,./:;<=>?@©®-[\\]^_`{|}~“”'
    specialChar = '!"#$%&\'()*+,./:;<=>?@©®-[\\]^`{|}~“”’|'
    for c in list(specialChar):
        #texts = [' '.join(x.split(c)) for x in texts]
        texts = texts.replace(c, ' ')
    texts = texts.replace('  ', ' ')

    return texts.strip()

if __name__ == "__main__":
    texto = 'my  Name 1 is ;**  leo-nardo4d sam0pAio. sam9pAio  cairo industry–a sy human-–computer '
    print(texto)    
    print(normalize_text(texto))
