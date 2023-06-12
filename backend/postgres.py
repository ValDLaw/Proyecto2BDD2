from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

# Configura la aplicación Flask
app = Flask(__name__)
CORS(app)

# Configura la conexión a la base de datos PostgreSQL
connection = psycopg2.connect(
    host='localhost',
    database='Proyecto2BDD2',
    user='postgres',
    password='onepiecelaw'
)
cursor = connection.cursor()


@app.route('/consulta')
def consulta():
    parametro = request.args.get('parametro')

    try:
        consulta = 'SELECT * FROM article WHERE columna = %s'
        cursor.execute(consulta, (parametro,))
        result = cursor.fetchall()
        return jsonify(result)
    except psycopg2.Error as e:
        print('Error en la consulta:', e)
        return jsonify(error='Ocurrió un error en la consulta.'), 500

# Ejecuta la aplicación Flask en el puerto especificado
if __name__ == '__main__':
    app.run(port=5432)
