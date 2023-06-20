# Proyecto 2 - Bases de Datos II

### Integrantes
* Valeria Espinoza Tarazona (202110109)
* Enzo Camizán Vidal (202110047)
* Diego Guerra Chevarría (202010137)
* Valentín Quezada Amour (202120570)
* Sofía García Quintana (202110567)

## Introducción
La recuperación de información y lectura en documentos de texto consiste en un procedimiento con trasfondo algorítmico un tanto complejo y bastante interesante. Hoy en día, existe una amplia variedad de técnicas y algoritmos planteados para realizar búsquedas en archivos textuales, manteniendo una efectividad precisa y buscando la mayor eficiencia posible. A continuación, se experimentará con el método del índice invertido en la búsqueda de textos para el dataset de ArXiv, el servicio open source de distribución de archivos.

### Objetivo del proyecto
El presente proyecto está enfocado en la construcción óptima de un índice invertido para tareas de búsqueda y recuperación en documentos de texto. Consistirá en la implementación de un sistema backend-frontend, con código de lenguaje Python en el backend y una GUI intuitiva como frontend. El objetivo principal será comparar el desempeño computacional de nuestra implementación propia del índice invertido con el de los gestores de bases de datos PostgreSQL y MongoDB. Nuestra GUI será capaz entonces de mostrar resultados para los tres escenarios, y a partir de ello, analizaremos los tiempos de ejecución para determinar la eficiencia de nuestro índice invertido.

### Descripción del dominio de datos
El dominio de datos escogido para este proyecto consiste en un conjunto de más de 1.7 millones de papers académicos almacenados en la base de datos de ArXiv. La gran mayoría de estos archivos están enfocados en las disciplinas de física, matemática, ingeniería, biología, ciencias de la computación, y entre otras áreas académicas. Cada entrada en este repositorio cuenta con el título de su artículo, el autor, las categorías que abarca, un corto resumen de su contenido y su fecha de actualización. Fue escogido debido a la consistencia y simpleza de los atributos seleccionados para cada fila, además de contar con una cantidad considerable de data para trabajar.

