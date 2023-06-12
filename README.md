# Proyecto 2

### Integrantes
* Valeria Espinoza Tarazona - (202110109)
* nombre
* nombre
* nombre
* nombre

## Introducción

## Database
### JSON to CSV
### PostgreSQL DB
Creamos un Database con nombre 'Proyecto2BDD2' y creamos la tabla Articles con el siguiente comando
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
