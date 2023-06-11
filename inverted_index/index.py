from inverted_index.preprocesamiento import preprocesar_query, preprocesar_textos
from inverted_index.tfidf import compute_tfidf

class InvertIndex:
    def __init__(self, index_file):
        self.index_file = index_file
        self.index = {}
        self.idf = {}
        self.length = {}
    
    def building(self, textos):
        collection = preprocesar_textos(textos)
        self.index, self.idf, self.length = compute_tfidf(collection)
        self.save_index(self.index_file)

    def retrieval(self, query, k):
        score = {}
        query_terms = preprocesar_query(query)
        
        # calcular el tf-idf del query
        query_tfidf = {term: (query_terms.count(term) / len(query_terms)) * self.idf.get(term, 0)
                       for term in query_terms}
        
        # calcular el score de cada documento
        for term, query_weight in query_tfidf.items():
            if term in self.index:
                postings = self.index[term]
                for doc_id, doc_weight in postings:
                    score[doc_id] = score.get(doc_id, 0) + query_weight * doc_weight
                
        # ordenar el score de forma descendente
        result = sorted(score.items(), key= lambda tup: tup[1], reverse=True)

        # retornar los k documentos mas relevantes
        return result[:k]

    def save_index(self,filename):
        with open(filename, 'w') as file:
            file.write(str(self.index) + '\n')
            file.write(str(self.idf) + '\n')
            file.write(str(self.length) + '\n')
    
    def load_index(self, filename):
        with open(filename, 'r') as file:
            self.index = eval(file.readline())
            self.idf = eval(file.readline())
            self.length = eval(file.readline())