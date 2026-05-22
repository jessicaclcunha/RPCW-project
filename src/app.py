from flask import Flask, render_template, request, redirect, url_for, jsonify
from query import exec_query, exec_update
import re

app = Flask(__name__)

PREFIX = """
PREFIX : <http://rpcw.di.uminho.pt/2026/music-ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
"""

def rows_of(result):
    if not result or "results" not in result:
        return []
    return result["results"].get("bindings", [])

def g(row, key, default=None):
    return row[key]["value"] if key in row else default

def generos_list():
    q = PREFIX + """
        SELECT DISTINCT ?id WHERE {
            ?id rdfs:subClassOf* :Genero .
            FILTER(?id != :Genero)
        }
    """
    return sorted([
        {"id": g(r, "id").split('/')[-1], "nome": g(r, "id").split('/')[-1]}
        for r in rows_of(exec_query(q))
    ], key=lambda x: x["nome"])

def editoras_list():
    q = PREFIX + "SELECT ?id ?nome WHERE { ?e a :Editora ; :nome ?nome . BIND(STRAFTER(STR(?e), 'music-ontology/') AS ?id) } ORDER BY ?nome"
    return [{"id": g(r,"id"), "nome": g(r,"nome")} for r in rows_of(exec_query(q))]


# ────────────────────────────────────────────────────────────────────
# LISTAGEM PRINCIPAL
# ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    busca         = request.args.get('q', '').strip()
    filtro_genero = request.args.get('genero', '').strip()
    filtro_tipo   = request.args.get('tipo', '').strip()
    filtro_editora= request.args.get('editora', '').strip()
    filtro_ano_de = request.args.get('ano_de', '').strip()
    filtro_ano_ate= request.args.get('ano_ate', '').strip()

    filtros = []
    if busca:
        filtros.append(f'FILTER(CONTAINS(LCASE(?nome), LCASE("{busca}")))')
    if filtro_genero:
        filtros.append(f'?artista :pertenceAoGenero :{filtro_genero} .')
    if filtro_editora:
        filtros.append(f'?artista :pertenceAEditora :{filtro_editora} .')
    if filtro_ano_de:
        filtros.append(f'OPTIONAL {{ ?artista :anoNascimento ?an1 . ?artista :anoFormacao ?an1 }} FILTER(!BOUND(?an1) || ?an1 >= {filtro_ano_de})')
    if filtro_ano_ate:
        filtros.append(f'OPTIONAL {{ ?artista :anoNascimento ?an2 . ?artista :anoFormacao ?an2 }} FILTER(!BOUND(?an2) || ?an2 <= {filtro_ano_ate})')

    if filtro_tipo == 'Solo':
        tipo_filter = '{ ?artista a :ArtistaSolo . BIND("Solo" AS ?tipo) }'
    elif filtro_tipo == 'Banda':
        tipo_filter = '{ ?artista a :Banda . BIND("Banda" AS ?tipo) }'
    else:
        tipo_filter = ('{ ?artista a :ArtistaSolo . BIND("Solo" AS ?tipo) }'
                       ' UNION { ?artista a :Banda . BIND("Banda" AS ?tipo) }')

    query = PREFIX + f"""
        SELECT DISTINCT ?artistaID ?nome ?tipo WHERE {{
            {tipo_filter}
            ?artista :nome ?nome .
            {''.join(filtros)}
            BIND(STRAFTER(STR(?artista), "music-ontology/") AS ?artistaID)
        }} ORDER BY ?nome
    """

    artistas = [
        {"id": g(r, "artistaID"), "nome": g(r, "nome"), "tipo": g(r, "tipo")}
        for r in rows_of(exec_query(query))
    ]

    # Estatísticas de topo
    q_stats = PREFIX + """
        SELECT
          (COUNT(DISTINCT ?solo)   AS ?nSolo)
          (COUNT(DISTINCT ?banda)  AS ?nBanda)
          (COUNT(DISTINCT ?album)  AS ?nAlbum)
          (COUNT(DISTINCT ?musica) AS ?nMusica)
          (COUNT(DISTINCT ?premio) AS ?nPremio)
          (COUNT(DISTINCT ?concerto) AS ?nConcerto)
        WHERE {
          { ?solo    a :ArtistaSolo }
          UNION { ?banda   a :Banda }
          UNION { ?album   a :Album }
          UNION { ?musica  a :Musica }
          UNION { ?premio  a :Premio }
          UNION { ?concerto a :Concerto }
        }
    """
    stats_rows = rows_of(exec_query(q_stats))
    stats = {}
    if stats_rows:
        r = stats_rows[0]
        stats = {
            "solos":    g(r, "nSolo",    "0"),
            "bandas":   g(r, "nBanda",   "0"),
            "albuns":   g(r, "nAlbum",   "0"),
            "musicas":  g(r, "nMusica",  "0"),
            "premios":  g(r, "nPremio",  "0"),
            "concertos":g(r, "nConcerto","0"),
        }

    return render_template(
        'lista.html',
        artistas=artistas,
        generos=generos_list(),
        editoras=editoras_list(),
        busca=busca,
        filtro_genero=filtro_genero,
        filtro_tipo=filtro_tipo,
        filtro_editora=filtro_editora,
        filtro_ano_de=filtro_ano_de,
        filtro_ano_ate=filtro_ano_ate,
        stats=stats,
    )