![image](https://github.com/ValDLaw/Proyecto2BDD2/assets/91209653/b0d83442-7283-4994-89da-de70a4df3a53)

## Backend
### Construcción del índice invertido

**preprocesamiento.py**

`tokenizar(texto)`:
 recibe como input un texto que pasa a minúsculas y luego utiliza "word_tokenize" de NLTK. Devuelve una lista de tokens.

`eliminarStopWords(tokenText)`: recibe una lista de tokens como entrada y elimina los stopwords. También hace un proceso de stemming utilizando "SnowballStemmer" de NLTK para reducir las palabras a su forma raíz. Devuelve una lista de tokens procesados.

`preprocesar_query(query)`: toma una consulta de texto como entrada y la procesa utilizando `tokenizar` y `eliminarStopWords`. Devuelve una lista de tokens procesados.

`preprocesar_textos(textos)`: es de forma muy similar a `preprocesar_query`.

**tfidf.py**

`compute_tf(collection)`: toma una colección de documentos como entrada y calcula la frecuencia de término (tf) para cada término en cada documento. Devuelve un diccionario "doc_tf" que contiene la frecuencia de término de cada documento, y un diccionario llamado "total_tf" que contiene la suma total de la frecuencia de término de cada término en todos los documentos.

`compute_idf(term, idf_freq, term_freq, N)`: calcula la frecuencia inversa de documento (idf) para un término dado. Si el **idf** ya existe se devuelve. De lo contrario, se calcula contando en cuántos documentos aparece el término y usando la fórmula **idf = log10(N/df)**. **N** es el número total de documentos y **df** es el número de documentos en los que aparece el término. El **idf** calculado se almacena en el diccionario "idf_freq" y se devuelve.

`cosine_sim(Q, Doc)`: calcula la similitud coseno entre dos vectores: consulta (Q) y documento (Doc). Utiliza np.dot para realizar el producto escalar de los dos vectores y np.linalg.norm para calcular las normas. Devuelve el resultado de la similitud coseno redondeado a 3 decimales.

`create_inverted_index(textos_tfidf)`: crea y muestra la matriz de similitud coseno entre todos los documentos en el conjunto de textos representado por "textos_tfidf".

`compute_tfidf(collection)`: calcula el **tf-idf** para cada término en cada documento en la colección de documentos. Utiliza "compute_tf" para obtener la frecuencia de término. Además, se calcula y almacena la longitud (norma) de cada vector de documento en el diccionario "length". También se crea un índice invertido en "index", donde cada término se asigna a una lista de pairs que contienen el nombre del documento y la frecuencia del término en ese documento.

**index.py**

`building(self, textos)`: construye el índice invertido a partir de una colección de textos. Utiliza la función "preprocesar_textos" y luego usa "compute_tfidf" para obtener el índice invertido, la frecuencia inversa de documento (idf) y la longitud de los vectores de documento. Luego guarda todo en el archivo especificado por "index_file" utilizando el método "save_index".

`retrieval(self, query, k)`: realiza una consulta en el índice invertido. Recibe como input la query de texto y una cantidad **k** de documentos más relevantes que se quiere recuperar. Se preprocesa de la consulta con "preprocesar_query" y calcula el **tf-idf** del query y el score de similitud coseno entre el query y los documentos. Se ordena los documentos de forma descendente y regresa los **k** más relevantes.

`save_index(self, filename)`: guarda el índice invertido, el **idf** y la longitud de los vectores de documento en un archivo "filename".

`load_index(self, filename)`: carga el índice invertido, el **idf** y la longitud de los vectores de documento desde un archivo "filename".

### Manejo de memoria secundaria

### Ejecución óptima de consultas

### Diseño del índice con PostgreSQL
Creamos un Database con nombre 'Proyecto2BDD2' y creamos la tabla Articles con el siguiente comando:
``` sql
CREATE TABLE article (
	id VARCHAR(255) PRIMARY KEY,
	submitter TEXT,
	authors TEXT,
	title TEXT,
	categories TEXT,
	abstract TEXT,
	update_date DATE,
	authors_parsed TEXT
);
```
Nos conectamos a nuestra Database desde terminal y ejecutamos lo siguiente para poder insertar todos los valores del csv a nuestra tabla:
``` sql
\copy article FROM '/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/dataset/arxiv-metadata-1.csv' WITH (FORMAT CSV, DELIMITER ',', QUOTE '"', HEADER);
\copy article FROM '/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/dataset/arxiv-metadata-2.csv' WITH (FORMAT CSV, DELIMITER ',', QUOTE '"', HEADER);
\copy article FROM '/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/dataset/arxiv-metadata-3.csv' WITH (FORMAT CSV, DELIMITER ',', QUOTE '"', HEADER);
```  

Luego, añadimos la columna vectorized_content y la llenamos de la siguiente manera:  
``` sql
ALTER TABLE article ADD COLUMN vectorized_content TSVECTOR;
UPDATE article SET vectorized_content = setweight(to_tsvector('english', title), 'A') || setweight(to_tsvector('english', abstract), 'B') || setweight(to_tsvector('english', authors), 'C');
```

Creamos el archivo *postgres.py* con una api con única ruta '/consultas', en la cual recibíamos como parámetros el texto de búsqueda y un entero k. Esta nos devolvía una lista con el top k de los artículos que hacian match y el tiempo de ejecución de la consulta.  

``` python
@app.route('/consulta', methods=['POST'])
def consulta():
    data = request.get_json()
    parametro = data['parametro']
    k = data['k']

    cursor = conn.cursor()
    conn.rollback()

    # Ejecutar la consulta en PostgreSQL y medir el tiempo de ejecución
    start_time = time.time()
    query = "SELECT * FROM article WHERE vectorized_content @@ plainto_tsquery('english', %s) LIMIT %s;"
    cursor.execute(query, (parametro, k))
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
```  
 Notamos que la query empleada fue la siguiente:  

 ``` sql
 SELECT * FROM article WHERE vectorized_content @@ plainto_tsquery('english', %s) LIMIT %s;
 ```  

### Diseño del índice con MongoDB  
Importamos los datos del archivo 'arxiv-metadata-oai-snapshot.json' a nuestra Database en MongoDB usando la herramiento Import de MongoDB Compass. Luego, creamos una colección llamada **articles**.  
![Articles](images/mongodb_articles.png)  

Luego, creamos el índice compuesto en nuestra colección, utilizando los campos *title*, *abstract* y *authors*.    

Creamos el archivo *mongodb.py* con una api con única ruta '/consultas', en la cual recibíamos como parámetros el texto de búsqueda y un entero k. Esta nos devolvía una lista con el top k de los artículos que hacian match y el tiempo de ejecución de la consulta.   

 ``` python
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
 ```  

  Notamos que la query empleada fue la siguiente:  

 ``` c++
resultado = collection.find(
    { '$text': { '$search': parametro } },
    { 'score': { '$meta': 'textScore' } }).sort([('score', { '$meta': 'textScore' })]).limit(k)
 ```  

## Frontend

### Screenshots de la GUI
Se creo un proyecto en Vue para la búsqueda textual. En la página principal, se le pide al usuario ingresar su consulta textual y un entero k que es la cantidad de artículos que se devolverán.  
![image](https://github.com/ValDLaw/Proyecto2BDD2/assets/91209653/94eb9648-4416-4a29-86d1-3630434a3600)  

Al presionar el botón *search*, se devuelve el top k de artíulos más relacionados. Asimismo, se le ofrece al usuario 3 formas de obtener este resultado: PostgreSQL, MongoDB o con un Self Inverted Index, el cual usa el método de SPIMI. El siguiente resultado es usando la base de datos de PostgreSQL:  
![image](https://github.com/ValDLaw/Proyecto2BDD2/assets/91209653/9d25119b-7d9f-4a7f-80d6-b4dcc692c838)

En segundo lugar, tenemos los resultados con MongoDB:  
![image](https://github.com/ValDLaw/Proyecto2BDD2/assets/91209653/6b7e5f62-539c-49d6-98a8-1b4149f673fe)

Finalmente, los artículos más relacionados usando el indíce invertido de código propio.  

### Análisis comparativo con su propia implementación

## Dataset
El Dataset empleado para el proyecto fue el arXiv Dataset, obtenido del siguiente enlace: https://www.kaggle.com/datasets/Cornell-University/arxiv, el cual tiene la información de un total de 2272690 artículos escolares.  

### JSON to CSV
Por temas de facilidad de manejo de la data, dividimos dicho archivo json en 3 archivos csv, usando las siguientes líneas de código.  

``` python
df = []
# Modificar ubicacion
with open("/Users/ValDLaw/Desktop/arxiv-metadata-oai-snapshot.json", "r") as f:
    #print("abierto")
    for line in f:
        data = json.loads(line)
        df.append(data)
        #print(data)

df = pd.DataFrame(df)
df = df.drop(columns=["doi", "journal-ref", "comments", "license", "report-no", "versions"])
df = df.replace('\n', ' ', regex=True)

# Modificar ubicacion
df.to_csv("/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/dataset/arxiv-metadata.csv", header=True, index=False)

# Modificar ubicacion
csv_file = '/Users/ValDLaw/Documents/GitHub/2023-1/BDD2/Proyecto2BDD2/dataset/arxiv-metadata.csv'
num_files = 3
df = pd.read_csv(csv_file)
rows_per_file = len(df) // num_files
split_dfs = [df[i*rows_per_file:(i+1)*rows_per_file] for i in range(num_files)]

for i, split_df in enumerate(split_dfs):
    split_df.to_csv(f'arxiv-metadata-{i+1}.csv', index=False, header=None, sep=',')
 ``` 