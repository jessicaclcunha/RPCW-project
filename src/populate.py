from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD, OWL
import re
import time
import sys

# ─────────────────────────────────────────────
# Namespace
# ─────────────────────────────────────────────
NS = Namespace("http://rpcw.di.uminho.pt/2026/music-ontology/")

def clean_id(text):
    if not text:
        return "Desconhecido"
    n = text.strip().lower()
    for src, dst in [
        (r'[àáâãäå]','a'), (r'[èéêë]','e'), (r'[ìíîï]','i'),
        (r'[òóôõö]','o'), (r'[ùúûü]','u'), (r'[ç]','c'),
        (r'[ñ]','n'),  (r'[ý]','y'),
    ]:
        n = re.sub(src, dst, n)
    n = re.sub(r'[^\w]', '_', n)
    n = re.sub(r'_+', '_', n).strip('_')
    return n.capitalize() or "Desconhecido"


# ─────────────────────────────────────────────
# SPARQL helper com retry e paginação
# ─────────────────────────────────────────────
ENDPOINT = "https://dbpedia.org/sparql"
PAGE_SIZE = 1000

def run_query(query: str, retries: int = 3, delay: float = 5.0) -> list[dict]:
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(60)
    sparql.setQuery(query)
    for attempt in range(retries):
        try:
            results = sparql.query().convert()
            return results["results"]["bindings"]
        except Exception as e:
            print(f"  ⚠  Tentativa {attempt+1}/{retries} falhou: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    print("  ✗  Query falhou definitivamente, a continuar...")
    return []


def paginate(query_template: str, label: str) -> list[dict]:
    """Corre uma query com paginação automática até esgotar resultados."""
    all_rows = []
    offset = 0
    print(f"\n[{label}]")
    while True:
        q = query_template + f"\nLIMIT {PAGE_SIZE} OFFSET {offset}"
        rows = run_query(q)
        print(f"  offset={offset:5d}  → {len(rows)} linhas")
        all_rows.extend(rows)
        if len(rows) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(1.5)   # respeita rate-limit do DBpedia
    print(f"  Total: {len(all_rows)} linhas")
    return all_rows


# ─────────────────────────────────────────────
# Helpers para adicionar triplos
# ─────────────────────────────────────────────
def add_str(g, subj, prop, bindings, key):
    if key in bindings:
        g.add((subj, prop, Literal(bindings[key]["value"], datatype=XSD.string)))

def add_int(g, subj, prop, bindings, key):
    if key in bindings:
        try:
            g.add((subj, prop, Literal(int(bindings[key]["value"]), datatype=XSD.integer)))
        except ValueError:
            pass

def add_year_from_date(g, subj, prop, bindings, key):
    if key in bindings:
        val = bindings[key]["value"]
        m = re.search(r'\d{4}', val)
        if m:
            g.add((subj, prop, Literal(int(m.group()), datatype=XSD.integer)))

def uri_from_val(bindings, key):
    """Devolve um URI rdflib a partir da binding de uma variável DBpedia."""
    if key in bindings:
        return URIRef(bindings[key]["value"])
    return None


# ─────────────────────────────────────────────
# QUERY 1 – Artistas Solo Portugueses
# ─────────────────────────────────────────────
Q_ARTISTAS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?artist ?name ?birthDate ?deathDate ?birthPlace ?birthPlaceName
                ?nationality ?abstract ?wikiPage
WHERE {
  { ?artist dct:subject dbc:Portuguese_musicians }
  UNION
  { ?artist dct:subject dbc:Portuguese_male_singers }
  UNION
  { ?artist dct:subject dbc:Portuguese_female_singers }
  UNION
  { ?artist dct:subject dbc:Portuguese_pop_singers }
  UNION
  { ?artist dct:subject dbc:Portuguese_rock_musicians }
  UNION
  { ?artist dct:subject dbc:Portuguese_jazz_musicians }
  UNION
  { ?artist dct:subject dbc:Portuguese_fado_singers }
  UNION
  { ?artist dct:subject dbc:Portuguese_folk_singers }
  UNION
  { ?artist dct:subject/skos:broader dbc:Portuguese_musicians }

  ?artist a dbo:MusicalArtist ;
          rdfs:label ?name .
  FILTER(LANG(?name) = "pt" || LANG(?name) = "en")

  OPTIONAL { ?artist dbo:birthDate ?birthDate }
  OPTIONAL { ?artist dbo:deathDate ?deathDate }
  OPTIONAL {
    ?artist dbo:birthPlace ?birthPlace .
    ?birthPlace rdfs:label ?birthPlaceName .
    FILTER(LANG(?birthPlaceName) = "pt" || LANG(?birthPlaceName) = "en")
  }
  OPTIONAL { ?artist dbp:nationality ?nationality }
  OPTIONAL { ?artist dbo:abstract ?abstract . FILTER(LANG(?abstract) = "pt") }
  OPTIONAL { ?artist foaf:isPrimaryTopicOf ?wikiPage }
}
"""

# ─────────────────────────────────────────────
# QUERY 2 – Bandas Portuguesas
# ─────────────────────────────────────────────
Q_BANDAS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?band ?name ?startYear ?endYear ?hometown ?hometownName ?abstract ?wikiPage
WHERE {
  { ?band dct:subject dbc:Portuguese_musical_groups }
  UNION
  { ?band dct:subject dbc:Portuguese_rock_music_groups }
  UNION
  { ?band dct:subject dbc:Portuguese_pop_music_groups }
  UNION
  { ?band dct:subject dbc:Portuguese_metal_bands }
  UNION
  { ?band dct:subject dbc:Portuguese_punk_rock_groups }
  UNION
  { ?band dct:subject dbc:Portuguese_hip_hop_groups }
  UNION
  { ?band dct:subject/skos:broader dbc:Portuguese_musical_groups }

  ?band a dbo:Band ;
        rdfs:label ?name .
  FILTER(LANG(?name) = "pt" || LANG(?name) = "en")

  OPTIONAL { ?band dbo:activeYearsStartYear ?startYear }
  OPTIONAL { ?band dbo:activeYearsEndYear ?endYear }
  OPTIONAL {
    ?band dbo:hometown ?hometown .
    ?hometown rdfs:label ?hometownName .
    FILTER(LANG(?hometownName) = "pt" || LANG(?hometownName) = "en")
  }
  OPTIONAL { ?band dbo:abstract ?abstract . FILTER(LANG(?abstract) = "pt") }
  OPTIONAL { ?band foaf:isPrimaryTopicOf ?wikiPage }
}
"""

# ─────────────────────────────────────────────
# QUERY 3 – Membros de Bandas Portuguesas
# ─────────────────────────────────────────────
Q_MEMBROS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?band ?bandName ?member ?memberName
WHERE {
  { ?band dct:subject dbc:Portuguese_musical_groups }
  UNION
  { ?band dct:subject/skos:broader dbc:Portuguese_musical_groups }

  ?band a dbo:Band ;
        rdfs:label ?bandName .
  FILTER(LANG(?bandName) = "pt" || LANG(?bandName) = "en")

  ?band dbo:bandMember ?member .
  ?member rdfs:label ?memberName .
  FILTER(LANG(?memberName) = "pt" || LANG(?memberName) = "en")
}
"""

# ─────────────────────────────────────────────
# QUERY 4 – Álbuns de Artistas/Bandas Portuguesas
# ─────────────────────────────────────────────
Q_ALBUNS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?album ?albumName ?artist ?artistName ?releaseDate ?label ?labelName ?genre ?genreName
WHERE {
  { ?artist dct:subject dbc:Portuguese_musicians }
  UNION
  { ?artist dct:subject dbc:Portuguese_musical_groups }
  UNION
  { ?artist dct:subject dbc:Portuguese_fado_singers }
  UNION
  { ?artist dct:subject/skos:broader dbc:Portuguese_musicians }
  UNION
  { ?artist dct:subject/skos:broader dbc:Portuguese_musical_groups }

  ?album dbo:artist ?artist ;
         a dbo:Album ;
         rdfs:label ?albumName .
  FILTER(LANG(?albumName) = "pt" || LANG(?albumName) = "en")

  ?artist rdfs:label ?artistName .
  FILTER(LANG(?artistName) = "pt" || LANG(?artistName) = "en")

  OPTIONAL { ?album dbo:releaseDate ?releaseDate }
  OPTIONAL {
    ?album dbo:recordLabel ?label .
    ?label rdfs:label ?labelName .
    FILTER(LANG(?labelName) = "pt" || LANG(?labelName) = "en")
  }
  OPTIONAL {
    ?album dbo:genre ?genre .
    ?genre rdfs:label ?genreName .
    FILTER(LANG(?genreName) = "pt" || LANG(?genreName) = "en")
  }
}
"""

# ─────────────────────────────────────────────
# QUERY 5 – Músicas/Singles de artistas portugueses
# ─────────────────────────────────────────────
Q_MUSICAS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?song ?songName ?artist ?artistName ?album ?albumName ?releaseDate ?duration
WHERE {
  { ?artist dct:subject dbc:Portuguese_musicians }
  UNION
  { ?artist dct:subject dbc:Portuguese_musical_groups }
  UNION
  { ?artist dct:subject dbc:Portuguese_fado_singers }
  UNION
  { ?artist dct:subject/skos:broader dbc:Portuguese_musicians }

  ?song dbo:artist ?artist ;
        a dbo:Single ;
        rdfs:label ?songName .
  FILTER(LANG(?songName) = "pt" || LANG(?songName) = "en")

  ?artist rdfs:label ?artistName .
  FILTER(LANG(?artistName) = "pt" || LANG(?artistName) = "en")

  OPTIONAL { ?song dbo:album ?album . ?album rdfs:label ?albumName . FILTER(LANG(?albumName) = "pt" || LANG(?albumName) = "en") }
  OPTIONAL { ?song dbo:releaseDate ?releaseDate }
  OPTIONAL { ?song dbo:runtime ?duration }
}
"""

# ─────────────────────────────────────────────
# QUERY 6 – Géneros Musicais Portugueses
# ─────────────────────────────────────────────
Q_GENEROS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?entity ?entityName ?genre ?genreName
WHERE {
  { ?entity dct:subject dbc:Portuguese_musicians }
  UNION
  { ?entity dct:subject dbc:Portuguese_musical_groups }
  UNION
  { ?entity dct:subject dbc:Portuguese_fado_singers }
  UNION
  { ?entity dct:subject/skos:broader dbc:Portuguese_musicians }
  UNION
  { ?entity dct:subject/skos:broader dbc:Portuguese_musical_groups }

  ?entity dbo:genre ?genre .
  ?genre rdfs:label ?genreName .
  FILTER(LANG(?genreName) = "pt" || LANG(?genreName) = "en")

  ?entity rdfs:label ?entityName .
  FILTER(LANG(?entityName) = "pt" || LANG(?entityName) = "en")
}
"""

# ─────────────────────────────────────────────
# QUERY 7 – Prémios e Nomeações
# ─────────────────────────────────────────────
Q_PREMIOS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?entity ?entityName ?award ?awardName
WHERE {
  { ?entity dct:subject dbc:Portuguese_musicians }
  UNION
  { ?entity dct:subject dbc:Portuguese_musical_groups }
  UNION
  { ?entity dct:subject dbc:Portuguese_fado_singers }
  UNION
  { ?entity dct:subject/skos:broader dbc:Portuguese_musicians }

  ?entity rdfs:label ?entityName .
  FILTER(LANG(?entityName) = "pt" || LANG(?entityName) = "en")

  { ?entity dbo:award ?award }
  UNION
  { ?entity dbp:awards ?award }

  ?award rdfs:label ?awardName .
  FILTER(LANG(?awardName) = "pt" || LANG(?awardName) = "en")
}
"""

# ─────────────────────────────────────────────
# QUERY 8 – Influências entre artistas
# ─────────────────────────────────────────────
Q_INFLUENCIAS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?entity ?entityName ?influence ?influenceName
WHERE {
  { ?entity dct:subject dbc:Portuguese_musicians }
  UNION
  { ?entity dct:subject dbc:Portuguese_musical_groups }
  UNION
  { ?entity dct:subject/skos:broader dbc:Portuguese_musicians }

  ?entity rdfs:label ?entityName .
  FILTER(LANG(?entityName) = "pt" || LANG(?entityName) = "en")

  { ?entity dbo:influencedBy ?influence }
  UNION
  { ?entity dbo:influenced ?influence }

  ?influence rdfs:label ?influenceName .
  FILTER(LANG(?influenceName) = "pt" || LANG(?influenceName) = "en")
}
"""

# ─────────────────────────────────────────────
# QUERY 9 – Festivais de Música em Portugal
# ─────────────────────────────────────────────
Q_FESTIVAIS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?festival ?name ?location ?locationName ?genre ?genreName ?foundingYear
WHERE {
  { ?festival dct:subject dbc:Music_festivals_in_Portugal }
  UNION
  { ?festival dct:subject dbc:Rock_festivals_in_Portugal }
  UNION
  { ?festival dct:subject dbc:Jazz_festivals_in_Portugal }

  ?festival rdfs:label ?name .
  FILTER(LANG(?name) = "pt" || LANG(?name) = "en")

  OPTIONAL { ?festival dbo:location ?location . ?location rdfs:label ?locationName . FILTER(LANG(?locationName) = "pt") }
  OPTIONAL { ?festival dbo:genre ?genre . ?genre rdfs:label ?genreName . FILTER(LANG(?genreName) = "pt" || LANG(?genreName) = "en") }
  OPTIONAL { ?festival dbp:date ?foundingYear }
}
"""

# ─────────────────────────────────────────────
# QUERY 10 – Editoras Discográficas em Portugal
# ─────────────────────────────────────────────
Q_EDITORAS = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?label ?name ?foundingYear ?location ?locationName
WHERE {
  { ?label dct:subject dbc:Record_labels_established_in_Portugal }
  UNION
  { ?label dct:subject dbc:Portuguese_record_labels }
  UNION
  { ?label a dbo:RecordLabel ; dbo:locationCity ?loc .
    ?loc dbo:country <http://dbpedia.org/resource/Portugal> .
  }

  ?label rdfs:label ?name .
  FILTER(LANG(?name) = "pt" || LANG(?name) = "en")

  OPTIONAL { ?label dbo:foundingYear ?foundingYear }
  OPTIONAL { ?label dbo:locationCity ?location . ?location rdfs:label ?locationName . FILTER(LANG(?locationName) = "pt") }
}
"""

# ─────────────────────────────────────────────
# Construção do grafo
# ─────────────────────────────────────────────
def build_graph():
    g = Graph()
    g.bind("", NS)
    g.bind("owl", OWL)

    # Declaração de Classes
    for cls in ["ArtistaSolo", "Banda", "Album", "Musica", "Genero",
                "Editora", "Local", "Festival", "Premio"]:
        g.add((NS[cls], RDF.type, OWL.Class))

    # ── Artistas Solo ──────────────────────────────────────────────
    rows = paginate(Q_ARTISTAS, "Artistas Solo")
    for r in rows:
        name = r["name"]["value"]
        uri = NS[clean_id(name)]
        g.add((uri, RDF.type, NS.ArtistaSolo))
        add_str(g, uri, NS.nome, r, "name")
        add_year_from_date(g, uri, NS.anoNascimento, r, "birthDate")
        add_year_from_date(g, uri, NS.anoFalecimento, r, "deathDate")
        add_str(g, uri, NS.descricao, r, "abstract")
        if "wikiPage" in r:
            g.add((uri, NS.wikiPage, URIRef(r["wikiPage"]["value"])))
        if "birthPlaceName" in r:
            loc_uri = NS[clean_id(r["birthPlaceName"]["value"])]
            g.add((loc_uri, RDF.type, NS.Local))
            g.add((loc_uri, NS.cidade, Literal(r["birthPlaceName"]["value"], datatype=XSD.string)))
            g.add((loc_uri, NS.pais, Literal("Portugal", datatype=XSD.string)))
            g.add((uri, NS.naturalDe, loc_uri))

    # ── Bandas ────────────────────────────────────────────────────
    rows = paginate(Q_BANDAS, "Bandas")
    for r in rows:
        name = r["name"]["value"]
        uri = NS[clean_id(name)]
        g.add((uri, RDF.type, NS.Banda))
        add_str(g, uri, NS.nome, r, "name")
        add_int(g, uri, NS.anoFormacao, r, "startYear")
        add_int(g, uri, NS.anoDissociao, r, "endYear")
        add_str(g, uri, NS.descricao, r, "abstract")
        if "wikiPage" in r:
            g.add((uri, NS.wikiPage, URIRef(r["wikiPage"]["value"])))
        if "hometownName" in r:
            loc_uri = NS[clean_id(r["hometownName"]["value"])]
            g.add((loc_uri, RDF.type, NS.Local))
            g.add((loc_uri, NS.cidade, Literal(r["hometownName"]["value"], datatype=XSD.string)))
            g.add((loc_uri, NS.pais, Literal("Portugal", datatype=XSD.string)))
            g.add((uri, NS.naturalDe, loc_uri))

    # ── Membros de Bandas ─────────────────────────────────────────
    rows = paginate(Q_MEMBROS, "Membros de Bandas")
    for r in rows:
        band_uri = NS[clean_id(r["bandName"]["value"])]
        member_uri = NS[clean_id(r["memberName"]["value"])]
        g.add((band_uri, RDF.type, NS.Banda))
        g.add((band_uri, NS.nome, Literal(r["bandName"]["value"], datatype=XSD.string)))
        g.add((member_uri, RDF.type, NS.ArtistaSolo))
        g.add((member_uri, NS.nome, Literal(r["memberName"]["value"], datatype=XSD.string)))
        g.add((member_uri, NS.membroDe, band_uri))
        g.add((band_uri, NS.temMembro, member_uri))

    # ── Álbuns ────────────────────────────────────────────────────
    rows = paginate(Q_ALBUNS, "Álbuns")
    for r in rows:
        alb_uri = NS[clean_id(r["albumName"]["value"])]
        g.add((alb_uri, RDF.type, NS.Album))
        add_str(g, alb_uri, NS.nome, r, "albumName")
        add_year_from_date(g, alb_uri, NS.anoLancamento, r, "releaseDate")

        artist_uri = NS[clean_id(r["artistName"]["value"])]
        g.add((artist_uri, NS.lancouAlbum, alb_uri))
        g.add((alb_uri, NS.artistaPrincipal, artist_uri))

        if "labelName" in r:
            ed_uri = NS[clean_id(r["labelName"]["value"])]
            g.add((ed_uri, RDF.type, NS.Editora))
            g.add((ed_uri, NS.nome, Literal(r["labelName"]["value"], datatype=XSD.string)))
            g.add((alb_uri, NS.editadoPor, ed_uri))

        if "genreName" in r:
            gen_uri = NS[clean_id(r["genreName"]["value"])]
            g.add((gen_uri, RDF.type, NS.Genero))
            g.add((gen_uri, NS.nome, Literal(r["genreName"]["value"], datatype=XSD.string)))
            g.add((alb_uri, NS.pertenceAoGenero, gen_uri))

    # ── Músicas / Singles ─────────────────────────────────────────
    rows = paginate(Q_MUSICAS, "Músicas/Singles")
    for r in rows:
        song_uri = NS[clean_id(r["songName"]["value"])]
        g.add((song_uri, RDF.type, NS.Musica))
        add_str(g, song_uri, NS.nome, r, "songName")
        add_year_from_date(g, song_uri, NS.anoLancamento, r, "releaseDate")
        if "duration" in r:
            try:
                g.add((song_uri, NS.duracao, Literal(float(r["duration"]["value"]), datatype=XSD.float)))
            except ValueError:
                pass

        artist_uri = NS[clean_id(r["artistName"]["value"])]
        g.add((artist_uri, NS.lancouMusica, song_uri))
        g.add((song_uri, NS.artistaPrincipal, artist_uri))

        if "albumName" in r:
            alb_uri = NS[clean_id(r["albumName"]["value"])]
            g.add((alb_uri, RDF.type, NS.Album))
            g.add((song_uri, NS.pertenceAoAlbum, alb_uri))

    # ── Géneros ───────────────────────────────────────────────────
    rows = paginate(Q_GENEROS, "Géneros")
    for r in rows:
        gen_uri = NS[clean_id(r["genreName"]["value"])]
        g.add((gen_uri, RDF.type, NS.Genero))
        g.add((gen_uri, NS.nome, Literal(r["genreName"]["value"], datatype=XSD.string)))
        entity_uri = NS[clean_id(r["entityName"]["value"])]
        g.add((entity_uri, NS.pertenceAoGenero, gen_uri))

    # ── Prémios ───────────────────────────────────────────────────
    rows = paginate(Q_PREMIOS, "Prémios")
    for r in rows:
        entity_uri = NS[clean_id(r["entityName"]["value"])]
        award_uri = NS[clean_id(r["awardName"]["value"])]
        g.add((award_uri, RDF.type, NS.Premio))
        g.add((award_uri, NS.nome, Literal(r["awardName"]["value"], datatype=XSD.string)))
        g.add((entity_uri, NS.recebeuPremio, award_uri))

    # ── Influências ───────────────────────────────────────────────
    rows = paginate(Q_INFLUENCIAS, "Influências")
    for r in rows:
        entity_uri = NS[clean_id(r["entityName"]["value"])]
        infl_uri = NS[clean_id(r["influenceName"]["value"])]
        g.add((infl_uri, NS.nome, Literal(r["influenceName"]["value"], datatype=XSD.string)))
        g.add((entity_uri, NS.influenciadoPor, infl_uri))

    # ── Festivais ─────────────────────────────────────────────────
    rows = paginate(Q_FESTIVAIS, "Festivais")
    for r in rows:
        name = r["name"]["value"]
        fest_uri = NS[clean_id(name)]
        g.add((fest_uri, RDF.type, NS.Festival))
        add_str(g, fest_uri, NS.nome, r, "name")
        if "locationName" in r:
            loc_uri = NS[clean_id(r["locationName"]["value"])]
            g.add((loc_uri, RDF.type, NS.Local))
            g.add((loc_uri, NS.cidade, Literal(r["locationName"]["value"], datatype=XSD.string)))
            g.add((fest_uri, NS.realizadoEm, loc_uri))
        if "genreName" in r:
            gen_uri = NS[clean_id(r["genreName"]["value"])]
            g.add((gen_uri, RDF.type, NS.Genero))
            g.add((gen_uri, NS.nome, Literal(r["genreName"]["value"], datatype=XSD.string)))
            g.add((fest_uri, NS.pertenceAoGenero, gen_uri))

    # ── Editoras ──────────────────────────────────────────────────
    rows = paginate(Q_EDITORAS, "Editoras")
    for r in rows:
        name = r["name"]["value"]
        ed_uri = NS[clean_id(name)]
        g.add((ed_uri, RDF.type, NS.Editora))
        add_str(g, ed_uri, NS.nome, r, "name")
        add_int(g, ed_uri, NS.anoFundacao, r, "foundingYear")
        if "locationName" in r:
            loc_uri = NS[clean_id(r["locationName"]["value"])]
            g.add((loc_uri, RDF.type, NS.Local))
            g.add((loc_uri, NS.cidade, Literal(r["locationName"]["value"], datatype=XSD.string)))
            g.add((ed_uri, NS.localizadaEm, loc_uri))

    return g


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "musica_portuguesa_completa2.ttl"
    print("=" * 60)
    print("  Construção da KB de Música Portuguesa")
    print("=" * 60)

    g = build_graph()

    print(f"\n{'='*60}")
    print(f"  Total de triplos: {len(g)}")
    print(f"  A serializar para: {output}")
    g.serialize(destination=output, format="turtle")
    print("  ✓ Concluído!")