# ────────────────────────────────────────────────────────────────────
# DETALHE DE ARTISTA
# ────────────────────────────────────────────────────────────────────
@app.route('/artista/<id_artista>')
def detalhe_artista(id_artista):
    query_info = PREFIX + f"""
        SELECT ?nome ?tipo ?anoNasc ?anoForm ?editora ?editoraNome ?bio WHERE {{
            :{id_artista} :nome ?nome .
            OPTIONAL {{ :{id_artista} a :ArtistaSolo . BIND("Solo" AS ?tipo) }}
            OPTIONAL {{ :{id_artista} a :Banda    . BIND("Banda" AS ?tipo) }}
            OPTIONAL {{ :{id_artista} :anoNascimento ?anoNasc }}
            OPTIONAL {{ :{id_artista} :anoFormacao   ?anoForm }}
            OPTIONAL {{ :{id_artista} :pertenceAEditora ?editora .
                        ?editora :nome ?editoraNome }}
            OPTIONAL {{ :{id_artista} :biografia ?bio }}
        }} LIMIT 1
    """
    res = rows_of(exec_query(query_info))
    if not res:
        return "Artista não encontrado", 404

    row = res[0]

    q_generos   = PREFIX + f"SELECT ?nome WHERE {{ :{id_artista} :pertenceAoGenero ?g . BIND(STRAFTER(STR(?g), 'music-ontology/') AS ?nome) }}"
    q_membros   = PREFIX + f"SELECT ?id ?nome WHERE {{ :{id_artista} :temMembro ?m . ?m :nome ?nome . BIND(STRAFTER(STR(?m), 'music-ontology/') AS ?id) }}"
    q_bandas    = PREFIX + f"SELECT ?id ?nome WHERE {{ ?b :temMembro :{id_artista} . ?b :nome ?nome . BIND(STRAFTER(STR(?b), 'music-ontology/') AS ?id) }}"
    q_albuns    = PREFIX + f"SELECT ?id ?nome ?ano WHERE {{ :{id_artista} :lancouAlbum ?a . ?a :nome ?nome . OPTIONAL {{ ?a :anoLancamento ?ano }} BIND(STRAFTER(STR(?a), 'music-ontology/') AS ?id) }} ORDER BY ?ano"
    q_musicas   = PREFIX + f"SELECT ?id ?nome ?album ?albumNome WHERE {{ ?m :interpretadaPor :{id_artista} ; :nome ?nome . BIND(STRAFTER(STR(?m), 'music-ontology/') AS ?id) OPTIONAL {{ ?m :pertenceAoAlbum ?albumR . ?albumR :nome ?albumNome . BIND(STRAFTER(STR(?albumR), 'music-ontology/') AS ?album) }} }} ORDER BY ?albumNome ?nome"
    q_premios   = PREFIX + f"SELECT ?id ?nome ?cat ?org ?ano WHERE {{ :{id_artista} :recebeupremio ?p . ?p :nome ?nome . OPTIONAL{{?p :categoria ?cat}} OPTIONAL{{?p :organizacao ?org}} OPTIONAL{{?p :anoPremio ?ano}} BIND(STRAFTER(STR(?p), 'music-ontology/') AS ?id) }} ORDER BY DESC(?ano)"
    q_concertos = PREFIX + f"SELECT ?id ?nome ?local ?data WHERE {{ :{id_artista} :atuouEm ?c . ?c :nome ?nome . OPTIONAL{{?c :local ?local}} OPTIONAL{{?c :data ?data}} BIND(STRAFTER(STR(?c), 'music-ontology/') AS ?id) }} ORDER BY DESC(?data)"
    q_influencias = PREFIX + f"SELECT ?id ?nome WHERE {{ :{id_artista} :influenciadoPor ?a . ?a :nome ?nome . BIND(STRAFTER(STR(?a), 'music-ontology/') AS ?id) }}"
    q_influenciou = PREFIX + f"SELECT ?id ?nome WHERE {{ ?a :influenciadoPor :{id_artista} . ?a :nome ?nome . BIND(STRAFTER(STR(?a), 'music-ontology/') AS ?id) }}"

    artista = {
        "id":         id_artista,
        "nome":       g(row, "nome"),
        "tipo":       g(row, "tipo", "Solo"),
        "anoNasc":    g(row, "anoNasc"),
        "anoForm":    g(row, "anoForm"),
        "editora":    g(row, "editoraNome"),
        "bio":        g(row, "bio"),
        "generos":    [{"nome": r["nome"]["value"]} for r in rows_of(exec_query(q_generos))],
        "membros":    [{"id": g(r,"id"), "nome": g(r,"nome")} for r in rows_of(exec_query(q_membros))],
        "bandas":     [{"id": g(r,"id"), "nome": g(r,"nome")} for r in rows_of(exec_query(q_bandas))],
        "albuns":     [{"id": g(r,"id"), "nome": g(r,"nome"), "ano": g(r,"ano")} for r in rows_of(exec_query(q_albuns))],
        "musicas":    [{"id": g(r,"id"), "nome": g(r,"nome"), "album": g(r,"album"), "albumNome": g(r,"albumNome")} for r in rows_of(exec_query(q_musicas))],
        "premios":    [{"id": g(r,"id"), "nome": g(r,"nome"), "cat": g(r,"cat"), "org": g(r,"org"), "ano": g(r,"ano")} for r in rows_of(exec_query(q_premios))],
        "concertos":  [{"id": g(r,"id"), "nome": g(r,"nome"), "local": g(r,"local"), "data": g(r,"data")} for r in rows_of(exec_query(q_concertos))],
        "influencias": [{"id": g(r,"id"), "nome": g(r,"nome")} for r in rows_of(exec_query(q_influencias))],
        "influenciou": [{"id": g(r,"id"), "nome": g(r,"nome")} for r in rows_of(exec_query(q_influenciou))],
    }

    return render_template('detalhe.html', artista=artista)


