from SPARQLWrapper import SPARQLWrapper, JSON

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/musica_portuguesa"

def exec_query(query):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        return sparql.query().convert()
    except Exception as e:
        print(f"Erro ao executar a query SPARQL: {e}")
        return None

def exec_update(query):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setMethod('POST')
    try:
        sparql.query()
        return True
    except Exception as e:
        print(f"Erro ao executar o UPDATE SPARQL: {e}")
        return False