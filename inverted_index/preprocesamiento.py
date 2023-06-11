import nltk
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('spanish')
nltk.download('punkt')

def tokenizar(texto):
    texto = texto.lower()
    tokens = nltk.word_tokenize(texto)
    tokenText = nltk.Text(tokens).tokens
    return tokenText

def eliminarStopWords(tokenText):
    #elegir stopwords
    customSW = open('inverted_index/docs/stopwords.txt','r')
    stoplist = customSW.read().splitlines()
    customSW.close()
    stoplist += [".", "?", "¿", "-", "!", ",", ":",";","«", "con", "»", ")", "(", "'", "```", "iii", "``"]    

    #reducir palabras
    tokensLst = []
    for token in tokenText:
        if token not in stoplist: #filtrar por stopwords
            tokensLst.append(stemmer.stem(token)) #stemming

    return tokensLst

def preprocesar_query(query):
    tokenText = tokenizar(query)
    tokensLst = eliminarStopWords(tokenText)
    return tokensLst

def preprocesar_textos(textos):
    textos_procesados = []
    for file_name in textos:
        file = open("inverted_index/docs/"+file_name)
        texto = file.read().rstrip()
        tokenText = tokenizar(texto)
        tokensLst = eliminarStopWords(tokenText)
        textos_procesados.append(tokensLst)

    return textos_procesados
