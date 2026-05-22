"""
gerar_dados.py — Geração completa dos datasets expandidos
Produz todos os JSONs: editoras, artistas, bandas, albuns, musicas,
premios, concertos, tours, colaboracoes.
"""
import json, os

OUT = 'datasets'
os.makedirs(OUT, exist_ok=True)

def gravar(nome, dados):
    with open(os.path.join(OUT, nome), 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {nome}")

# ══════════════════════════════════════════════════════════════════════
# EDITORAS
# ══════════════════════════════════════════════════════════════════════
editoras = [
    {"id": "valentim_de_carvalho", "nome": "Valentim de Carvalho"},
    {"id": "edisco",               "nome": "Edisco"},
    {"id": "emi_portugal",         "nome": "EMI Portugal"},
    {"id": "universal_pt",         "nome": "Universal Music Portugal"},
    {"id": "sony_pt",              "nome": "Sony Music Portugal"},
    {"id": "transformadores",      "nome": "Transformadores Discos"},
    {"id": "edicoes_orfeu",        "nome": "Edições Orfeu"},
    {"id": "ovacao",               "nome": "Ovação Records"},
    {"id": "polygram",             "nome": "PolyGram Portugal"},
    {"id": "zona_musica",          "nome": "Zona Música"},
]

# ══════════════════════════════════════════════════════════════════════
# ARTISTAS SOLO (expandido)
# ══════════════════════════════════════════════════════════════════════
artistas_solo = [
    # ── FADO ──────────────────────────────────────────────────────────
    {"id":"amalia_rodrigues",   "nome":"Amália Rodrigues",        "anoNascimento":1920, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho",
     "descricao":"A voz mais emblemática do fado português, conhecida mundialmente como a Rainha do Fado.", "curiosidade":"Representou Portugal no Festival de Cinema de Cannes em 1955."},
    {"id":"carlos_do_carmo",    "nome":"Carlos do Carmo",         "anoNascimento":1939, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho",
     "descricao":"Um dos maiores nomes do fado moderno, filho da fadista Lucília do Carmo."},
    {"id":"fernando_mauricio",  "nome":"Fernando Maurício",       "anoNascimento":1933, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"alfredo_marceneiro", "nome":"Alfredo Marceneiro",      "anoNascimento":1891, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"lucilia_do_carmo",   "nome":"Lucília do Carmo",        "anoNascimento":1903, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"luiz_goes",          "nome":"Luiz Goes",               "anoNascimento":1933, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"mariza",             "nome":"Mariza",                  "anoNascimento":1973, "generos":["Fado"],           "pertenceAEditora":"universal_pt",
     "descricao":"Fadista nascida em Moçambique que se tornou uma das maiores embaixadoras do fado no mundo.", "curiosidade":"Já actuou em mais de 60 países."},
    {"id":"camane",             "nome":"Camané",                  "anoNascimento":1967, "generos":["Fado"],           "pertenceAEditora":"universal_pt"},
    {"id":"ana_moura",          "nome":"Ana Moura",               "anoNascimento":1979, "generos":["Fado"],           "pertenceAEditora":"universal_pt",
     "descricao":"Fadista que colaborou com os Rolling Stones e Prince, levando o fado a novas audiências."},
    {"id":"carminho",           "nome":"Carminho",                "anoNascimento":1984, "generos":["Fado"],           "pertenceAEditora":"emi_portugal"},
    {"id":"gisela_joao",        "nome":"Gisela João",             "anoNascimento":1983, "generos":["Fado"],           "pertenceAEditora":"transformadores",
     "curiosidade":"Estudou teatro antes de se dedicar ao fado."},
    {"id":"ricardo_ribeiro",    "nome":"Ricardo Ribeiro",         "anoNascimento":1981, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"antonio_zambujo",    "nome":"António Zambujo",         "anoNascimento":1975, "generos":["Fado","Pop"],     "pertenceAEditora":"universal_pt",
     "descricao":"Alentejano que mistura fado com cante alentejano e música brasileira."},
    {"id":"katia_guerreiro",    "nome":"Kátia Guerreiro",         "anoNascimento":1974, "generos":["Fado"],           "pertenceAEditora":"emi_portugal"},
    {"id":"mafalda_arnauth",    "nome":"Mafalda Arnauth",         "anoNascimento":1974, "generos":["Fado"],           "pertenceAEditora":"emi_portugal"},
    {"id":"miguel_povoas",      "nome":"Miguel Póvoas",           "anoNascimento":1978, "generos":["Fado"],           "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"raul_nery",          "nome":"Raúl Nery",               "anoNascimento":1932, "generos":["Fado","Tradicional"],"pertenceAEditora":"valentim_de_carvalho",
     "descricao":"Guitarrista português que acompanhou Amália Rodrigues durante décadas."},

    # ── ROCK / POP CLÁSSICO ────────────────────────────────────────────
    {"id":"antonio_variacoes",  "nome":"António Variações",       "anoNascimento":1944, "generos":["Pop","Rock"],     "pertenceAEditora":"valentim_de_carvalho",
     "descricao":"Barbeiro de profissão que se tornou um dos maiores ícones do pop-rock português.", "curiosidade":"Faleceu em 1983 com apenas 39 anos."},
    {"id":"jorge_palma",        "nome":"Jorge Palma",             "anoNascimento":1950, "generos":["Rock","Pop"],     "pertenceAEditora":"emi_portugal",
     "descricao":"Cantor, compositor e pianista, um dos pilares do rock português."},
    {"id":"manel_cruz",         "nome":"Manel Cruz",              "anoNascimento":1975, "generos":["Rock","Indie"],   "pertenceAEditora":"transformadores"},
    {"id":"lena_d_agua",        "nome":"Lena d'Água",             "anoNascimento":1956, "generos":["Pop","Rock"],     "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"paulo_de_carvalho",  "nome":"Paulo de Carvalho",       "anoNascimento":1947, "generos":["Pop","Fado"],     "pertenceAEditora":"emi_portugal",
     "curiosidade":"Representou Portugal na Eurovisão 1974 com 'E Depois do Adeus', canção que foi sinal para o 25 de Abril."},
    {"id":"carlos_paiao",       "nome":"Carlos Paião",            "anoNascimento":1957, "generos":["Pop"],            "pertenceAEditora":"valentim_de_carvalho",
     "curiosidade":"Faleceu tragicamente num acidente de viação em 1988."},
    {"id":"rui_veloso",         "nome":"Rui Veloso",              "anoNascimento":1956, "generos":["Rock","Blues"],   "pertenceAEditora":"valentim_de_carvalho",
     "descricao":"O padrinho do rock em português, autor de Porto Sentido."},
    {"id":"xana_toc_toc",       "nome":"Xana",                    "anoNascimento":1963, "generos":["Pop"],            "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"fernando_ribeiro",   "nome":"Fernando Ribeiro",        "anoNascimento":1974, "generos":["Rock","Metal"],
     "descricao":"Vocalista dos Moonspell, a banda de metal mais importante de Portugal."},
    {"id":"tomas_wallenstein",  "nome":"Tomás Wallenstein",       "anoNascimento":1989, "generos":["Pop","Indie"]},
    {"id":"rodrigo_leao",       "nome":"Rodrigo Leão",            "anoNascimento":1964, "generos":["Pop","Indie"],    "pertenceAEditora":"sony_pt",
     "descricao":"Músico e compositor, ex-membro da Sétima Legião e dos Madredeus."},
    {"id":"pedro_ayres_magalhaes","nome":"Pedro Ayres Magalhães", "anoNascimento":1956, "generos":["Pop","Rock"],     "pertenceAEditora":"valentim_de_carvalho"},
    {"id":"teresa_salgueiro",   "nome":"Teresa Salgueiro",        "anoNascimento":1969, "generos":["Indie","Folk"],   "pertenceAEditora":"universal_pt",
     "descricao":"Voz original dos Madredeus, conhecida pela sua voz inconfundível."},
    {"id":"pedro_abrunhosa",    "nome":"Pedro Abrunhosa",         "anoNascimento":1960, "generos":["Pop","Jazz"],     "pertenceAEditora":"sony_pt",
     "descricao":"Cantor e compositor portuense com forte influência do jazz."},

    # ── POP CONTEMPORÂNEO ──────────────────────────────────────────────
    {"id":"barbara_bandeira",   "nome":"Bárbara Bandeira",        "anoNascimento":2001, "generos":["Pop"],            "pertenceAEditora":"universal_pt",
     "descricao":"A artista portuguesa mais ouvida em streaming da sua geração."},
    {"id":"salvador_sobral",    "nome":"Salvador Sobral",         "anoNascimento":1989, "generos":["Pop","Jazz"],     "pertenceAEditora":"valentim_de_carvalho",
     "descricao":"Vencedor do Festival Eurovisão 2017 com 'Amar Pelos Dois'.", "curiosidade":"Sobreviveu a um transplante cardíaco em 2017."},
    {"id":"luisa_sobral",       "nome":"Luísa Sobral",            "anoNascimento":1987, "generos":["Pop","Jazz"],     "pertenceAEditora":"valentim_de_carvalho",
     "descricao":"Compositora e cantora, irmã de Salvador Sobral, autora de 'Amar Pelos Dois'."},
    {"id":"mariza_liz",         "nome":"Marisa Liz",              "anoNascimento":1982, "generos":["Pop","Rock"],     "pertenceAEditora":"sony_pt"},
    {"id":"rita_redshoes",      "nome":"Rita Redshoes",           "anoNascimento":1981, "generos":["Pop","Indie"],    "pertenceAEditora":"transformadores"},
    {"id":"carolina_deslandes", "nome":"Carolina Deslandes",      "anoNascimento":1991, "generos":["Pop"],            "pertenceAEditora":"universal_pt"},
    {"id":"barbara_tinoco",     "nome":"Bárbara Tinoco",          "anoNascimento":1998, "generos":["Pop"],            "pertenceAEditora":"universal_pt"},
    {"id":"buba_espinho",       "nome":"Buba Espinho",            "anoNascimento":1995, "generos":["Pop","Soul"],     "pertenceAEditora":"universal_pt"},
    {"id":"ivandro",            "nome":"Ivandro",                 "anoNascimento":1998, "generos":["Pop","RB"],       "pertenceAEditora":"universal_pt"},
    {"id":"dino_d_santiago",    "nome":"Dino D'Santiago",         "anoNascimento":1982, "generos":["Pop","RB","Kizomba"],"pertenceAEditora":"sony_pt",
     "descricao":"Músico cabo-verdiano radicado em Portugal, mistura kizomba, soul e pop."},
    {"id":"ana_bacalhau",       "nome":"Ana Bacalhau",            "anoNascimento":1978, "generos":["Pop"],
     "descricao":"Vocalista dos Deolinda, conhecida pela voz característica e letras poéticas."},
    {"id":"david_fonseca",      "nome":"David Fonseca",           "anoNascimento":1976, "generos":["Pop","Indie"],    "pertenceAEditora":"universal_pt"},
    {"id":"m_fontes",           "nome":"M. Fontes",               "anoNascimento":1987, "generos":["Pop"],            "pertenceAEditora":"sony_pt"},
    {"id":"ana_free",           "nome":"Ana Free",                "anoNascimento":1987, "generos":["Pop","Soul"],     "pertenceAEditora":"universal_pt"},
    {"id":"sara_tavares",       "nome":"Sara Tavares",            "anoNascimento":1978, "generos":["Pop","RB","Soul"],"pertenceAEditora":"universal_pt",
     "descricao":"Cantora e guitarrista com forte influência africana e soul."},
    {"id":"seu_jorge_pt",       "nome":"Zé Manel Focinho",        "anoNascimento":1972, "generos":["Pop","Soul"],     "pertenceAEditora":"universal_pt"},
    {"id":"diogo_piçarra",      "nome":"Diogo Piçarra",           "anoNascimento":1994, "generos":["Pop"],            "pertenceAEditora":"universal_pt",
     "descricao":"Artista pop do Algarve com grande popularidade nas redes sociais."},
    {"id":"carlao",             "nome":"Carlão",                  "anoNascimento":1980, "generos":["Pop","Soul"],     "pertenceAEditora":"sony_pt"},

    # ── HIP-HOP ────────────────────────────────────────────────────────
    {"id":"slow_j",             "nome":"Slow J",                  "anoNascimento":1992, "generos":["HipHop","Pop"],   "pertenceAEditora":"sony_pt",
     "descricao":"João Coelho, produtor e rapper que mistura hip-hop com fado e música africana."},
    {"id":"valete",             "nome":"Valete",                  "anoNascimento":1981, "generos":["HipHop"],         "pertenceAEditora":"edisco",
     "descricao":"Um dos rappers mais letrados do hip-hop português, com letras de intervenção social."},
    {"id":"profjam",            "nome":"ProfJam",                 "anoNascimento":1991, "generos":["HipHop"],         "pertenceAEditora":"sony_pt"},
    {"id":"bispo",              "nome":"Bispo",                   "anoNascimento":1992, "generos":["HipHop"],         "pertenceAEditora":"sony_pt"},
    {"id":"t_rex_pt",           "nome":"T-Rex",                   "anoNascimento":1997, "generos":["HipHop","RB"],    "pertenceAEditora":"universal_pt"},
    {"id":"plutonio",           "nome":"Plutónio",                "anoNascimento":1985, "generos":["HipHop","RB"],    "pertenceAEditora":"sony_pt"},
    {"id":"chullage",           "nome":"Chullage",                "anoNascimento":1977, "generos":["HipHop"],         "pertenceAEditora":"edisco",
     "descricao":"Pioneiro do hip-hop de intervenção política em Portugal."},
    {"id":"capicua",            "nome":"Capicua",                 "anoNascimento":1982, "generos":["HipHop"],         "pertenceAEditora":"universal_pt",
     "descricao":"Uma das rappers mais aclamadas do hip-hop português, com letras feministas e poéticas."},
    {"id":"dj_ride",            "nome":"DJ Ride",                 "anoNascimento":1976, "generos":["HipHop","Electronica"],"pertenceAEditora":"edisco"},
    {"id":"boss_ac",            "nome":"Boss AC",                 "anoNascimento":1975, "generos":["HipHop"],         "pertenceAEditora":"edisco",
     "descricao":"Um dos pioneiros do hip-hop português, ativo desde os anos 90."},
    {"id":"dealema",            "nome":"Dealema",                 "anoNascimento":1987, "generos":["HipHop"],         "pertenceAEditora":"sony_pt"},
    {"id":"dillaz",             "nome":"Dillaz",                  "anoNascimento":1988, "generos":["HipHop"],         "pertenceAEditora":"universal_pt"},
    {"id":"agir",               "nome":"Agir",                    "anoNascimento":1990, "generos":["Pop","RB"],       "pertenceAEditora":"universal_pt",
     "descricao":"Cantor de reggaeton e pop que dominou os tops portugueses no início dos anos 2010."},

    # ── INTERVENÇÃO ────────────────────────────────────────────────────
    {"id":"zeca_afonso",        "nome":"Zeca Afonso",             "anoNascimento":1929, "generos":["Intervencao","Folk"],"pertenceAEditora":"edicoes_orfeu",
     "descricao":"O mais importante cantor de intervenção português, autor de Grândola Vila Morena.", "curiosidade":"Grândola Vila Morena foi o sinal da Revolução dos Cravos a 25 de Abril de 1974."},
    {"id":"adriano_correia",    "nome":"Adriano Correia de Oliveira","anoNascimento":1942,"generos":["Intervencao"],"pertenceAEditora":"edicoes_orfeu"},
    {"id":"vitorino",           "nome":"Vitorino Salomé",          "anoNascimento":1942, "generos":["Intervencao","Folk"],"pertenceAEditora":"edicoes_orfeu"},
    {"id":"janita_salome",      "nome":"Janita Salomé",            "anoNascimento":1947, "generos":["Intervencao"],   "pertenceAEditora":"edicoes_orfeu"},
    {"id":"luisa_basto",        "nome":"Luísa Basto",              "anoNascimento":1947, "generos":["Intervencao"],   "pertenceAEditora":"edicoes_orfeu"},
    {"id":"sergio_godinho",     "nome":"Sérgio Godinho",           "anoNascimento":1945, "generos":["Intervencao","Pop"],"pertenceAEditora":"edicoes_orfeu",
     "descricao":"Poeta e cantor, um dos mais importantes da geração de Abril."},
    {"id":"fausto",             "nome":"Fausto",                   "anoNascimento":1948, "generos":["Intervencao","Folk"],"pertenceAEditora":"edicoes_orfeu"},
    {"id":"jose_mario_branco",  "nome":"José Mário Branco",        "anoNascimento":1942, "generos":["Intervencao"],   "pertenceAEditora":"edicoes_orfeu",
     "descricao":"Compositor, produtor e cantor, uma das figuras centrais da música de intervenção."},

    # ── PIMBA ──────────────────────────────────────────────────────────
    {"id":"quim_barreiros",     "nome":"Quim Barreiros",           "anoNascimento":1951, "generos":["Pimba"],         "pertenceAEditora":"ovacao",
     "descricao":"O rei do pimba, famoso pelas letras picantes e pela Garagem da Vizinha."},
    {"id":"toy",                "nome":"Toy",                      "anoNascimento":1963, "generos":["Pimba"],         "pertenceAEditora":"ovacao"},
    {"id":"agata",              "nome":"Ágata",                    "anoNascimento":1959, "generos":["Pimba"],         "pertenceAEditora":"ovacao"},
    {"id":"marante",            "nome":"Marante",                  "anoNascimento":1956, "generos":["Pimba"],         "pertenceAEditora":"ovacao"},
    {"id":"ruth_marlene",       "nome":"Ruth Marlene",             "anoNascimento":1978, "generos":["Pimba"],         "pertenceAEditora":"ovacao"},
    {"id":"zeca_medeiros",      "nome":"Zeca Medeiros",            "anoNascimento":1948, "generos":["Pimba"],         "pertenceAEditora":"ovacao"},
]

# ══════════════════════════════════════════════════════════════════════
# BANDAS (expandido)
# ══════════════════════════════════════════════════════════════════════
bandas = [
    {"id":"quarteto_1111",      "nome":"Quarteto 1111",         "anoFormacao":1967, "generos":["Rock","Pop"],        "pertenceAEditora":"valentim_de_carvalho", "temMembro":[]},
    {"id":"sheiks",             "nome":"Os Sheiks",             "anoFormacao":1963, "generos":["Pop","Rock"],        "pertenceAEditora":"valentim_de_carvalho", "temMembro":["paulo_de_carvalho"]},
    {"id":"taxi",               "nome":"Táxi",                  "anoFormacao":1979, "generos":["Rock"],              "pertenceAEditora":"universal_pt",         "temMembro":[]},
    {"id":"uhf",                "nome":"UHF",                   "anoFormacao":1978, "generos":["Rock"],              "pertenceAEditora":"edisco",               "temMembro":[]},
    {"id":"radio_macau",        "nome":"Rádio Macau",           "anoFormacao":1983, "generos":["Pop","Rock"],        "pertenceAEditora":"emi_portugal",         "temMembro":[]},
    {"id":"setima_legiao",      "nome":"Sétima Legião",         "anoFormacao":1982, "generos":["Pop","Rock"],        "pertenceAEditora":"valentim_de_carvalho", "temMembro":["rodrigo_leao","pedro_ayres_magalhaes"],
     "descricao":"Banda emblemática do rock português dos anos 80."},
    {"id":"xutos_pontapes",     "nome":"Xutos & Pontapés",      "anoFormacao":1978, "generos":["Rock"],              "pertenceAEditora":"universal_pt",         "temMembro":[],
     "descricao":"A mais longeva banda de rock português, activa desde 1978.", "curiosidade":"O vocalista Tim faleceu em 2019 após décadas de actividade."},
    {"id":"rui_veloso_banda",   "nome":"Rui Veloso e Banda",    "anoFormacao":1980, "generos":["Rock","Blues"],      "pertenceAEditora":"valentim_de_carvalho", "temMembro":["rui_veloso"]},
    {"id":"herois_do_mar",      "nome":"Heróis do Mar",         "anoFormacao":1981, "generos":["Pop","Rock"],        "pertenceAEditora":"valentim_de_carvalho", "temMembro":[]},
    {"id":"ex_votos",           "nome":"Os Ex-Votos",           "anoFormacao":1989, "generos":["Rock","Indie"],      "pertenceAEditora":"transformadores",      "temMembro":[]},
    {"id":"mao_morta",          "nome":"Mão Morta",             "anoFormacao":1984, "generos":["Rock","Indie"],      "pertenceAEditora":"transformadores",      "temMembro":[]},
    {"id":"quinta_do_bill",     "nome":"Quinta do Bill",        "anoFormacao":1987, "generos":["Rock"],              "pertenceAEditora":"universal_pt",         "temMembro":[]},
    {"id":"peste_sida",         "nome":"Peste & Sida",          "anoFormacao":1986, "generos":["Rock","Indie"],      "pertenceAEditora":"transformadores",      "temMembro":[]},
    {"id":"trabalhadores_mar",  "nome":"Trabalhadores do Mar",  "anoFormacao":1987, "generos":["Pop","Rock"],        "pertenceAEditora":"polygram",             "temMembro":[]},
    {"id":"cla",                "nome":"Clã",                   "anoFormacao":1996, "generos":["Rock","Indie"],      "pertenceAEditora":"universal_pt",         "temMembro":[]},
    {"id":"ornatos_violeta",    "nome":"Ornatos Violeta",       "anoFormacao":1991, "generos":["Rock","Indie"],      "pertenceAEditora":"universal_pt",         "temMembro":["manel_cruz"],
     "descricao":"Banda de rock alternativo do Porto, considerada um dos maiores projetos do rock português.", "curiosidade":"Terminaram a carreira em 2002 no auge da popularidade."},
    {"id":"linda_martini",      "nome":"Linda Martini",         "anoFormacao":2003, "generos":["Rock","Indie"],      "pertenceAEditora":"universal_pt",         "temMembro":[]},
    {"id":"moonspell",          "nome":"Moonspell",             "anoFormacao":1992, "generos":["Rock","Metal"],      "pertenceAEditora":"universal_pt",         "temMembro":["fernando_ribeiro"],
     "descricao":"A banda de metal português com maior projeção internacional.", "curiosidade":"Foram o primeiro grupo de metal a tocar no Rock in Rio Lisboa."},
    {"id":"capitao_fausto",     "nome":"Capitão Fausto",        "anoFormacao":2009, "generos":["Rock","Indie"],      "pertenceAEditora":"sony_pt",              "temMembro":["tomas_wallenstein"],
     "descricao":"Banda de rock indie de Lisboa com forte influência da cena independente."},
    {"id":"kussondulola",       "nome":"Kussondulola",          "anoFormacao":1992, "generos":["Pop","Reggae"],      "pertenceAEditora":"emi_portugal",         "temMembro":[]},
    {"id":"corvos",             "nome":"Corvos",                "anoFormacao":1998, "generos":["Rock","Metal"],      "pertenceAEditora":"zona_musica",          "temMembro":[]},
    {"id":"the_gift",           "nome":"The Gift",              "anoFormacao":1994, "generos":["Pop","Indie"],       "pertenceAEditora":"transformadores",      "temMembro":[],
     "descricao":"Banda de pop alternativo de Coimbra, uma das mais internacionais do pop português."},
    {"id":"deolinda",           "nome":"Deolinda",              "anoFormacao":2006, "generos":["Pop","Fado","Folk"], "pertenceAEditora":"sony_pt",              "temMembro":["ana_bacalhau"],
     "descricao":"Quarteto de Lisboa que mistura fado, folk e pop com letras sociais e poéticas."},
    {"id":"amor_electro",       "nome":"Amor Electro",          "anoFormacao":2010, "generos":["Pop","Rock"],        "pertenceAEditora":"sony_pt",              "temMembro":["mariza_liz"]},
    {"id":"os_quatro_e_meia",   "nome":"Os Quatro e Meia",      "anoFormacao":2013, "generos":["Pop"],               "pertenceAEditora":"universal_pt",         "temMembro":[]},
    {"id":"dzrt",               "nome":"D'ZRT",                 "anoFormacao":2004, "generos":["Pop"],               "pertenceAEditora":"universal_pt",         "temMembro":[]},
    {"id":"santamaria",         "nome":"Santamaria",            "anoFormacao":1998, "generos":["Pop"],               "pertenceAEditora":"ovacao",               "temMembro":[]},
    {"id":"davidinho_e_banda",  "nome":"David Fonseca e Banda", "anoFormacao":2000, "generos":["Pop","Rock"],        "pertenceAEditora":"universal_pt",         "temMembro":["david_fonseca"]},
    {"id":"wet_bed_gang",       "nome":"Wet Bed Gang",          "anoFormacao":2014, "generos":["HipHop"],            "pertenceAEditora":"sony_pt",              "temMembro":[]},
    {"id":"buraka_som_sistema", "nome":"Buraka Som Sistema",    "anoFormacao":2006, "generos":["HipHop","Electronica"],"pertenceAEditora":"sony_pt",            "temMembro":[],
     "descricao":"Coletivo musical de Lisboa que popularizou o kuduro e a música eletrónica africana."},
    {"id":"expensive_soul",     "nome":"Expensive Soul",        "anoFormacao":1999, "generos":["HipHop","RB"],       "pertenceAEditora":"sony_pt",              "temMembro":[]},
    {"id":"black_company",      "nome":"Black Company",         "anoFormacao":1993, "generos":["HipHop"],            "pertenceAEditora":"edisco",               "temMembro":[]},
    {"id":"dealema_banda",      "nome":"Dealema",               "anoFormacao":1999, "generos":["HipHop"],            "pertenceAEditora":"sony_pt",              "temMembro":["dealema"]},
    {"id":"madredeus",          "nome":"Madredeus",             "anoFormacao":1986, "generos":["Folk","Indie","Pop"], "pertenceAEditora":"universal_pt",         "temMembro":["teresa_salgueiro","rodrigo_leao"],
     "descricao":"Grupo musical português que mistura fado, música medieval e pop, reconhecido internacionalmente.", "curiosidade":"Apareceram no filme 'Lisboa Story' de Wim Wenders em 1994."},
    {"id":"pedro_abrunhosa_banda","nome":"Pedro Abrunhosa e Comité Caviar","anoFormacao":1993,"generos":["Pop","Jazz","Soul"],"pertenceAEditora":"sony_pt","temMembro":["pedro_abrunhosa"],
     "descricao":"Projeto musical do compositor portuense Pedro Abrunhosa."},
    {"id":"tao_cruz_band",      "nome":"Silence 4",             "anoFormacao":1994, "generos":["Rock","Indie"],      "pertenceAEditora":"sony_pt",              "temMembro":["david_fonseca"],
     "descricao":"Banda de rock alternativo portuense precursora do indie rock português."},
]

# ══════════════════════════════════════════════════════════════════════
# ÁLBUNS (expandido)
# ══════════════════════════════════════════════════════════════════════
albuns = [
    # FADO
    {"id":"estranha_forma_vida",   "nome":"Estranha Forma de Vida",      "anoLancamento":1962, "lancadoPor":"amalia_rodrigues", "generos":["Fado"]},
    {"id":"com_que_voz",           "nome":"Com Que Voz",                  "anoLancamento":1970, "lancadoPor":"amalia_rodrigues", "generos":["Fado"]},
    {"id":"amalia_71",             "nome":"Amália 71",                    "anoLancamento":1971, "lancadoPor":"amalia_rodrigues", "generos":["Fado"]},
    {"id":"fado_em_mim",           "nome":"O Fado",                       "anoLancamento":2001, "lancadoPor":"carlos_do_carmo",  "generos":["Fado"]},
    {"id":"fado_mae",              "nome":"Fado Mãe",                     "anoLancamento":2008, "lancadoPor":"carminho",         "generos":["Fado"]},
    {"id":"mariza_fado_em_mim",    "nome":"Fado em Mim",                  "anoLancamento":2001, "lancadoPor":"mariza",           "generos":["Fado"]},
    {"id":"transparente_alb",      "nome":"Transparente",                 "anoLancamento":2005, "lancadoPor":"mariza",           "generos":["Fado"]},
    {"id":"ana_moura_desfado",     "nome":"Desfado",                      "anoLancamento":2012, "lancadoPor":"ana_moura",        "generos":["Fado"]},
    {"id":"katia_longe",           "nome":"Longe",                        "anoLancamento":2003, "lancadoPor":"katia_guerreiro",  "generos":["Fado"]},
    {"id":"gisela_gisela",         "nome":"Gisela João",                  "anoLancamento":2013, "lancadoPor":"gisela_joao",      "generos":["Fado"]},
    {"id":"zambujo_alfama",        "nome":"Alfama",                       "anoLancamento":2011, "lancadoPor":"antonio_zambujo",  "generos":["Fado","Pop"]},
    # ROCK/POP CLÁSSICO
    {"id":"ar_de_rock_alb",        "nome":"Ar de Rock",                   "anoLancamento":1980, "lancadoPor":"rui_veloso",       "generos":["Rock","Blues"]},
    {"id":"anjo_da_guarda_alb",    "nome":"Anjo da Guarda",               "anoLancamento":1983, "lancadoPor":"antonio_variacoes","generos":["Pop"]},
    {"id":"cafe_berlin_alb",       "nome":"Café Berlim",                  "anoLancamento":1986, "lancadoPor":"antonio_variacoes","generos":["Pop","Rock"]},
    {"id":"album_1111",            "nome":"Quarteto 1111",                "anoLancamento":1970, "lancadoPor":"quarteto_1111",    "generos":["Rock"]},
    {"id":"taxi_81",               "nome":"Táxi",                         "anoLancamento":1981, "lancadoPor":"taxi",             "generos":["Rock"]},
    {"id":"madrugada_80",          "nome":"À Flor da Pele",               "anoLancamento":1981, "lancadoPor":"uhf",              "generos":["Rock"]},
    {"id":"a_um_deus_alb",         "nome":"A um Deus Desconhecido",       "anoLancamento":1984, "lancadoPor":"setima_legiao",    "generos":["Pop"]},
    {"id":"ao_vivo_setima",        "nome":"Ao Vivo",                      "anoLancamento":1989, "lancadoPor":"setima_legiao",    "generos":["Pop","Rock"]},
    {"id":"irreligious",           "nome":"Irreligious",                  "anoLancamento":1996, "lancadoPor":"moonspell",        "generos":["Rock","Metal"]},
    {"id":"wolfheart_alb",         "nome":"Wolfheart",                    "anoLancamento":1995, "lancadoPor":"moonspell",        "generos":["Rock","Metal"]},
    {"id":"night_eternal_alb",     "nome":"Night Eternal",                "anoLancamento":2008, "lancadoPor":"moonspell",        "generos":["Rock","Metal"]},
    {"id":"subtilezas_bairro",     "nome":"Subtilezas de um Rapaz de Bairro","anoLancamento":1992,"lancadoPor":"ex_votos",       "generos":["Rock","Indie"]},
    {"id":"mutantes_alb",          "nome":"Mutantes S.21",                "anoLancamento":1992, "lancadoPor":"mao_morta",        "generos":["Rock","Indie"]},
    {"id":"ganda_banda_alb",       "nome":"Ganda Banda",                  "anoLancamento":1998, "lancadoPor":"quinta_do_bill",   "generos":["Rock"]},
    {"id":"portem_se_bem_alb",     "nome":"Portem-se Bem",                "anoLancamento":1989, "lancadoPor":"peste_sida",       "generos":["Rock","Indie"]},
    {"id":"cancoes_pos_guerra",    "nome":"Canções do Pós-Guerra",        "anoLancamento":2020, "lancadoPor":"jorge_palma",      "generos":["Rock"]},
    {"id":"fragil_alb",            "nome":"Frágil",                       "anoLancamento":1985, "lancadoPor":"jorge_palma",      "generos":["Rock","Pop"]},
    {"id":"ornatos_adeus",         "nome":"Adeus Tristeza",               "anoLancamento":1995, "lancadoPor":"ornatos_violeta",  "generos":["Rock","Indie"]},
    {"id":"ornatos_calmamente",    "nome":"Calmamente",                   "anoLancamento":1999, "lancadoPor":"ornatos_violeta",  "generos":["Rock","Indie"]},
    {"id":"xutos_confidencial",    "nome":"Confidencial",                 "anoLancamento":1985, "lancadoPor":"xutos_pontapes",   "generos":["Rock"]},
    {"id":"xutos_barrotes",        "nome":"Barrotes",                     "anoLancamento":1982, "lancadoPor":"xutos_pontapes",   "generos":["Rock"]},
    {"id":"herois_vikings",        "nome":"Os Vikings",                   "anoLancamento":1983, "lancadoPor":"herois_do_mar",    "generos":["Pop","Rock"]},
    {"id":"madredeus_o_espirito",  "nome":"O Espírito da Paz",            "anoLancamento":1994, "lancadoPor":"madredeus",        "generos":["Folk","Indie"]},
    {"id":"madredeus_ainda",       "nome":"Ainda",                        "anoLancamento":1995, "lancadoPor":"madredeus",        "generos":["Folk","Indie"]},
    {"id":"capitao_fausto_monte",  "nome":"Monte Selvatico",              "anoLancamento":2017, "lancadoPor":"capitao_fausto",   "generos":["Rock","Indie"]},
    # POP CONTEMPORÂNEO
    {"id":"flores_cinema",         "nome":"Flarixa Flaus",                "anoLancamento":2023, "lancadoPor":"barbara_bandeira", "generos":["Pop"]},
    {"id":"sobral_amar_pelos_2",   "nome":"Amar Pelos Dois",              "anoLancamento":2017, "lancadoPor":"salvador_sobral",  "generos":["Pop","Jazz"]},
    {"id":"vinyl_album",           "nome":"Vinyl",                        "anoLancamento":2017, "lancadoPor":"the_gift",         "generos":["Pop","Indie"]},
    {"id":"cancao_deolinda",       "nome":"Canção ao Lado",               "anoLancamento":2008, "lancadoPor":"deolinda",         "generos":["Pop","Fado"]},
    {"id":"deolinda_dois",         "nome":"Dois",                         "anoLancamento":2015, "lancadoPor":"deolinda",         "generos":["Pop","Folk"]},
    {"id":"baza_baza_reggae",      "nome":"Janela para o Recreio",        "anoLancamento":1995, "lancadoPor":"kussondulola",     "generos":["Pop","Reggae"]},
    {"id":"dino_santiago_mundu",   "nome":"Mundu Nôbu",                   "anoLancamento":2021, "lancadoPor":"dino_d_santiago",  "generos":["RB","Kizomba","Pop"]},
    # HIP-HOP
    {"id":"black_diamond_alb",     "nome":"Black Diamond",                "anoLancamento":2008, "lancadoPor":"buraka_som_sistema","generos":["HipHop","Electronica"]},
    {"id":"sara_balance",          "nome":"Balancê",                      "anoLancamento":2008, "lancadoPor":"sara_tavares",     "generos":["Pop","RB","Soul"]},
    {"id":"afro_fado_album",       "nome":"Afro Fado",                    "anoLancamento":2023, "lancadoPor":"slow_j",           "generos":["HipHop","Pop"]},
    {"id":"servico_publico_alb",   "nome":"Serviço Público",              "anoLancamento":2006, "lancadoPor":"valete",           "generos":["HipHop"]},
    {"id":"valete_estado_alb",     "nome":"Estado de Sítio",              "anoLancamento":2012, "lancadoPor":"valete",           "generos":["HipHop"]},
    {"id":"capicua_anelar",        "nome":"Anelar",                       "anoLancamento":2014, "lancadoPor":"capicua",          "generos":["HipHop"]},
    {"id":"boss_ac_anti",          "nome":"Anti",                         "anoLancamento":2003, "lancadoPor":"boss_ac",          "generos":["HipHop"]},
    # INTERVENÇÃO
    {"id":"zeca_bancal_alb",       "nome":"Balada do Outono",             "anoLancamento":1964, "lancadoPor":"zeca_afonso",      "generos":["Intervencao","Folk"]},
    {"id":"grandola_alb",          "nome":"Cantigas do Maio",             "anoLancamento":1971, "lancadoPor":"zeca_afonso",      "generos":["Intervencao"]},
    {"id":"sergio_caminhante",     "nome":"Caminhante",                   "anoLancamento":1974, "lancadoPor":"sergio_godinho",   "generos":["Intervencao"]},
    # PIMBA
    {"id":"atento_album",          "nome":"Atento",                       "anoLancamento":2003, "lancadoPor":"quim_barreiros",   "generos":["Pimba"]},
    {"id":"es_tao_sensual_alb",    "nome":"És Tão Sensual",               "anoLancamento":2002, "lancadoPor":"toy",              "generos":["Pimba"]},
    {"id":"coracao_de_pau_alb",    "nome":"Coração de Pau",               "anoLancamento":1997, "lancadoPor":"agata",            "generos":["Pimba"]},
]

# ══════════════════════════════════════════════════════════════════════
# MÚSICAS (expandido)
# ══════════════════════════════════════════════════════════════════════
musicas = [
    # FADO
    {"id":"estranha_forma_mus",    "nome":"Estranha Forma de Vida",    "interpretadaPor":["amalia_rodrigues"], "pertenceAoAlbum":"estranha_forma_vida", "generos":["Fado"], "duracao":213,
     "curiosidade":"Baseada num poema de Florbela Espanca."},
    {"id":"uma_casa_portuguesa",   "nome":"Uma Casa Portuguesa",       "interpretadaPor":["amalia_rodrigues"], "generos":["Fado"], "duracao":178,
     "curiosidade":"Um dos temas mais identificativos de Amália no estrangeiro."},
    {"id":"lagrima_mus",           "nome":"Lágrima",                   "interpretadaPor":["amalia_rodrigues"], "pertenceAoAlbum":"com_que_voz", "generos":["Fado"], "duracao":195},
    {"id":"povo_que_lavas",        "nome":"Povo Que Lavas no Rio",     "interpretadaPor":["amalia_rodrigues"], "generos":["Fado"], "duracao":224,
     "curiosidade":"Letra de Pedro Homem de Melo."},
    {"id":"barco_negro",           "nome":"Barco Negro",               "interpretadaPor":["amalia_rodrigues"], "generos":["Fado"], "duracao":240,
     "curiosidade":"Considerada uma das mais belas canções de Amália."},
    {"id":"com_que_voz_mus",       "nome":"Com Que Voz",               "interpretadaPor":["amalia_rodrigues"], "pertenceAoAlbum":"com_que_voz", "generos":["Fado"], "duracao":208,
     "curiosidade":"Letra baseada num poema de Luís de Camões."},
    {"id":"um_homem_cidade",       "nome":"Um Homem na Cidade",        "interpretadaPor":["carlos_do_carmo"],  "pertenceAoAlbum":"fado_em_mim", "generos":["Fado"], "duracao":255},
    {"id":"lisboa_menina_moca",    "nome":"Lisboa, Menina e Moça",     "interpretadaPor":["carlos_do_carmo"],  "generos":["Fado"], "duracao":230},
    {"id":"corre_mus",             "nome":"Corre",                     "interpretadaPor":["mariza"],            "pertenceAoAlbum":"mariza_fado_em_mim", "generos":["Fado"], "duracao":245},
    {"id":"transparente_mus",      "nome":"Transparente",              "interpretadaPor":["mariza"],            "pertenceAoAlbum":"transparente_alb", "generos":["Fado"], "duracao":228},
    {"id":"fado_da_saudade_mus",   "nome":"Fado da Saudade",           "interpretadaPor":["carminho"],          "pertenceAoAlbum":"fado_mae", "generos":["Fado"], "duracao":217},
    {"id":"desfado_mus",           "nome":"Desfado",                   "interpretadaPor":["ana_moura"],         "pertenceAoAlbum":"ana_moura_desfado", "generos":["Fado"], "duracao":234},
    {"id":"duende_gisela",         "nome":"Duende",                    "interpretadaPor":["gisela_joao"],       "pertenceAoAlbum":"gisela_gisela", "generos":["Fado"], "duracao":198},
    {"id":"zambujo_alfama_mus",    "nome":"Alfama",                    "interpretadaPor":["antonio_zambujo"],   "pertenceAoAlbum":"zambujo_alfama", "generos":["Fado","Pop"], "duracao":262},
    {"id":"pica_do_sete",          "nome":"O Pica do Sete",            "interpretadaPor":["antonio_zambujo"],   "generos":["Fado","Pop"], "duracao":215},

    # INTERVENÇÃO
    {"id":"grandola_mus",          "nome":"Grândola, Vila Morena",     "interpretadaPor":["zeca_afonso"],       "pertenceAoAlbum":"grandola_alb", "generos":["Intervencao","Folk"], "duracao":276,
     "curiosidade":"Serviu de sinal para o início da Revolução dos Cravos a 25 de Abril de 1974."},
    {"id":"vejam_bem_mus",         "nome":"Vejam Bem",                 "interpretadaPor":["zeca_afonso"],       "generos":["Intervencao"], "duracao":195},
    {"id":"menino_bairro_negro",   "nome":"Menino do Bairro Negro",    "interpretadaPor":["zeca_afonso"],       "generos":["Intervencao","Folk"], "duracao":210},
    {"id":"traz_outro_amigo",      "nome":"Traz Outro Amigo Também",   "interpretadaPor":["zeca_afonso"],       "pertenceAoAlbum":"zeca_bancal_alb", "generos":["Intervencao","Folk"], "duracao":183},
    {"id":"primeiro_dia_mus",      "nome":"Primeiro Dia",              "interpretadaPor":["sergio_godinho"],    "pertenceAoAlbum":"sergio_caminhante", "generos":["Intervencao"], "duracao":222},
    {"id":"carvalhesa_mus",        "nome":"A Carvalhesa",              "interpretadaPor":["adriano_correia"],   "generos":["Intervencao"], "duracao":198},
    {"id":"pintassilgo_mus",       "nome":"Como um Pintassilgo",       "interpretadaPor":["vitorino"],          "generos":["Intervencao","Folk"], "duracao":205},

    # ROCK/POP CLÁSSICO
    {"id":"cancao_engate",         "nome":"Canção de Engate",          "interpretadaPor":["antonio_variacoes"], "pertenceAoAlbum":"anjo_da_guarda_alb", "generos":["Pop"], "duracao":188},
    {"id":"estou_alem_mus",        "nome":"Estou Além",                "interpretadaPor":["antonio_variacoes"], "pertenceAoAlbum":"cafe_berlin_alb", "generos":["Pop","Rock"], "duracao":215},
    {"id":"povo_que_amas_mus",     "nome":"O Povo Que Amas em Demasia","interpretadaPor":["antonio_variacoes"],"generos":["Pop"], "duracao":197},
    {"id":"porto_sentido_mus",     "nome":"Porto Sentido",             "interpretadaPor":["rui_veloso"],        "pertenceAoAlbum":"ar_de_rock_alb", "generos":["Rock"], "duracao":298,
     "curiosidade":"Hino não oficial da cidade do Porto."},
    {"id":"chico_fininho_mus",     "nome":"Chico Fininho",             "interpretadaPor":["rui_veloso"],        "generos":["Rock","Blues"], "duracao":245},
    {"id":"fragil_mus",            "nome":"Frágil",                    "interpretadaPor":["jorge_palma"],       "pertenceAoAlbum":"fragil_alb", "generos":["Rock"], "duracao":256},
    {"id":"aprender_voar_mus",     "nome":"Aprender a Voar",           "interpretadaPor":["jorge_palma"],       "pertenceAoAlbum":"cancoes_pos_guerra", "generos":["Rock"], "duracao":271},
    {"id":"depois_adeus_mus",      "nome":"E Depois do Adeus",         "interpretadaPor":["paulo_de_carvalho"], "generos":["Pop"], "duracao":183,
     "curiosidade":"Sinal da Revolução dos Cravos em conjunto com Grândola Vila Morena."},
    {"id":"playback_mus",          "nome":"Playback",                  "interpretadaPor":["carlos_paiao"],      "generos":["Pop"], "duracao":201},
    {"id":"cinderela_mus",         "nome":"Cinderela",                 "interpretadaPor":["carlos_paiao"],      "generos":["Pop"], "duracao":195},
    {"id":"contentores_mus",       "nome":"Contentores",               "interpretadaPor":["xutos_pontapes"],    "pertenceAoAlbum":"xutos_confidencial", "generos":["Rock"], "duracao":312},
    {"id":"nao_sao_ceus_mus",      "nome":"Não São os Céus",           "interpretadaPor":["xutos_pontapes"],    "generos":["Rock"], "duracao":278},
    {"id":"sol_e_chuva_mus",       "nome":"Sol e Chuva",               "interpretadaPor":["xutos_pontapes"],    "generos":["Rock"], "duracao":265},
    {"id":"deus_desconhecido_mus", "nome":"A um Deus Desconhecido",    "interpretadaPor":["setima_legiao"],     "pertenceAoAlbum":"a_um_deus_alb", "generos":["Pop"], "duracao":240},
    {"id":"chama_mus",             "nome":"Chama",                     "interpretadaPor":["setima_legiao"],     "generos":["Pop","Rock"], "duracao":228},
    {"id":"opium_mus",             "nome":"Opium",                     "interpretadaPor":["moonspell"],         "pertenceAoAlbum":"irreligious", "generos":["Rock","Metal"], "duracao":325},
    {"id":"wolfheart_mus",         "nome":"Wolfheart",                 "interpretadaPor":["moonspell"],         "pertenceAoAlbum":"wolfheart_alb", "generos":["Rock","Metal"], "duracao":289},
    {"id":"night_eternal_mus",     "nome":"Night Eternal",             "interpretadaPor":["moonspell"],         "pertenceAoAlbum":"night_eternal_alb", "generos":["Rock","Metal"], "duracao":301},
    {"id":"mais_alguem_mus",       "nome":"Mais Alguém",               "interpretadaPor":["ornatos_violeta"],   "pertenceAoAlbum":"ornatos_calmamente", "generos":["Rock","Indie"], "duracao":295},
    {"id":"adeus_tristeza_mus",    "nome":"Adeus Tristeza",            "interpretadaPor":["ornatos_violeta"],   "pertenceAoAlbum":"ornatos_adeus", "generos":["Rock","Indie"], "duracao":310},
    {"id":"o_rio_mus",             "nome":"O Rio",                     "interpretadaPor":["ornatos_violeta"],   "pertenceAoAlbum":"ornatos_calmamente", "generos":["Rock","Indie"], "duracao":267},
    {"id":"chiclete_mus",          "nome":"Chiclete",                  "interpretadaPor":["taxi"],              "pertenceAoAlbum":"taxi_81", "generos":["Rock"], "duracao":223},
    {"id":"cavalo_corrida_mus",    "nome":"Cavalo de Corrida",         "interpretadaPor":["uhf"],               "pertenceAoAlbum":"madrugada_80", "generos":["Rock"], "duracao":248},
    {"id":"lenda_elrei_mus",       "nome":"Lenda de El-Rei D. Sebastião","interpretadaPor":["quarteto_1111"],  "pertenceAoAlbum":"album_1111", "generos":["Rock"], "duracao":275},
    {"id":"vikings_mus",           "nome":"Vikings",                   "interpretadaPor":["herois_do_mar"],     "pertenceAoAlbum":"herois_vikings", "generos":["Pop","Rock"], "duracao":215},
    # MADREDEUS
    {"id":"o_pastor_mus",          "nome":"O Pastor",                  "interpretadaPor":["madredeus"],         "pertenceAoAlbum":"madredeus_ainda", "generos":["Folk","Indie"], "duracao":280,
     "curiosidade":"Usada na banda sonora do filme 'Lisboa Story' de Wim Wenders."},
    {"id":"o_mar_mus",             "nome":"O Mar",                     "interpretadaPor":["madredeus"],         "pertenceAoAlbum":"madredeus_o_espirito", "generos":["Folk","Indie"], "duracao":245},
    # POP CONTEMPORÂNEO
    {"id":"parva_que_sou_mus",     "nome":"Parva que Sou",             "interpretadaPor":["deolinda"],          "pertenceAoAlbum":"cancao_deolinda", "generos":["Pop","Fado"], "duracao":233,
     "curiosidade":"Tornou-se um hino da geração precária portuguesa."},
    {"id":"a_estranheza_mus",      "nome":"A Estranheza",              "interpretadaPor":["deolinda"],          "pertenceAoAlbum":"deolinda_dois", "generos":["Pop"], "duracao":219},
    {"id":"driving_slow_mus",      "nome":"Driving You Slow",          "interpretadaPor":["the_gift"],          "pertenceAoAlbum":"vinyl_album", "generos":["Pop","Indie"], "duracao":248},
    {"id":"amar_pelos_dois_mus",   "nome":"Amar Pelos Dois",           "interpretadaPor":["salvador_sobral"],   "pertenceAoAlbum":"sobral_amar_pelos_2", "generos":["Pop","Jazz"], "duracao":185,
     "compostaPor":["luisa_sobral"], "curiosidade":"Venceu o Festival Eurovisão 2017 com a maior margem de pontos da história."},
    {"id":"como_tu_mus",           "nome":"Como Tu (feat. Ivandro)",   "interpretadaPor":["barbara_bandeira","ivandro"], "pertenceAoAlbum":"flores_cinema", "generos":["Pop"], "duracao":202},
    {"id":"nos_os_dois_mus",       "nome":"Nós os Dois",               "interpretadaPor":["barbara_bandeira"],  "generos":["Pop"], "duracao":188},
    {"id":"balance_mus",           "nome":"Balancê",                   "interpretadaPor":["sara_tavares"],      "pertenceAoAlbum":"sara_balance", "generos":["Pop","RB","Soul"], "duracao":265},
    # HIP-HOP
    {"id":"where_heart_is_mus",    "nome":"Where x Heart Is",          "interpretadaPor":["slow_j"],            "pertenceAoAlbum":"afro_fado_album", "generos":["HipHop","Pop"], "duracao":238},
    {"id":"roleta_russa_mus",      "nome":"Roleta Russa",              "interpretadaPor":["valete"],             "pertenceAoAlbum":"servico_publico_alb", "generos":["HipHop"], "duracao":278},
    {"id":"estado_sitio_mus",      "nome":"Estado de Sítio",           "interpretadaPor":["valete"],             "pertenceAoAlbum":"valete_estado_alb", "generos":["HipHop"], "duracao":264},
    {"id":"capicua_anelar_mus",    "nome":"Anelar",                    "interpretadaPor":["capicua"],            "pertenceAoAlbum":"capicua_anelar", "generos":["HipHop"], "duracao":255},
    {"id":"kalemba_mus",           "nome":"Kalemba (Wegue Wegue)",     "interpretadaPor":["buraka_som_sistema"], "pertenceAoAlbum":"black_diamond_alb", "generos":["HipHop","Electronica"], "duracao":302,
     "curiosidade":"Tornou-se viral internacionalmente em 2008."},
    {"id":"boss_anti_mus",         "nome":"Anti",                      "interpretadaPor":["boss_ac"],            "pertenceAoAlbum":"boss_ac_anti", "generos":["HipHop"], "duracao":245},
    {"id":"danca_reggae_mus",      "nome":"Dança Reggae",              "interpretadaPor":["kussondulola"],       "pertenceAoAlbum":"baza_baza_reggae", "generos":["Pop","Reggae"], "duracao":239},
    # PIMBA
    {"id":"garagem_vizinha_mus",   "nome":"A Garagem da Vizinha",      "interpretadaPor":["quim_barreiros"],    "pertenceAoAlbum":"atento_album", "generos":["Pimba"], "duracao":205},
    {"id":"mestre_culinario_mus",  "nome":"O Mestre de Culinária",     "interpretadaPor":["quim_barreiros"],    "generos":["Pimba"], "duracao":198},
    {"id":"coracao_melao_mus",     "nome":"Coração de Melão",          "interpretadaPor":["toy"],               "pertenceAoAlbum":"es_tao_sensual_alb", "generos":["Pimba"], "duracao":212},
    {"id":"coracao_pau_mus",       "nome":"Coração de Pau",            "interpretadaPor":["agata"],             "pertenceAoAlbum":"coracao_de_pau_alb", "generos":["Pimba"], "duracao":220},
    # OUTROS
    {"id":"subtilezas_mus",        "nome":"Subtilezas de um Rapaz de Bairro","interpretadaPor":["ex_votos"],    "pertenceAoAlbum":"subtilezas_bairro", "generos":["Rock","Indie"], "duracao":267},
    {"id":"filhos_tedio_mus",      "nome":"Filhos do Tédio",           "interpretadaPor":["quinta_do_bill"],    "pertenceAoAlbum":"ganda_banda_alb", "generos":["Rock"], "duracao":243},
    {"id":"sol_caparica_mus",      "nome":"Sol da Caparica",           "interpretadaPor":["peste_sida"],        "pertenceAoAlbum":"portem_se_bem_alb", "generos":["Rock","Indie"], "duracao":258},
    {"id":"mais_alguem_capfausto", "nome":"Enquanto Houver Estradas",  "interpretadaPor":["capitao_fausto"],    "pertenceAoAlbum":"capitao_fausto_monte", "generos":["Rock","Indie"], "duracao":271},
    {"id":"dino_mundu_mus",        "nome":"Mundu Nôbu",                "interpretadaPor":["dino_d_santiago"],   "pertenceAoAlbum":"dino_santiago_mundu", "generos":["RB","Kizomba","Pop"], "duracao":249},
]

# ══════════════════════════════════════════════════════════════════════
# PRÉMIOS
# ══════════════════════════════════════════════════════════════════════
premios = [
    {"id":"eurovisao_2017",      "nome":"Eurovision Song Contest 2017",  "anoPremio":2017, "categoriaPremio":"Primeiro Lugar", "entidadePremio":"European Broadcasting Union", "ganhadoPor":"salvador_sobral"},
    {"id":"globo_ouro_amalia",   "nome":"Globo de Ouro Carreira",        "anoPremio":2019, "categoriaPremio":"Carreira",       "entidadePremio":"Globos de Ouro (SIC)",          "ganhadoPor":"mariza"},
    {"id":"order_merit_amalia",  "nome":"Ordem do Mérito (Grã-Cruz)",    "anoPremio":1990, "categoriaPremio":"Mérito Civil",   "entidadePremio":"Estado Português",             "ganhadoPor":"amalia_rodrigues"},
    {"id":"premio_mpa_capicua",  "nome":"Prémio Música Portuguesa",      "anoPremio":2015, "categoriaPremio":"Hip-Hop",        "entidadePremio":"Associação Portuguesa de Editoras","ganhadoPor":"capicua"},
    {"id":"premio_zdb_ornatos",  "nome":"Prémio ZDB",                    "anoPremio":2000, "categoriaPremio":"Álbum do Ano",   "entidadePremio":"Zinc Discos",                  "ganhadoPor":"ornatos_violeta"},
    {"id":"world_music_mariza",  "nome":"BBC Radio 3 World Music Award", "anoPremio":2006, "categoriaPremio":"Europe Award",   "entidadePremio":"BBC Radio 3",                  "ganhadoPor":"mariza"},
    {"id":"wma_ana_moura",       "nome":"BBC Radio 3 World Music Award", "anoPremio":2014, "categoriaPremio":"Europe Award",   "entidadePremio":"BBC Radio 3",                  "ganhadoPor":"ana_moura"},
    {"id":"prémio_carlos_paredes","nome":"Prémio Carlos Paredes",        "anoPremio":2005, "categoriaPremio":"Música",        "entidadePremio":"Câmara Municipal de Lisboa",    "ganhadoPor":"carminho"},
    {"id":"globo_ouro_banda_deolinda","nome":"Globo de Ouro Melhor Banda","anoPremio":2010,"categoriaPremio":"Melhor Banda",  "entidadePremio":"Globos de Ouro (SIC)",          "ganhadoPor":"deolinda"},
    {"id":"antena3_moonspell",   "nome":"Antena 3 Music Awards",         "anoPremio":2012, "categoriaPremio":"Melhor Banda Rock","entidadePremio":"Antena 3 / RTP",             "ganhadoPor":"moonspell"},
]

# ══════════════════════════════════════════════════════════════════════
# CONCERTOS
# ══════════════════════════════════════════════════════════════════════
concertos = [
    {"id":"amalia_carnegie_1952", "nome":"Amália no Carnegie Hall",     "dataConcerto":"1952-01-15", "localConcerto":"Carnegie Hall",        "cidadeConcerto":"Nova Iorque",    "paisConcerto":"EUA",      "artista":"amalia_rodrigues"},
    {"id":"mariza_coliseu_2004",  "nome":"Mariza — Coliseu dos Recreios","dataConcerto":"2004-03-20","localConcerto":"Coliseu dos Recreios", "cidadeConcerto":"Lisboa",        "paisConcerto":"Portugal", "artista":"mariza"},
    {"id":"ana_moura_royal_albert","nome":"Ana Moura — Royal Albert Hall","dataConcerto":"2013-11-12","localConcerto":"Royal Albert Hall",   "cidadeConcerto":"Londres",       "paisConcerto":"Reino Unido","artista":"ana_moura"},
    {"id":"sobral_eurovisao_2017","nome":"Salvador Sobral — Eurovision 2017","dataConcerto":"2017-05-13","localConcerto":"Kiev Arena",       "cidadeConcerto":"Kiev",          "paisConcerto":"Ucrânia",  "artista":"salvador_sobral"},
    {"id":"zeca_coliseu_1983",    "nome":"Zeca Afonso — Coliseu",        "dataConcerto":"1983-04-25","localConcerto":"Coliseu dos Recreios", "cidadeConcerto":"Lisboa",        "paisConcerto":"Portugal", "artista":"zeca_afonso"},
    {"id":"moonspell_rock_in_rio","nome":"Moonspell — Rock in Rio Lisboa","dataConcerto":"2006-06-02","localConcerto":"Parque da Bela Vista","cidadeConcerto":"Lisboa",        "paisConcerto":"Portugal", "artista":"moonspell"},
    {"id":"xutos_estadio_luz_2016","nome":"Xutos — Estádio da Luz",      "dataConcerto":"2016-07-09","localConcerto":"Estádio da Luz",       "cidadeConcerto":"Lisboa",        "paisConcerto":"Portugal", "artista":"xutos_pontapes"},
    {"id":"ornatos_coliseu_2002", "nome":"Ornatos Violeta — Despedida",  "dataConcerto":"2002-07-20","localConcerto":"Coliseu do Porto",     "cidadeConcerto":"Porto",         "paisConcerto":"Portugal", "artista":"ornatos_violeta"},
    {"id":"deolinda_novas_doc",   "nome":"Deolinda — Campo Pequeno",     "dataConcerto":"2011-04-13","localConcerto":"Campo Pequeno",        "cidadeConcerto":"Lisboa",        "paisConcerto":"Portugal", "artista":"deolinda"},
    {"id":"capicua_porto_2015",   "nome":"Capicua — Casa da Música",     "dataConcerto":"2015-09-18","localConcerto":"Casa da Música",       "cidadeConcerto":"Porto",         "paisConcerto":"Portugal", "artista":"capicua"},
]

# ══════════════════════════════════════════════════════════════════════
# TOURS
# ══════════════════════════════════════════════════════════════════════
tours = [
    {"id":"mariza_world_2005",    "nome":"Mariza World Tour 2005",      "artista":"mariza",       "concertos":["mariza_coliseu_2004"]},
    {"id":"sobral_tour_2017",     "nome":"Amar Pelos Dois — European Tour","artista":"salvador_sobral","concertos":["sobral_eurovisao_2017"]},
    {"id":"moonspell_tour_2006",  "nome":"Memorial Tour 2006",          "artista":"moonspell",    "concertos":["moonspell_rock_in_rio"]},
]

# ══════════════════════════════════════════════════════════════════════
# COLABORAÇÕES
# ══════════════════════════════════════════════════════════════════════
colaboracoes = [
    {"artista1":"barbara_bandeira", "artista2":"ivandro",         "musica":"como_tu_mus"},
    {"artista1":"salvador_sobral",  "artista2":"luisa_sobral",    "musica":"amar_pelos_dois_mus"},
    {"artista1":"ana_moura",        "artista2":"antonio_zambujo", "nota":"Colaboração em digressão conjunta 2014"},
    {"artista1":"slow_j",           "artista2":"capicua",         "nota":"Colaboração em faixa de Afro Fado"},
    {"artista1":"deolinda",         "artista2":"carminho",        "nota":"Concerto conjunto no Coliseu 2012"},
    {"artista1":"buraka_som_sistema","artista2":"dino_d_santiago","nota":"Colaboração em Black Diamond"},
    {"artista1":"rodrigo_leao",     "artista2":"teresa_salgueiro","nota":"Membros dos Madredeus"},
    {"artista1":"manel_cruz",       "artista2":"ornatos_violeta", "nota":"Manel Cruz foi vocalista dos Ornatos Violeta"},
    {"artista1":"rui_veloso",       "artista2":"jorge_palma",     "nota":"Concertos conjuntos ao longo dos anos 80-90"},
    {"artista1":"mariza",           "artista2":"ana_moura",       "nota":"Representantes do fado da nova geração"},
]

# ══════════════════════════════════════════════════════════════════════
# INFLUÊNCIAS
# ══════════════════════════════════════════════════════════════════════
influencias = [
    {"influenciador":"amalia_rodrigues",  "influenciado":"mariza"},
    {"influenciador":"amalia_rodrigues",  "influenciado":"carminho"},
    {"influenciador":"amalia_rodrigues",  "influenciado":"ana_moura"},
    {"influenciador":"amalia_rodrigues",  "influenciado":"gisela_joao"},
    {"influenciador":"carlos_do_carmo",   "influenciado":"antonio_zambujo"},
    {"influenciador":"zeca_afonso",       "influenciado":"sergio_godinho"},
    {"influenciador":"zeca_afonso",       "influenciado":"adriano_correia"},
    {"influenciador":"rui_veloso",        "influenciado":"jorge_palma"},
    {"influenciador":"rui_veloso",        "influenciado":"ornatos_violeta"},
    {"influenciador":"antonio_variacoes", "influenciado":"barbara_bandeira"},
    {"influenciador":"ornatos_violeta",   "influenciado":"capitao_fausto"},
    {"influenciador":"ornatos_violeta",   "influenciado":"linda_martini"},
    {"influenciador":"boss_ac",           "influenciado":"valete"},
    {"influenciador":"boss_ac",           "influenciado":"capicua"},
    {"influenciador":"madredeus",         "influenciado":"deolinda"},
    {"influenciador":"buraka_som_sistema","influenciado":"slow_j"},
]

print("\n=== A gerar datasets expandidos de Música Portuguesa ===\n")
gravar('editoras.json',    {"editoras":    editoras})
gravar('artistas.json',    {"artistasSolo": artistas_solo})
gravar('bandas.json',      {"bandas":      bandas})
gravar('albuns.json',      {"albuns":      albuns})
gravar('musicas.json',     {"musicas":     musicas})
gravar('premios.json',     {"premios":     premios})
gravar('concertos.json',   {"concertos":   concertos})
gravar('tours.json',       {"tours":       tours})
gravar('colaboracoes.json',{"colaboracoes":colaboracoes})
gravar('influencias.json', {"influencias": influencias})

print(f"""
✅  Datasets gerados com sucesso!
    Editoras     : {len(editoras)}
    Artistas     : {len(artistas_solo)}
    Bandas       : {len(bandas)}
    Álbuns       : {len(albuns)}
    Músicas      : {len(musicas)}
    Prémios      : {len(premios)}
    Concertos    : {len(concertos)}
    Colaborações : {len(colaboracoes)}
    Influências  : {len(influencias)}
""")