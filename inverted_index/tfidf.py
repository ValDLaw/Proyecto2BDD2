import numpy as np

def compute_tf(collection):
    doc_tf = {}
    total_tf = {}
    for doc_id, doc in enumerate(collection):
        doc_term_freq = {} #cuantas veces aparece cada term en cada doc
        for term in doc:
            if term in doc_term_freq:
                doc_term_freq[term] += 1
                total_tf[term] += 1
            else:
                if term not in total_tf:
                    total_tf[term] = 0
                doc_term_freq[term] = 0
            
        doc_tf[doc_id] = doc_term_freq
    
    total_tf = sorted(total_tf.items(), key= lambda tup: tup[1], reverse=True)
    return doc_tf, total_tf

def compute_idf(term, idf_freq, term_freq, N):
    if term in idf_freq: #si ya existe para term
        idf = idf_freq[term]
    else:
        df = 0 #en cuantos docs aparece term
        for num in range(N):
            if term in term_freq[num]:
                df += 1
        idf = np.log10(N / df)
        idf_freq[term] = idf
    return idf

def compute_tfidf(collection):
    tfidf_dict = {} # Contar tfidf de cada término en cada documento
    idf_freq = {}
    term_freq, orden_keywords = compute_tf(collection) # Contar la frecuencia de cada término en cada documento

    index = {}
    for doc_id, doc in enumerate(collection):
        lstWords = []
        nameDoc = "doc"+str(doc_id+1)
        
        for tup_term in orden_keywords:
            term = tup_term[0]

            if term in term_freq[doc_id]:
                if term_freq[doc_id][term] != 0:
                    if term in index:
                        index[term].append((nameDoc, term_freq[doc_id][term]))
                    else:
                        index[term] = [(nameDoc, term_freq[doc_id][term])]
                #Term Frequency + Smoothing
                tf = np.log10(term_freq[doc_id][term]+1)
                idf = compute_idf(term, idf_freq, term_freq, len(collection))
                lstWords.append(round(tf * idf, 3))
            else:
                lstWords.append(0)
        tfidf_dict[nameDoc] = lstWords

    return tfidf_dict, idf_freq, index

def compute_length(tfidf):
    length = {}
    for doc in tfidf.items():
        array = np.array(list(doc[1]))
        length[doc[0]] = np.linalg.norm(array)

    return length

def cosine_sim(Q, Doc):  
  return round(np.dot(Q, Doc) / (np.linalg.norm(Q)*np.linalg.norm(Doc)),3)
