from pymongo import MongoClient

uri = 'mongodb://localhost:27017'

client = MongoClient(uri)
db = client['Proyecto2BDD2']
article = db['article']