# ────────────────────────────────────────────────────────────────────
# DETALHE DE ÁLBUM
# ────────────────────────────────────────────────────────────────────
@app.route('/album/<id_album>')
def detalhe_album(id_album):
    query_album = PREFIX + f"""
        SELECT ?nome ?ano ?artistaId ?artistaNome WHERE {{
            :{id_album} a :Album ; :nome ?nome .
            OPTIONAL {{ :{id_album} :anoLancamento ?ano }}
            OPTIONAL {{ ?artista :lancouAlbum :{id_album} ; :nome ?artistaNome .
                        BIND(STRAFTER(STR(?artista), "music-ontology/") AS ?artistaId) }}
        }} LIMIT 1
    """
    res = rows_of(exec_query(query_album))
    if not res:
        return "Álbum não encontrado", 404

    row = res[0]
    q_generos = PREFIX + f"SELECT ?nome WHERE {{ :{id_album} :pertenceAoGenero ?g . BIND(STRAFTER(STR(?g), 'music-ontology/') AS ?nome) }}"
    q_musicas = PREFIX + f"SELECT ?id ?nome WHERE {{ ?m :pertenceAoAlbum :{id_album} ; :nome ?nome . BIND(STRAFTER(STR(?m), 'music-ontology/') AS ?id) }} ORDER BY ?nome"

    artista_dados = None
    if g(row, "artistaId"):
        artista_dados = {"id": g(row, "artistaId"), "nome": g(row, "artistaNome")}

    album = {
        "id":      id_album,
        "nome":    g(row, "nome"),
        "ano":     g(row, "ano"),
        "artista": artista_dados,
        "generos": [{"nome": g(r,"nome")} for r in rows_of(exec_query(q_generos))],
        "musicas": [{"id": g(r,"id"), "nome": g(r,"nome")} for r in rows_of(exec_query(q_musicas))],
    }

    return render_template('album.html', album=album)


