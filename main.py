from inverted_index.index import InvertIndex

textos = ["libro1.txt","libro2.txt","libro3.txt","libro4.txt","libro5.txt","libro6.txt"]
test = InvertIndex("prueba",300000,"Data.csv")
#test.SPIMIConstruction()
merge_blocks = test.index_blocks()
test.write_index_tf_idf(merge_blocks, test.path_index, len(merge_blocks))
#test.save_index("index_file")
#print(test.retrieval("gandalf y los anillos", 3))