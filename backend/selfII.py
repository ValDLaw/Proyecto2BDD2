import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import OrderedDict, defaultdict
import math
import pandas as pd
import numpy as np
import os
import sys

# Obtén la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtén la ruta absoluta del directorio 'inverted_index'
inverted_index_dir = os.path.join(current_dir, '..', 'inverted_index')

# Agrega la ruta del directorio 'inverted_index' al sys.path
sys.path.append(inverted_index_dir)

# Ahora puedes realizar la importación relativa
from preprocesamiento import preprocesar_textos
from tfidf import calculate_tf


app = Flask(__name__)
CORS(app, origin="*", supports_credentials=True)

def loadData(data_path):
        data = pd.read_csv(data_path, header=None)
        data.columns = ["id","submitter","authors","title","categories","abstract","update_date","authors_parsed"]
        data["id"] = data["id"].astype(str)
        return data

def load_Index(path_index):
        result = []
        with open(path_index, 'r') as file:
            document = file.read()

            lines = document.split('\n')
            for line in lines:
                if line:
                    key, posting_list = line.split(':', 1)
                    result.append((key, posting_list)) #linea de strings, key con posting_list en string
        return result   

data = loadData('/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/dataset/arxiv-metadata.csv')
index_data = load_Index('/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/inverted_index/spimi.txt')

def cos_Similarity(query, cosine_docs):
    cosine_scores = defaultdict(float)
    for docId in cosine_docs:
        doc = cosine_docs[docId]
        q = query
        sum_ = 0
        sum_ += round(np.dot(q/(np.linalg.norm(q)),doc/(np.linalg.norm(doc))),5)
        cosine_scores[docId] = sum_
    return cosine_scores

#IMPLEMENTAR BINARY!
#Index Data es cada linea del documento como un set Term, postinglist
#siendo postinglist toda una string de docId, tf_idf; docId2, tf_idf;
def binary_search(term, index_data):
    left = 0
    right = len(index_data) - 1
    while left <= right:
        mid = (left + right) // 2
        current_term = index_data[mid][0]
        if current_term == term:
            return index_data[mid][1].split(";")[:-1]
        elif term < current_term:
            right = mid - 1
        else:
            left = mid + 1

    return None

#Sequential Search on Index
def loop(term, index_data):
    for data in index_data:
        term_index = data[0]
        docId_scores = data[1]
        if term_index == term:
            return docId_scores.split(";")[:-1]
    return None

def retrieve_k_nearest(query, k):
    #data = loadData('')
    query = preprocesar_textos(query)

    cos_to_evaluar = defaultdict(dict)
    idf_query=defaultdict(float)
    query_tfidf = []

    for term in query:
        term_data = binary_search(term, index_data)
        #term_data = loop(term, index_data) #posting list
        if term_data is None:
            continue
        
        idf_query[term] = round(math.log10((len(data)/len(term_data)) + 1),4)

        for docId_tfidfin in term_data:
            docId = docId_tfidfin.split(",")[0]
            tf_idf = docId_tfidfin.split(",")[1]
            cos_to_evaluar[docId][term] = tf_idf
            #va guardando en cada doc, el tf idf en orden de los querys keywords
        
        tf_ = calculate_tf(term, query)
        idf_ = idf_query[term]
        query_tfidf.append(tf_*idf_)
    
    #Crear vectores caracteristicos
    cosine_docs = defaultdict(list)

    for docId in cos_to_evaluar:
        for term in query:
            if term in cos_to_evaluar[docId]:
                cosine_docs[docId].append(float(cos_to_evaluar[docId][term]))
            else:
                cosine_docs[docId].append(0)

    scores = cos_Similarity(query_tfidf, cosine_docs)

    # Ordenar los documentos por puntuación de similitud de coseno en orden descendente
    scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    scores = scores[:k]
    
    temp = []
    for result in scores:
        temp.append(result[0])


    # INDICES para hallar en el dataframe
    matching_indices = data.loc[data["id"].isin(temp)].index

    return matching_indices

@app.route('/consulta', methods=['POST'])
def consulta():
    data_json = request.get_json()
    parametro = data_json['parametro']
    k = data_json['k']

    # Ejecutar la consulta en PostgreSQL y medir el tiempo de ejecución
    start_time = time.time()
    results = retrieve_k_nearest(parametro,k)
    resultados = data.iloc[results]
    end_time = time.time()

    tiempo_ejecucion = end_time - start_time

    print(resultados)
    # Convertir el DataFrame en una lista de diccionarios
    resultados_dict = resultados.to_dict(orient='records')

    response = {
        'resultados': resultados_dict,
        'tiempo_ejecucion': tiempo_ejecucion
    }

    return jsonify(response)


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'statusCode': 404,
        'message': 'Resource not found'
    }), 404

@app.route("/")
def indice():
    print("Ruta raíz accedida")
    return "Api para Retrieve propio"

if __name__ == '__main__':
    app.run(port=5023)