# ────────────────────────────────────────────────────────────────────
# GÉNEROS
# ────────────────────────────────────────────────────────────────────
@app.route('/generos')
def generos():
    query_g = PREFIX + """
        SELECT DISTINCT ?gid WHERE {
            ?gid rdfs:subClassOf* :Genero .
            FILTER(?gid != :Genero)
        }
    """
    gen_list = []
    for r in rows_of(exec_query(query_g)):
        gid = r["gid"]["value"].split('/')[-1]
        q_art = PREFIX + f"""
            SELECT DISTINCT ?id ?nome ?tipo WHERE {{
                {{ ?a a :ArtistaSolo . BIND("Solo" AS ?tipo) }}
                UNION {{ ?a a :Banda . BIND("Banda" AS ?tipo) }}
                ?a :pertenceAoGenero :{gid} ; :nome ?nome .
                BIND(STRAFTER(STR(?a), "music-ontology/") AS ?id)
            }} ORDER BY ?nome
        """
        artistas = [{"id": g(ra,"id"), "nome": g(ra,"nome"), "tipo": g(ra,"tipo")}
                    for ra in rows_of(exec_query(q_art))]
        gen_list.append({"id": gid, "nome": gid, "artistas": artistas, "total": len(artistas)})

    gen_list.sort(key=lambda x: -x["total"])
    return render_template('generos.html', generos=gen_list)


# ────────────────────────────────────────────────────────────────────
# TIMELINE
# ────────────────────────────────────────────────────────────────────
@app.route('/timeline')
def timeline():
    query = PREFIX + """
        SELECT DISTINCT ?id ?nome ?tipo ?ano WHERE {
            {
                ?a a :ArtistaSolo ; :nome ?nome ; :anoNascimento ?ano .
                BIND("Nascimento" AS ?tipo)
                BIND(STRAFTER(STR(?a), "music-ontology/") AS ?id)
            }
            UNION {
                ?a a :Banda ; :nome ?nome ; :anoFormacao ?ano .
                BIND("Formação" AS ?tipo)
                BIND(STRAFTER(STR(?a), "music-ontology/") AS ?id)
            }
            UNION {
                ?a a :Album ; :nome ?nome ; :anoLancamento ?ano .
                BIND("Álbum" AS ?tipo)
                BIND(STRAFTER(STR(?a), "music-ontology/") AS ?id)
            }
            UNION {
                ?a a :Premio ; :nome ?nome ; :anoPremio ?ano .
                BIND("Prémio" AS ?tipo)
                BIND(STRAFTER(STR(?a), "music-ontology/") AS ?id)
            }
        } ORDER BY ?ano
    """
    eventos = [
        {"id": g(r,"id"), "nome": g(r,"nome"), "tipo": g(r,"tipo"), "ano": g(r,"ano")}
        for r in rows_of(exec_query(query))
        if g(r,"ano") and g(r,"ano").isdigit()
    ]
    return render_template('timeline.html', eventos=eventos)


