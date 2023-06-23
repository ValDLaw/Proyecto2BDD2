from inverted_index.index import InvertIndex

test = InvertIndex("prueba",2000000,"arxiv-metadata.csv")
#test.SPIMIConstruction()
#merge_blocks = test.index_blocks()
#test.write_index_tf_idf(merge_blocks, len(merge_blocks))
result = test.prueba2()
print(result)
#test.save_index("index_file")
#print(test.retrieval("gandalf y los anillos", 3))