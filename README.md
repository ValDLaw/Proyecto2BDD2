# Proyecto 2

### Integrantes
* Valeria Espinoza Tarazona (202110109)
* Enzo Camizán Vidal (202110047)
* Diego Guerra Chevarría (202010137)
* Valentín Quezada Amour (202120570)
* Sofía García Quintana (202110567)

## Introducción
### Descripción del dominio de datos

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

## Frontend
### Diseño del índice con PostgreSQL/MongoDB

### Análisis comparativo con su propia implementación

### Screenshots de la GUI


## Database
### JSON to CSV
### PostgreSQL DB
Creamos un Database con nombre 'Proyecto2BDD2' y creamos la tabla Articles con el siguiente comando:
``` sql
CREATE TABLE article (
	id FLOAT PRIMARY KEY,
	submitter VARCHAR(40),
	authors VARCHAR(80),
	title VARCHAR(200),
	categories VARCHAR(30),
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