# ────────────────────────────────────────────────────────────────────
# ESTATÍSTICAS
# ────────────────────────────────────────────────────────────────────
@app.route('/estatisticas')
def estatisticas():
    # Artistas por género
    q_gen = PREFIX + """
        SELECT ?genero (COUNT(DISTINCT ?a) AS ?total) WHERE {
            { ?a a :ArtistaSolo } UNION { ?a a :Banda }
            ?a :pertenceAoGenero ?g .
            BIND(STRAFTER(STR(?g), "music-ontology/") AS ?genero)
        } GROUP BY ?genero ORDER BY DESC(?total)
    """
    por_genero = [{"genero": g(r,"genero"), "total": int(g(r,"total","0"))}
                  for r in rows_of(exec_query(q_gen))]

    # Artistas por editora
    q_edit = PREFIX + """
        SELECT ?editora (COUNT(DISTINCT ?a) AS ?total) WHERE {
            { ?a a :ArtistaSolo } UNION { ?a a :Banda }
            ?a :pertenceAEditora ?e . ?e :nome ?editora .
        } GROUP BY ?editora ORDER BY DESC(?total)
    """
    por_editora = [{"editora": g(r,"editora"), "total": int(g(r,"total","0"))}
                   for r in rows_of(exec_query(q_edit))]

    # Albuns por década
    q_dec = PREFIX + """
        SELECT (FLOOR(?ano / 10) * 10 AS ?decada) (COUNT(?a) AS ?total) WHERE {
            ?a a :Album ; :anoLancamento ?ano .
        } GROUP BY (FLOOR(?ano / 10) * 10) ORDER BY ?decada
    """
    por_decada = [{"decada": str(int(float(g(r,"decada","0"))))+"s", "total": int(g(r,"total","0"))}
                  for r in rows_of(exec_query(q_dec)) if g(r,"decada")]

    # Top prémios por organização
    q_prem = PREFIX + """
        SELECT ?org (COUNT(?p) AS ?total) WHERE {
            ?p a :Premio ; :organizacao ?org .
        } GROUP BY ?org ORDER BY DESC(?total)
    """
    por_org = [{"org": g(r,"org"), "total": int(g(r,"total","0"))}
               for r in rows_of(exec_query(q_prem))]

    # Artistas mais premiados
    q_top = PREFIX + """
        SELECT ?id ?nome (COUNT(?p) AS ?total) WHERE {
            { ?a a :ArtistaSolo } UNION { ?a a :Banda }
            ?a :nome ?nome ; :recebeupremio ?p .
            BIND(STRAFTER(STR(?a), "music-ontology/") AS ?id)
        } GROUP BY ?id ?nome ORDER BY DESC(?total) LIMIT 10
    """
    mais_premiados = [{"id": g(r,"id"), "nome": g(r,"nome"), "total": int(g(r,"total","0"))}
                      for r in rows_of(exec_query(q_top))]

    return render_template('estatisticas.html',
                           por_genero=por_genero,
                           por_editora=por_editora,
                           por_decada=por_decada,
                           por_org=por_org,
                           mais_premiados=mais_premiados)


# ────────────────────────────────────────────────────────────────────
# COLABORAÇÕES / GRAFO DE INFLUÊNCIAS
# ────────────────────────────────────────────────────────────────────
@app.route('/colaboracoes')
def colaboracoes():
    q_inf = PREFIX + """
        SELECT ?aId ?aNome ?bId ?bNome WHERE {
            ?a :influenciadoPor ?b .
            ?a :nome ?aNome .
            ?b :nome ?bNome .
            BIND(STRAFTER(STR(?a), "music-ontology/") AS ?aId)
            BIND(STRAFTER(STR(?b), "music-ontology/") AS ?bId)
        }
    """
    influencias = [
        {"source": g(r,"bId"), "sourceNome": g(r,"bNome"),
         "target": g(r,"aId"), "targetNome": g(r,"aNome")}
        for r in rows_of(exec_query(q_inf))
    ]

    q_feat = PREFIX + """
        SELECT ?mId ?mNome ?aId ?aNome ?bId ?bNome WHERE {
            ?m a :Musica ; :nome ?mNome ; :interpretadaPor ?a ; :temColaboracao ?b .
            ?a :nome ?aNome .
            ?b :nome ?bNome .
            BIND(STRAFTER(STR(?m), "music-ontology/") AS ?mId)
            BIND(STRAFTER(STR(?a), "music-ontology/") AS ?aId)
            BIND(STRAFTER(STR(?b), "music-ontology/") AS ?bId)
        }
    """
    feats = [
        {"musica": g(r,"mNome"),
         "artista": g(r,"aNome"), "artistaId": g(r,"aId"),
         "feat": g(r,"bNome"), "featId": g(r,"bId")}
        for r in rows_of(exec_query(q_feat))
    ]

    return render_template('colaboracoes.html', influencias=influencias, feats=feats)


