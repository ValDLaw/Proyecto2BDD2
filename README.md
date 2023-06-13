# Proyecto 2

### Integrantes
* Valeria Espinoza Tarazona - (202110109)
* Enzo Camizán Vidal - (202110047)
* Diego Guerra Chevarría - (202010137)
* Valentín Quezada Amour - (202120570)
* Sofía García Quintana - (202110567)

## Introducción

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
