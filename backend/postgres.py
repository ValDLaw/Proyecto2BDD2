import time
import psycopg2
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, origin="*", supports_credentials=True)
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="Proyecto2BDD2",
    user="postgres",
    password="onepiecelaw"
)

@app.route('/consulta', methods=['POST'])
def consulta():
    data = request.get_json()
    parametro = data['parametro']
    k = data['k']

    cursor = conn.cursor()

    # Ejecutar la consulta en PostgreSQL y medir el tiempo de ejecución
    start_time = time.time()
    query = "SELECT * FROM article WHERE submitter = %s LIMIT %s"
    cursor.execute(query, (parametro, k,))
    resultados = cursor.fetchall()
    end_time = time.time()

    tiempo_ejecucion = end_time - start_time

    cursor.close()
    print(resultados)

    response = {
        'resultados': resultados,
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
    return "Api para PostgreSQL"

if __name__ == '__main__':
    app.run(port=5002)