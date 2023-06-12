from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

# Configura la aplicación Flask
app = Flask(__name__)
CORS(app)  # Permite peticiones CORS desde el cliente Vue.js

# Configura la conexión a la base de datos PostgreSQL
connection = psycopg2.connect(
    host='localhost',
    database='tu_basededatos',
    user='tu_usuario',
    password='tu_contraseña'
)
cursor = connection.cursor()

# Define una ruta para ejecutar la consulta con parámetros proporcionados por el usuario
@app.route('/consulta')
def consulta():
    parametro = request.args.get('parametro')

    try:
        consulta = 'SELECT * FROM tabla WHERE columna = %s'
        cursor.execute(consulta, (parametro,))
        result = cursor.fetchall()
        return jsonify(result)
    except psycopg2.Error as e:
        print('Error en la consulta:', e)
        return jsonify(error='Ocurrió un error en la consulta.'), 500

# Ejecuta la aplicación Flask en el puerto especificado
if __name__ == '__main__':
    app.run(port=3000)
