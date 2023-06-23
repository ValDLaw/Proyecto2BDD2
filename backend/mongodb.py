import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, origin="*", supports_credentials=True)
client = MongoClient("mongodb://localhost:27017")  # URL de conexión a MongoDB

@app.route('/consulta', methods=['POST'])
def consulta():
    data = request.get_json()
    parametro = data['parametro']
    k = data['k']

    db = client['Proyecto2BDD2']  # Nombre de la base de datos en MongoDB
    collection = db['articles']  # Nombre de la colección en MongoDB

    # Ejecutar la consulta en MongoDB y medir tiempos
    start_time = time.time()
    resultado = collection.find(
    { '$text': { '$search': parametro } },
    { 'score': { '$meta': 'textScore' } }).sort([('score', { '$meta': 'textScore' })]).limit(k)
    end_time = time.time()

    # Convertir los resultados en una lista de diccionarios
    resultados_lista = []
    for documento in resultado:
        documento['_id'] = str(documento['_id'])
        resultados_lista.append(documento)

    tiempo_ejecucion = end_time - start_time

    response = {
        'resultados': resultados_lista,
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
    return "Api para MongoDB"

if __name__ == '__main__':
    app.run(port=5011)