# ────────────────────────────────────────────────────────────────────
# PRÉMIOS
# ────────────────────────────────────────────────────────────────────
@app.route('/premios')
def premios():
    q = PREFIX + """
        SELECT ?pId ?pNome ?cat ?org ?ano ?aId ?aNome WHERE {
            ?p a :Premio ; :nome ?pNome .
            OPTIONAL { ?p :categoria ?cat }
            OPTIONAL { ?p :organizacao ?org }
            OPTIONAL { ?p :anoPremio ?ano }
            OPTIONAL { ?a :recebeupremio ?p ; :nome ?aNome .
                       BIND(STRAFTER(STR(?a), "music-ontology/") AS ?aId) }
            BIND(STRAFTER(STR(?p), "music-ontology/") AS ?pId)
        } ORDER BY DESC(?ano) ?org
    """
    lista = [
        {"id": g(r,"pId"), "nome": g(r,"pNome"), "cat": g(r,"cat"),
         "org": g(r,"org"), "ano": g(r,"ano"),
         "artistaId": g(r,"aId"), "artistaNome": g(r,"aNome")}
        for r in rows_of(exec_query(q))
    ]
    return render_template('premios.html', premios=lista)


# ────────────────────────────────────────────────────────────────────
# CONCERTOS
# ────────────────────────────────────────────────────────────────────
@app.route('/concertos')
def concertos():
    q = PREFIX + """
        SELECT ?cId ?cNome ?local ?data WHERE {
            ?c a :Concerto ; :nome ?cNome .
            OPTIONAL { ?c :local ?local }
            OPTIONAL { ?c :data ?data }
            BIND(STRAFTER(STR(?c), "music-ontology/") AS ?cId)
        } ORDER BY DESC(?data)
    """
    concertos_list = []
    for r in rows_of(exec_query(q)):
        cid = g(r, "cId")
        q_art = PREFIX + f"""
            SELECT ?id ?nome WHERE {{
                ?a :atuouEm :{cid} ; :nome ?nome .
                BIND(STRAFTER(STR(?a), "music-ontology/") AS ?id)
            }}
        """
        artistas = [{"id": g(ra,"id"), "nome": g(ra,"nome")} for ra in rows_of(exec_query(q_art))]
        concertos_list.append({
            "id": cid, "nome": g(r,"cNome"),
            "local": g(r,"local"), "data": g(r,"data"),
            "artistas": artistas
        })
    return render_template('concertos.html', concertos=concertos_list)


# ────────────────────────────────────────────────────────────────────
# PESQUISA GLOBAL
# ────────────────────────────────────────────────────────────────────
@app.route('/pesquisa')
def pesquisa():
    q = request.args.get('q', '').strip()
    genero = request.args.get('genero', '').strip()
    ano_de = request.args.get('ano_de', '').strip()
    ano_ate = request.args.get('ano_ate', '').strip()
    editora = request.args.get('editora', '').strip()

    filtros_art = []
    if genero:
        filtros_art.append(f'?e :pertenceAoGenero :{genero} .')
    if editora:
        filtros_art.append(f'?e :pertenceAEditora :{editora} .')

    resultados = []
    if q or genero or editora or ano_de or ano_ate:
        filtro_nome = f'FILTER(CONTAINS(LCASE(?nome), LCASE("{q}")))' if q else ''
        query = PREFIX + f"""
            SELECT DISTINCT ?id ?nome ?tipo WHERE {{
                {{
                    {{ ?e a :ArtistaSolo . BIND("Artista" AS ?tipo) }}
                    UNION {{ ?e a :Banda . BIND("Banda" AS ?tipo) }}
                    ?e :nome ?nome .
                    {filtro_nome}
                    {''.join(filtros_art)}
                    BIND(CONCAT("/artista/", STRAFTER(STR(?e), "music-ontology/")) AS ?id)
                }}
                UNION {{
                    ?e a :Album ; :nome ?nome .
                    {filtro_nome}
                    BIND("Álbum" AS ?tipo)
                    BIND(CONCAT("/album/", STRAFTER(STR(?e), "music-ontology/")) AS ?id)
                }}
                UNION {{
                    ?e a :Musica ; :nome ?nome .
                    {filtro_nome}
                    BIND("Música" AS ?tipo)
                    BIND("" AS ?id)
                }}
            }} ORDER BY ?tipo ?nome LIMIT 80
        """
        resultados = [
            {"id": g(r,"id"), "nome": g(r,"nome"), "tipo": g(r,"tipo")}
            for r in rows_of(exec_query(query))
        ]

    return render_template('pesquisa.html',
                           resultados=resultados, busca=q,
                           generos=generos_list(),
                           editoras=editoras_list(),
                           filtro_genero=genero,
                           filtro_editora=editora,
                           ano_de=ano_de, ano_ate=ano_ate)


