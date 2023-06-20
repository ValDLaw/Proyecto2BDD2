import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origin="*", supports_credentials=True)

@app.route('/consulta', methods=['POST'])
def consulta():
    data = request.get_json()
    parametro = data['parametro']
    k = data['k']

    # Ejecutar la consulta en PostgreSQL y medir el tiempo de ejecución
    start_time = time.time()
    resultados = []
    end_time = time.time()

    tiempo_ejecucion = end_time - start_time

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
    app.run(port=5003)