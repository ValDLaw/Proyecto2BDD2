from inverted_index.index import InvertIndex

textos = ["libro1.txt","libro2.txt","libro3.txt","libro4.txt","libro5.txt","libro6.txt"]
test = InvertIndex("index_file")
test.building(textos)
test.save_index("index_file")
print(test.retrieval("gandalf y los anillos", 3))