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
                    total_tf[term] = 1
                doc_term_freq[term] = 1
            
        doc_tf[doc_id] = doc_term_freq
    
    total_tf = sorted(total_tf.items(), key= lambda tup: tup[1], reverse=True)
    return doc_tf, total_tf
    
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
        if df == 0:
            idf = 0
        else:
            idf = np.log10((N / df))
        idf_freq[term] = idf
    return idf

def cosine_sim(Q, Doc):  
  return round(np.dot(Q, Doc) / (np.linalg.norm(Q)*np.linalg.norm(Doc)),3)

def create_inverted_index(textos_tfidf):
    matriz = []
    for doc1 in textos_tfidf.values():
        row = []
        array1 = np.array(list(doc1))
        for doc2 in textos_tfidf.values():
            array2 = np.array(list(doc2))
            row.append(cosine_sim(array1, array2))
        matriz.append(row)

    count = 0
    print("      doc1   doc2   doc3   doc4   doc5   doc6")
    for row in matriz:
        print("doc" + str(count), row)
        count += 1

def compute_tfidf(data, collection):
    tfidf = {} #para tener score tfidf
    idf_freq = {} #se va updateando cada vez que se saque idf de una palabra, para no recalcular
    index = {} #para tener 
    length = {} #para tener vector normalizado de cada abstract

    term_freq, orden_keywords = compute_tf(collection) # Contar la frecuencia de cada término en cada documento

    for doc_id, doc in enumerate(collection):
        nameDoc = str(data.iloc[int(doc_id),0])
        smoothed_tf = []

        for tup_term in orden_keywords:
            term = tup_term[0]
            #compute index
            if term in term_freq[doc_id]:
                tf_t_d = term_freq[doc_id][term]
                if term_freq[doc_id][term] != 0:
                    if term in index:
                        index[term].append((nameDoc, tf_t_d))
                    else:
                        index[term] = [(nameDoc, tf_t_d)]
                #Term Frequency + Smoothing
                tf = np.log10(tf_t_d +1)
                idf = compute_idf(term, idf_freq, term_freq, len(collection))
                smoothed_tf.append(round(tf * idf, 3))
            else:
                smoothed_tf.append(0)
        
        #compute length
        array = np.array(list(smoothed_tf))
        length[nameDoc] = np.linalg.norm(array)
        tfidf[nameDoc] = smoothed_tf
    
    #create_inverted_index(tfidf) esto no es el inverted index

    return length, idf_freq, index