# ────────────────────────────────────────────────────────────────────
# API JSON para gráficos (usado por estatisticas.html via fetch)
# ────────────────────────────────────────────────────────────────────
@app.route('/api/stats/generos')
def api_stats_generos():
    q = PREFIX + """
        SELECT ?genero (COUNT(DISTINCT ?a) AS ?total) WHERE {
            { ?a a :ArtistaSolo } UNION { ?a a :Banda }
            ?a :pertenceAoGenero ?g .
            BIND(STRAFTER(STR(?g), "music-ontology/") AS ?genero)
        } GROUP BY ?genero ORDER BY DESC(?total)
    """
    return jsonify([{"genero": g(r,"genero"), "total": int(g(r,"total","0"))}
                    for r in rows_of(exec_query(q))])

@app.route('/api/stats/decadas')
def api_stats_decadas():
    q = PREFIX + """
        SELECT (FLOOR(?ano / 10) * 10 AS ?decada) (COUNT(?a) AS ?total) WHERE {
            ?a a :Album ; :anoLancamento ?ano .
        } GROUP BY (FLOOR(?ano / 10) * 10) ORDER BY ?decada
    """
    return jsonify([{"decada": str(int(float(g(r,"decada","0"))))+"s", "total": int(g(r,"total","0"))}
                    for r in rows_of(exec_query(q)) if g(r,"decada")])


# ────────────────────────────────────────────────────────────────────
# ADICIONAR ARTISTA (POST)
# ────────────────────────────────────────────────────────────────────
@app.route('/artista/adicionar', methods=['POST'])
def adicionar_artista():
    nome      = request.form.get('nome', '').strip()
    tipo      = request.form.get('tipo', 'ArtistaSolo')
    ano       = request.form.get('ano', '').strip()
    genero_id = request.form.get('genero', '').strip()
    editora   = request.form.get('editora', '').strip()

    if not nome:
        return redirect(url_for('index'))

    new_id   = re.sub(r'[^\w]', '_', nome).strip('_')
    prop_ano = ":anoNascimento" if tipo == 'ArtistaSolo' else ":anoFormacao"

    triplos = [
        f':{new_id} a :{tipo} .',
        f':{new_id} :nome "{nome}"^^xsd:string .',
    ]
    if ano and ano.isdigit():
        triplos.append(f':{new_id} {prop_ano} "{int(ano)}"^^xsd:integer .')
    if genero_id:
        triplos.append(f':{new_id} :pertenceAoGenero :{genero_id} .')
    if editora:
        triplos.append(f':{new_id} :pertenceAEditora :{editora} .')

    exec_update(PREFIX + "INSERT DATA {\n  " + "\n  ".join(triplos) + "\n}")
    return redirect(url_for('detalhe_artista', id_artista=new_id))


# ────────────────────────────────────────────────────────────────────
# ADICIONAR ÁLBUM (POST)
# ────────────────────────────────────────────────────────────────────
@app.route('/album/adicionar', methods=['POST'])
def adicionar_album():
    nome       = request.form.get('nome', '').strip()
    ano        = request.form.get('ano', '').strip()
    artista_id = request.form.get('artista_id', '').strip()
    genero_id  = request.form.get('genero', '').strip()

    if not nome or not artista_id:
        return redirect(url_for('detalhe_artista', id_artista=artista_id or ''))

    new_id = re.sub(r'[^\w]', '_', nome).strip('_') + '_alb'
    triplos = [
        f':{new_id} a :Album .',
        f':{new_id} :nome "{nome}"^^xsd:string .',
    ]
    if ano and ano.isdigit():
        triplos.append(f':{new_id} :anoLancamento "{int(ano)}"^^xsd:integer .')
    if genero_id:
        triplos.append(f':{new_id} :pertenceAoGenero :{genero_id} .')
    triplos.append(f':{artista_id} :lancouAlbum :{new_id} .')

    exec_update(PREFIX + "INSERT DATA {\n  " + "\n  ".join(triplos) + "\n}")
    return redirect(url_for('detalhe_album', id_album=new_id))


if __name__ == '__main__':
    app.run(debug=True, port=5000)