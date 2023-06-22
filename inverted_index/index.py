from inverted_index.preprocesamiento import preprocesar_textos
from inverted_index.tfidf import compute_tfidf, tf_idf
import pandas as pd

import sys
import ast
import re
import json

import os
from operator import itemgetter
from collections import OrderedDict, defaultdict


class InvertIndex:
    def __init__(self, index_file, abstracts_por_bloque=10000, dataFile=""):
        self.index_file = index_file
        self.index = {}
        self.idf = {}
        self.length = {}
        self.BLOCK_LIMIT = abstracts_por_bloque
        self.lista_de_bloques = []
        self.data_path = "/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/inverted_index/docs/"+dataFile #data.csv
        self.path_index = "/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/inverted_index/spimi.txt"


    def SPIMIConstruction(self):
        data = pd.read_csv(self.data_path, header=None)
        data.columns = ["id","submitter","authors","title","categories","abstract","update_date","authors_parsed"]

        documents_count = len(data)
        dictTerms = defaultdict(list)
        block_n = 1

        for idx, row in data.iterrows():
            if idx % 20000 == 0: print("Estamos en el index ", idx)
            abstract = row["abstract"]
            docID = row["id"]
            tokensAbstract = preprocesar_textos(abstract)
            #Crear postingList
            term_freq = defaultdict(int)
            for term in tokensAbstract:
                term_freq[term] += 1
            
            for term, freq in term_freq.items():
                if sys.getsizeof(dictTerms) > self.BLOCK_LIMIT:
                    sorted_block = sorted(dictTerms.items(), key=itemgetter(0))
                    block_name = "bloque-"+str(block_n)+".txt"
                    with open("/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/inverted_index/docs/blocks/"+block_name, "w") as file_part:
                        json.dump(sorted_block, file_part, indent=2)
                    sorted_block = {} #clear
                    block_n += 1
                    dictTerms = defaultdict(list) #clear
                dictTerms[term].append((docID, freq))
        
        if dictTerms:
            sorted_block = sorted(dictTerms.items(), key=itemgetter(0))
            block_name = "bloque-"+str(block_n)+".txt"
            with open("/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/inverted_index/docs/blocks/"+block_name, "w") as file_part:
                json.dump(sorted_block, file_part, indent=2)
            dictTerms = defaultdict(list)

    def listFiles(self):
        filepaths = "/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/inverted_index/docs/blocks/"
        files = []
        for file_name in os.listdir(filepaths):
            file_path = os.path.join(filepaths, file_name)
            if os.path.isfile(file_path):
                files.append(file_path)
        return files #list of pathnames
    
    def merge(self, block1, block2):
        merge_final = OrderedDict()

        for term, ids in block1.items():
            if term in merge_final:
                merge_final[term]+= ids
            else:
                merge_final[term] = ids
        
        for term, ids in block2.items():
            if term in merge_final:
                merge_final[term]+= ids
            else:
                merge_final[term] = ids
        bloque_ordenado = OrderedDict(sorted(merge_final.items(), key=lambda x: x[0]))

        return bloque_ordenado
        
    def write_index_tf_idf(self, inverted_dict, filename, n_documents):
        with open(filename, "w") as index:
            for term, ids in inverted_dict.items():
                docFrec = len(ids) #en cuantos docs aparece?
                index.write(f"{term}:")
                for doc_tf_id in ids:
                    doc_id = doc_tf_id[0]
                    tf = doc_tf_id[1]
                    termdoc_tfidf = tf_idf(tf, docFrec, n_documents)

                    index.write(f"{doc_id},{termdoc_tfidf};")
                index.write("\n")

    def write_index(self, inverted_dict, filename):
        with open(filename, "w") as index:
            for term, ids in inverted_dict.items():
                index.write(f"{term}:{ids};")
                index.write("\n")

    #Se encarga de hacer el merge de blocks, e indexar
    def index_blocks(self):
        blocks = []
        files = self.listFiles()
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as file:
                block = json.load(file)
                blocks.append(block)


        while 1 < len(blocks):
            merged_blocks = []
            for i in range(0,len(blocks), 2):
                if i+1 <len(blocks): #si ya no hay mas con que agarrar, o sea el ultimo
                    combinados = self.merge(dict(blocks[i]), dict(blocks[i+1]))
                    merged_blocks.append(combinados)
                else:#solo append al final
                    merged_blocks.append(blocks[i])
            blocks = merged_blocks #actualiza el nuevo merge
        ordenar_merge = OrderedDict(sorted(blocks[0].items(), key=lambda x: x[0]))

        return ordenar_merge

    def prueba(self):
        #Merge completo
        self.SPIMIConstruction()
        merge_final = self.index_blocks()
        self.write_index_tf_idf(merge_final, self.path_index, len(merge_final))

    def getTokens(self, textos):
        collection = preprocesar_textos(textos)
        return collection