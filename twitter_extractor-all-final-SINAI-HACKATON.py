# uso: twitter_extractor-all-final-SINAI-HACKATON <localizacion>

import tweepy
import sys
import json
import re
import string
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime 
from elasticsearch import Elasticsearch 
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from stop_words import get_stop_words
from langdetect import detect
import time
from http.client import IncompleteRead
from urllib3.exceptions import ProtocolError

'''
@author Jiménez Zafra, Salud María 
@author Plaza del Arco, Flor Miriam
@author García Cumbreras, Miguel Ángel

@created_at enero 2018
'''

localizacion=sys.argv[1]

# Create authentication via Oauth2 twitter
consumer_key = '' 
consumer_secret = '' 
access_token = '' 
access_secret = ''


# KEYWORDS ESPAÑOL
keywords_basic_ebola = ["ebola", "ébola"]
keywords_basic_gripe = ["gripe", "trancazo", "influenza"]
keywords_basic_resfriado = ["resfriado", "catarro", "constipado", "resfriamiento"]
keywords_basic_cancer = ["cáncer", "cancer", "tumor", "carcinoma", "granuloma", "epitelioma", "sarcoma", "neoplasia", "cefaloma"]
keywords_basic_asma = ["asma", "disnea"]
keywords_basic_hepatitis = ["hepatitis"]
keywords_basic_otitis = ["otitis"]
keywords_basic_diabetes = ["diabetes", "glucosuria"]
keywords_basic_caries = ["caries"]
keywords_basic_anorexia = ["anorexia"]
keywords_basic_obesidad = ["obesidad", "gordura", "adiposidad"]
keywords_basic_alzheimer = ["alzheimer"]
keywords_basic_sida = ["sida", "vih"]
keywords_basic_varicela = ["varicela"]
keywords_basic_sarampion = ["sarampion", "sarampión"]
keywords_basic_apendicitis = ["apendicitis"]

keywords_basic_es = [keywords_basic_ebola, keywords_basic_gripe, keywords_basic_resfriado, keywords_basic_cancer, keywords_basic_asma, keywords_basic_hepatitis, keywords_basic_otitis, keywords_basic_diabetes, keywords_basic_caries, keywords_basic_anorexia, keywords_basic_obesidad, keywords_basic_alzheimer, keywords_basic_sida, keywords_basic_varicela, keywords_basic_sarampion, keywords_basic_apendicitis]

# KEYWORDS CATALÁN
keywords_cat_ebola = ["ebola", "ebola"]
keywords_cat_gripe = ["grip", "trancazo", "influença"]
keywords_cat_resfriado = ["refredat", "refredat", "constipat", "refredament"]
keywords_cat_cancer = ["càncer", "tumor", "carcinoma", "granuloma", "epitelioma", "sarcoma", "neoplàsia", "cefaloma"]
keywords_cat_asma = ["asma", "dispnea"]
keywords_cat_hepatitis = ["hepatitis"]
keywords_cat_otitis = ["otitis"]
keywords_cat_diabetes = ["diabetis" "glucosúria"]
keywords_cat_caries = ["càries", "picada", "úlcera", "perforació", "horadación"]
keywords_cat_anorexia = ["anorèxia"]
keywords_cat_obesidad = ["obesitat", "grassor", "adipositat"]
keywords_cat_alzheimer = ["alzheimer"]
keywords_cat_sida = ["sida", "vih"]
keywords_cat_varicela = ["varicella"]
keywords_cat_sarampion = ["sarampion", "xarampió"]
keywords_cat_apendicitis = ["apendicitis"]

keywords_basic_cat = [keywords_cat_ebola, keywords_cat_gripe, keywords_cat_resfriado, keywords_cat_cancer, keywords_cat_asma, keywords_cat_hepatitis, keywords_cat_otitis, keywords_cat_diabetes, keywords_cat_caries, keywords_cat_anorexia, keywords_cat_obesidad, keywords_cat_alzheimer, keywords_cat_sida, keywords_cat_varicela, keywords_cat_sarampion, keywords_cat_apendicitis]

# INDEXNAMES ESPAÑOL
indexname_basic_ebola = 'twitter_basic_ebola'
indexname_basic_gripe = 'twitter_basic_gripe'
indexname_basic_resfriado = 'twitter_basic_resfriado'
indexname_basic_cancer = 'twitter_basic_cancer'
indexname_basic_asma = 'twitter_basic_asma'
indexname_basic_hepatitis = 'twitter_basic_hepatitis'
indexname_basic_otitis = 'twitter_basic_otitis'
indexname_basic_diabetes = 'twitter_basic_diabetes'
indexname_basic_caries = 'twitter_basic_caries'
indexname_basic_anorexia = 'twitter_basic_anorexia'
indexname_basic_obesidad = 'twitter_basic_obesidad'
indexname_basic_alzheimer = 'twitter_basic_alzheimer'
indexname_basic_sida = 'twitter_basic_sida'
indexname_basic_varicela = 'twitter_basic_varicela'
indexname_basic_sarampion = 'twitter_basic_sarampion'
indexname_basic_apendicitis = 'twitter_basic_apendicitis'

indexname_basic_es = [indexname_basic_ebola, indexname_basic_gripe, indexname_basic_resfriado, indexname_basic_cancer, indexname_basic_asma, indexname_basic_hepatitis, indexname_basic_otitis, indexname_basic_diabetes, indexname_basic_caries, indexname_basic_anorexia, indexname_basic_obesidad, indexname_basic_alzheimer, indexname_basic_sida, indexname_basic_varicela, indexname_basic_sarampion, indexname_basic_apendicitis]

# INDEXNAMES CATALÁN
indexname_basic_cat_ebola = 'twitter_basic_cat_ebola'
indexname_basic_cat_gripe = 'twitter_basic_cat_gripe'
indexname_basic_cat_resfriado = 'twitter_basic_cat_resfriado'
indexname_basic_cat_cancer = 'twitter_basic_cat_cancer'
indexname_basic_cat_asma = 'twitter_basic_cat_asma'
indexname_basic_cat_hepatitis = 'twitter_basic_cat_hepatitis'
indexname_basic_cat_otitis = 'twitter_basic_otitis'
indexname_basic_cat_diabetes = 'twitter_basic_cat_diabetes'
indexname_basic_cat_caries = 'twitter_basic_cat_caries'
indexname_basic_cat_anorexia = 'twitter_basic_cat_anorexia'
indexname_basic_cat_obesidad = 'twitter_basic_cat_obesidad'
indexname_basic_cat_alzheimer = 'twitter_basic_cat_alzheimer'
indexname_basic_cat_sida = 'twitter_basic_cat_sida'
indexname_basic_cat_varicela = 'twitter_basic_cat_varicela'
indexname_basic_cat_sarampion = 'twitter_basic_cat_sarampion'
indexname_basic_cat_apendicitis = 'twitter_basic_cat_apendicitis'

indexname_basic_cat = [indexname_basic_cat_ebola, indexname_basic_cat_gripe, indexname_basic_cat_resfriado, indexname_basic_cat_cancer, indexname_basic_cat_asma, indexname_basic_cat_hepatitis, indexname_basic_cat_otitis, indexname_basic_cat_diabetes, indexname_basic_cat_caries, indexname_basic_cat_anorexia, indexname_basic_cat_obesidad, indexname_basic_cat_alzheimer, indexname_basic_cat_sida, indexname_basic_cat_varicela, indexname_basic_cat_sarampion, indexname_basic_cat_apendicitis]


# Embeeding de Wikipedia
keywords_wiki_alzheimer = ["alzheimer", "parkinson", "enfermedad", "degenerativa", "demencia", "crohn", "incurable", "sífilis", "neurodegenerativa", "tuberculosis", "cirrosis", "diabetes", "moyamoya", "neurológica", "esquizofrenia", "leucemia", "autoinmune", "padecer", "epilepsia", "cáncer", "dolencia", "neumonía", "infecciosa", "padecía", "sepsis", "ménière", "rubéola", "enfisema", "diagnosticada", "venérea", "asma"]

keywords_wiki_asma = ["asma", "bronquitis", "reumatismo", "migrañas", "gastrointestinales", "gastritis", "sinusitis", "resfriados", "tos", "rinitis", "afecciones", "gastroenteritis", "catarros", "conjuntivitis", "diarreas", "nefritis", "ictericia", "dismenorrea", "epilepsia", "diarrea", "artritis", "colitis", "faringitis", "diabetes", "hemorragias", "ronquera", "hidropesía", "estreñimiento", "cardiovasculares", "epoc", "hemorroides"]

keywords_wiki_cancer = ["cancer", "cáncer", "próstata", "pulmón", "colorrectal", "leucemia", "melanoma", "enfisema", "páncreas", "linfoma", "tumor", "neumonía", "tuberculosis", "metastásico", "diabetes", "cánceres", "meningitis", "enfermedad", "alzheimer", "carcinoma", "hepatocarcinoma", "cirrosis", "metástasis", "microcítico", "cérvico", "peritonitis", "asma", "sífilis", "mama", "glioblastoma", "cervicouterino", "diagnosticado"]

keywords_wiki_caries = ["caries", "celulitis", "osteoartritis", "gastritis", "litiasis", "indigestión", "osteoporosis", "psoriasis", "periodontales", "gingivitis", "constipación", "amebiasis", "hepatoesplenomegalia", "dispepsias", "pancitopenia", "estreñimiento", "ielonefritis", "supuración", "leucorrea", "vaginitis", "xerosis", "tetania", "pericarditis", "rinorrea", "nefropatías", "cólicos", "acalasia", "eczemas", "meteorismo", "osteoarticulares", "hipocalcemia"]

keywords_wiki_diabetes = ["diabetes", "mellitus", "obesidad", "cardiovasculares", "hipertensión", "asma", "cardiopatías", "osteoporosis", "dislipidemia", "tabaquismo", "reumatismo", "epilepsia", "crohn", "meningitis", "bronquitis", "enfisema", "arteriosclerosis", "gastroenteritis", "cirrosis", "anemia", "gastritis", "artrosis", "cardiovascular", "migrañas", "enfermedad", "arritmia", "sepsis", "parkinson", "epoc", "gastrointestinales", "artritis"]

keywords_wiki_ebola = ["ebola", "ébola", "parainfluenza", "parotiditis", "vlfe", "poliomavirus", "vaccinia", "adenovirus", "estreptococo", "citomegalovirus", "enterovirus", "lcmv", "coronavirus", "sincitial", "vsr", "cowpox", "clamidia", "meningoencefalitis", "arbovirus", "leishmania", "pvy", "papiloma", "salmonelosis", "virus", "zóster", "tularemia", "vph", "papilomavirus", "brucelosis", "rotavirus", "shigelosis"]

keywords_wiki_gripe = ["gripe", "influenza", "h1n1", "pandemia", "viruela", "ah1n1", "sarampión", "malaria", "tifus", "sífilis", "tuberculosis", "aviar", "rubéola", "paludismo", "lepra", "tifoidea", "infección", "varicela", "neumonía", "meningitis", "bubónica", "epidémica", "contagio", "hepatitis", "h5n1", "contagiada", "disentería", "dengue", "enfermedad", "infectados", "cólera"]

keywords_wiki_hepatitis = ["hepatitis", "infección", "varicela", "meningitis", "encefalitis", "infecciosa", "sífilis", "parotiditis", "herpes", "gonorrea", "sepsis", "brucelosis", "endocarditis", "paperas", "cirrosis", "citomegalovirus", "rubéola", "gastroenteritis", "vírica", "toxoplasmosis", "hepatocarcinoma", "granulomatosa", "enfermedad", "sinusitis", "leptospirosis", "sarcoidosis", "meningoencefalitis", "sarampión", "infecciones", "malaria", "paratifoidea"]

keywords_wiki_obesidad = ["obesidad", "diabetes", "osteoporosis", "tabaquismo", "cardiovasculares", "epilepsia", "mellitus", "migrañas", "dislipidemia", "hipertensión", "asma", "sobrepeso", "desnutrición", "migraña", "cardiopatías", "hipertiroidismo", "padecer", "aterosclerosis", "hipogonadismo", "acné", "gastritis", "estreñimiento", "endocarditis", "sepsis", "hipotiroidismo", "crónicos", "gastrointestinales", "artrosis", "anorexia", "artritis", "osteoartritis"]

keywords_wiki_otitis = ["otitis", "sinusitis", "faringitis", "bronquiectasia", "bronquitis", "colecistitis", "amigdalitis", "endocarditis", "enteritis", "cistitis", "purulenta", "pancreatitis", "sarcoidosis", "epistaxis", "gastritis", "atrófica", "disquinesias", "urticaria", "flebitis", "eosinofilia", "sintomática", "hipotiroidismo", "neumonitis", "dismenorrea", "uretritis", "osteomielitis", "artralgias", "litiasis", "estomatitis", "colitis", "hepatobiliares"]

keywords_wiki_resfriado = ["resfriado", "catarro", "migrañas", "resfriados", "resfrío", "reumatismo", "gastroenteritis", "indigestión", "migraña", "cólicos", "faringitis", "sinusitis", "empacho", "diarreas", "asma", "diarrea", "varicela", "amebiasis", "reuma", "bronquitis", "amigdalitis", "urticaria", "gonorrea", "gastritis", "paperas", "úlcera", "amebiana", "neumocócica", "dispepsia", "gripales", "ferina"]

keywords_wiki_sarampión = ["sarampión", "sarampion", "viruela", "tifus", "difteria", "malaria", "rubéola", "sífilis", "paperas", "disentería", "tuberculosis", "meningitis", "varicela", "tifoidea", "paludismo", "parotiditis", "tétanos", "hepatitis", "poliomielitis", "infección", "lepra", "encefalitis", "brucelosis", "aviar", "puerperal", "epidémica", "escarlatina", "infecciosa", "gripe", "sepsis", "erisipela", "hemorrágica"]

keywords_wiki_sida = ["sida", "vih", "hiv", "malaria", "influenza", "tuberculosis", "paludismo", "lepra", "sífilis", "poliomielitis", "onusida", "inmunodeficiencia", "drogadicción", "vacunación", "hepatitis", "dengue", "cáncer", "sarampión", "desnutrición", "varicela", "enfermedad", "brucelosis", "diabetes", "tétanos", "contagio", "seropositivos", "viruela", "gripe", "tabaquismo", "leishmaniasis", "enfermedades"]

keywords_wiki_varicela = ["varicela", "herpes", "zóster", "parotiditis", "paperas", "citomegalovirus", "hepatitis", "rubéola", "gonorrea", "meningitis", "infección", "brucelosis", "gastroenteritis", "zoster", "encefalitis", "neumonías", "sífilis", "toxoplasmosis", "erisipela", "sepsis", "sarampión", "meningoencefalitis", "leptospirosis", "inmunodeficiencia", "candidiasis", "amebiana", "infecciones", "vph", "sinusitis", "sarcoidosis", "estomatitis"]

keywords_wikipedia_es = [keywords_wiki_alzheimer, keywords_wiki_asma, keywords_wiki_cancer, keywords_wiki_caries, keywords_wiki_diabetes, keywords_wiki_ebola, keywords_wiki_gripe, keywords_wiki_hepatitis, keywords_wiki_obesidad, keywords_wiki_otitis, keywords_wiki_resfriado, keywords_wiki_sarampión, keywords_wiki_sida, keywords_wiki_varicela]

# INDEXNAMES
indexname_wiki_ebola = 'twitter_wiki_ebola'
indexname_wiki_gripe = 'twitter_wiki_gripe'
indexname_wiki_resfriado = 'twitter_wiki_resfriado'
indexname_wiki_cancer = 'twitter_wiki_cancer'
indexname_wiki_asma = 'twitter_wiki_asma'
indexname_wiki_hepatitis = 'twitter_wiki_hepatitis'
indexname_wiki_otitis = 'twitter_wiki_otitis'
indexname_wiki_diabetes = 'twitter_wiki_diabetes'
indexname_wiki_caries = 'twitter_wiki_caries'
indexname_wiki_anorexia = 'twitter_wiki_anorexia'
indexname_wiki_obesidad = 'twitter_wiki_obesidad'
indexname_wiki_alzheimer = 'twitter_wiki_alzheimer'
indexname_wiki_sida = 'twitter_wiki_sida'
indexname_wiki_varicela = 'twitter_wiki_varicela'
indexname_wiki_sarampion = 'twitter_wiki_sarampion'
indexname_wiki_apendicitis = 'twitter_wiki_apendicitis'

indexname_wikipedia_es = [indexname_wiki_ebola, indexname_wiki_gripe, indexname_wiki_resfriado, indexname_wiki_cancer, indexname_wiki_asma, indexname_wiki_hepatitis, indexname_wiki_otitis, indexname_wiki_diabetes, indexname_wiki_caries, indexname_wiki_anorexia, indexname_wiki_obesidad, indexname_wiki_alzheimer, indexname_wiki_sida, indexname_wiki_varicela, indexname_wiki_sarampion, indexname_wiki_apendicitis]

keywords_cat_wikipedia_hepatitis= ["hepatitis", "infección","varicela","meningitis","encefalitis","infecciosa","sáfilis","parotiditis","herpes","gonorrea","sèpsia","brucel·losi","endocarditis","galteres","cirrosi","citomegalovirus","rubèola","gastroenteritis","várica","toxoplasmosi","hepatocarcinoma","granulomatosa","malaltia","sinusitis","leptospirosi","sarcoïdosi","meningoencefalitis","sarampión","infeccions","malària","paratifoidea"]

keywords_cat_wikipedia_sida = ["vih","hiv","malària","influença","tuberculosi","paludisme","lepra","sáfilis","poliomielitis","ONUSIDA","immunodeficiència","drogadicción","vacunación","hepatitis","dengue","càncer","sarampión","desnutrición","varicel·la","malaltia","brucel·losi","diabetis","tètanus","contagi","seropositius","verola","grip","tabaquisme","leishmaniosi","malalties"]

keywords_cat_wikipedia_sarampion = ["verola","tifus","diftèria","malària","rubèola","sáfilis","galteres","disenteráa","tuberculosi","meningitis","varicela","tifoide","paludisme","parotiditis","tètanus","hepatitis","poliomielitis","infecció","lepra","encefalitis","brucel·losi","aviària","puerperal","epidèmica","escarlatina","infecciosa","grip","sèpsia","erisipela","hemorràgica"]

keywords_cat_wikipedia_obesidad = ["diabetis","osteoporosi","tabaquisme","cardiovasculars","epilèpsia","mellitus","migranyes","dislipidèmia","hipertensió","asma","sobrepès","desnutrición","migranya","cardiopatáas","hipertiroïdisme","patir","aterosclerosi","hipogonadisme","acne","gastritis","endocarditis","sèpsia","hipotiroïdisme","crónicos","gastrointestinals","artrosi","anorèxia","artritis","osteoartritis"]

keywords_cat_wikipedia_alzheimer = ["parkinson","malaltia","degenerativa","demència","crohn","incurable","sáfilis","neurodegenerativa","tuberculosi","cirrosi","diabetis","moyamoya","neurológica","esquizofrènia","leucèmia","autoimmune","patir","epilèpsia","càncer","malaltia","neumonáa","infecciosa","padecáa","sèpsia","ménière","rubèola","emfisema","diagnosticada","venèria","asma"]

keywords_cat_wikipedia_caries = ["cellulitis","osteoartritis","gastritis","litiasi","indigestión","osteoporosi","psoriasi","periodontals","gingivitis","constipación","amebiasi","hepatoesplenomegalia","dispèpsies","pancitopènia","restrenyiment","pielonefritis","supuración","leucorrea","vaginitis","xerosi","tetània","pericarditis","rinorrea","nefropatáas","cólicos","acalàsia","èczemes","meteorisme","osteoarticulars","hipocalcèmia"]

keywords_cat_wikipedia_varicela = ["herpes","zóster","parotiditis","galteres","citomegalovirus","hepatitis","rubèola","gonorrea","meningitis","infecció","brucel·losi","gastroenteritis","zòster","encefalitis","neumonáas","sáfilis","toxoplasmosi","erisipela","sèpsia","sarampión","meningoencefalitis","leptospirosi","immunodeficiència","candidiasi","amebiana","infeccions","VPH","sinusitis","sarcoïdosi","estomatitis"]

keywords_cat_wikipedia_asma = ["bronquitis","reumatisme","migranyas","gastrointestinals","gastritis","sinusitis","refredats","tos","rinitis","afeccions","gastroenteritis","refredats","conjuntivitis","diarrees","nefritis","icterícia","dismenorrea","epilèpsia","diarrea","artritis","colitis","faringitis","diabetis","hemorràgies","ronquera","hidropesáa","restrenyiment","cardiovasculars","MPOC","hemorroides"]

keywords_cat_wikipedia_gripe = ["influença","h1n1","pandèmia","verola","AH1N1","sarampión","malària","tifus","sáfilis","tuberculosi","aviària","rubèola","paludisme","lepra","tifoide","infecció","varicel·la","neumonáa","meningitis","bubónica","epidèmica","contagi","hepatitis","H5N1","contagiada","disenteráa","dengue","malaltia","infectats","cólera"]

keywords_cat_wikipedia_apendicitis =  ["peritonitis","meningitis","pancreatitis","diverticulitis","descompensada","hemoptisi","colecistitis","infecció","hemorràgia","reumática","neumonáa","artrosi","arítmia","sinusitis","septicèmia","bronquiectasia","nefritis","urèmia","embòlia","pericarditis","sarcoïdosi","endocarditis","cardiopatáa","postoperatori","neurodegenerativa","sèpsia","migranya","osteomielitis","malaltia","isquèmica"]

keywords_cat_wikipedia_otitis = ["sinusitis","faringitis","bronquiectasia","bronquitis","colecistitis","amigdalitis","endocarditis","enteritis","cistitis","purulenta","pancreatitis","sarcoïdosi","epistaxis","gastritis","atrófica","disquinesias","urticària","flebitis","eosinofília","sintomática","hipotiroïdisme","pneumonitis","dismenorrea","uretritis","osteomielitis","artràlgies","litiasi","estomatitis","colitis","hepatobiliars"]

keywords_cat_wikipedia_anorexia = ["bulímia","vómitos","marejos","diarrea","cefalea","náuseas","insomni","restrenyiment","gastrointestinals","náusea","migranyes","dispnea","cefalees","icterícia","dispèpsia","epilèpsia","astènia","naáºseas","cólicos","constipación","palpitacions","irritabilitat","diarrees","migranya","vómito","dismenorrea","asma","rampes","espasmes","miàlgia"]

keywords_cat_wikipedia_cancer = ["health","gastric","chemotherapy","Psychiatric","breast","research","Cardiology","prevention","Oncology","disorders","diseases","humane","surgical","colorectal","pediatrics","humanities","medical","toxicology","Neurological","clinical","aids","preservation","Biomedical","institutes","treatment","palsy","pathology","Epidemiology","Thoracic","interdisciplinary"]

keywords_cat_wikipedia_resfriado = ["refredat","migranyas","refredats","resfráo","reumatisme","gastroenteritis","indigestión","migranya","cólicos","faringitis","sinusitis","empatx","diarrees","asma","diarrea","varicel·la","amebiasi","reuma","bronquitis","amigdalitis","urticària","gonorrea","gastritis","galteres","úlcera","amebiana","neumocócica","dispèpsia","gripals","ferina"]

keywords_cat_wikipedia_diabetes = ["mellitus","obesitat","cardiovasculars","hipertensió","asma","cardiopatáas","osteoporosi","dislipidèmia","tabaquisme","reumatisme","epilèpsia","crohn","meningitis","bronquitis","emfisema","arteriosclerosi","gastroenteritis","cirrosi","anèmia","gastritis","artrosi","cardiovascular","migranyas","malaltia","arítmia","sèpsia","parkinson","MPOC","gastrointestinals","artritis"]

keywords_cat_wikipedia_ebola = ["viruses","mammalian","uptake","corrected","respiratory","inhibition","mediated","Grandparents","limb","peptide","fluorescence","receptors","systemic","mechanisms","sulfate","relationships","leukemia","nested","undergo","deficiency","mitochondrial","aromatic","quantitative","probabilístic","photovoltaic","Pathogens","Pancreatic","activated","propagation","measuring"]

keywords_cat_wikipedia_hepatits = ["hepatitis","meningitis","infecció","parotiditis","VHB","citomegalovirus","VHC","toxoplasmosi","meningococ","galteres","rubèola","rubèola","infeccions","sífilis","influenzae","haemophilus","varicel·la","tifoide","zòster","tuberculosi","virus","Haemophilus","herpes","pneumocòccica","estreptocòccica","meningocòccica","rotavirus","xarampió","tos ferina","pneumococ"]

keywords_wikipedia_cat = [keywords_cat_wikipedia_hepatitis, keywords_cat_wikipedia_sida, keywords_cat_wikipedia_sarampion, keywords_cat_wikipedia_obesidad, keywords_cat_wikipedia_alzheimer, keywords_cat_wikipedia_caries,keywords_cat_wikipedia_varicela, keywords_cat_wikipedia_asma, keywords_cat_wikipedia_gripe, keywords_cat_wikipedia_apendicitis, keywords_cat_wikipedia_otitis, keywords_cat_wikipedia_anorexia, keywords_cat_wikipedia_cancer, keywords_cat_wikipedia_resfriado, keywords_cat_wikipedia_diabetes, keywords_cat_wikipedia_ebola, keywords_cat_wikipedia_hepatits]

indexname_wikipedia_cat_ebola = 'twittercat_wikipedia_ebola'
indexname_wikipedia_cat_gripe = 'twittercat_wikipedia_gripe'
indexname_wikipedia_cat_resfriado = 'twittercat_wikipedia_resfriado'
indexname_wikipedia_cat_cancer = 'twittercat_wikipedia_cancer'
indexname_wikipedia_cat_asma = 'twittercat_wikipedia_asma'
indexname_wikipedia_cat_hepatitis = 'twittercat_wikipedia_hepatitis'
indexname_wikipedia_cat_otitis = 'twittercat_wikipedia_otitis'
indexname_wikipedia_cat_diabetes = 'twittercat_wikipedia_diabetes'
indexname_wikipedia_cat_caries = 'twittercat_wikipedia_caries'
indexname_wikipedia_cat_anorexia = 'twittercat_wikipedia_anorexia'
indexname_wikipedia_cat_obesidad = 'twittercat_wikipedia_obesidad'
indexname_wikipedia_cat_alzheimer = 'twittercat_wikipedia_alzheimer'
indexname_wikipedia_cat_sida = 'twittercat_wikipedia_sida'
indexname_wikipedia_cat_varicela = 'twittercat_wikipedia_varicela'
indexname_wikipedia_cat_sarampion = 'twittercat_wikipedia_sarampion'
indexname_wikipedia_cat_apendicitis = 'twittercat_wikipedia_apendicitis'

indexname_wikipedia_cat = [indexname_wikipedia_cat_ebola, indexname_wikipedia_cat_gripe, indexname_wikipedia_cat_resfriado, indexname_wikipedia_cat_cancer, indexname_wikipedia_cat_asma, indexname_wikipedia_cat_hepatitis, indexname_wikipedia_cat_otitis, indexname_wikipedia_cat_diabetes, indexname_wikipedia_cat_caries, indexname_wikipedia_cat_anorexia, indexname_wikipedia_cat_obesidad, indexname_wikipedia_cat_alzheimer, indexname_wikipedia_cat_sida, indexname_wikipedia_cat_varicela, indexname_wikipedia_cat_sarampion, indexname_wikipedia_cat_apendicitis]

# Embeedings de SBW
keywords_sbw_alzheimer = ["alzheimer", "alzhéimer", "demencia", "parkinson", "esclerosis", "neurodegenerativas", "neurodegenerativa", "demencias", "senil", "enfermedad", "esquizofrenia", "Alzhéimer", "neurodegenerativos", "párkinson", "degenerativa", "autismo", "degenerativas", "diabetes", "invidencia", "neurodegenerativo", "leucemia", "crohn", "fibrosis", "ictus", "amiotrófica", "amiotrofica", "epilepsia", "cáncer", "cancer", "Alzhaimer", "arteriosclerosis"]

keywords_sbw_anorexia = ["anorexia", "bulimia", "vigorexia", "obesidad", "ortorexia", "trastornos", "dismórfico", "dismorfico", "premenstrual", "sobrepeso", "diabetes", "hipertensión", "hipertension", "gastritis", "somatizaciones", "somatomorfo", "psicosomáticos", "psicosomaticos", "dismorfofobia", "trastorno", "distimia", "tabaquismo", "anoréxicas", "anorexicas", "estreñimiento", "febrícula", "febricula", "disfórico", "disforico", "irritabilidad", "alcoholismo", "vómitos", "vomitos", "endometriosis", "esquizofrenia", "comorbilidades", "insomnio", "migrañas"]

keywords_sbw_apendicitis = ["apendicitis", "peritonitis", "hernia", "diverticulitis", "apendicectomía", "apendicectomia", "neumonía", "neumonia", "amigdalitis", "tromboembolia", "reumática", "reumatica", "hemorragia", "pancreatitis", "colecistitis", "pericarditis", "úlcera", "ulcera", "sinusitis", "nefritis", "cardiorrespiratorios", "osteomielitis", "sepsis", "cervicalgia", "bronconeumonía", "bronconeumonia", "miocarditis", "abceso", "hemoptisis", "adenopatía", "adenopatia", "uremia", "bursitis", "absceso", "colangitis", "postoperatorias", "endometritis"]

keywords_sbw_asma = ["asma", "bronquitis", "alergias", "hipertensión", "hipertension", "asmáticos", "asmaticos", "respiratorias", "rinitis", "sinusitis", "bronquial", "obstructiva", "afecciones", "respiratorios", "broncoespasmo", "reumática", "reumatica", "artritis", "pulmonares", "gastritis", "cardiopatías", "cardiopatias", "cardiovasculares", "diabetes", "neumopatías", "neumopatias", "epilepsia", "miocarditis", "tos", "dispepsia", "migrañas", "bronquiolitis", "colitis", "péptica", "peptica", "alérgica", "alergica", "rinoconjuntivitis"]

keywords_sbw_cancer = ["cancer", "cáncer", "colorectal", "mama", "pancreas", "colon", "carcinoma", "breast", "próstata", "prostata", "colorrectal", "neuroblastoma", "metastásico", "metastasico", "tumors", "HPV", "melanoma", "tumor", "tumour", "pneumonia", "leucemia", "prostate", "disease", "espinocelular", "metastasis", "patients", "cystic", "laparoscopic", "hepatocarcinoma", "microcítico", "microcitico", "coronary", "cánceres", "canceres", "carcinoma", "pulmón", "pulmon", "tumor", "páncreas", "linfoma", "cervicouterino", "enfermedad", "tumores", "mieloma", "diabetes", "uterino", "metástasis", "metastasis", "cérvico", "cervico", "quimioterapia", "pancreático", "pancreatico", "cirrosis", "mesotelioma", "mamario", "sarcoma", "hepatocarcinoma", "metastatizado"]

keywords_sbw_caries = ["caries", "gingivitis", "encías", "encias", "periodontales", "periodontitis", "fluorosis", "periodontal", "halitosis", "bucal", "dental", "maloclusión", "maloclusion", "osteoporosis", "dentobacteriana", "dentales", "bucales", "gastrointestinales", "desmineralización", "desmineralizacion", "sarro", "gastritis", "piorrea", "remineralización", "remineralizacion", "bruxismo", "caries", "várices", "ulceras", "biofilm", "pulpitis", "úlceras", "ulceras", "ferropénica", "ferropenica", "ferropenia", "diabetes"]

keywords_sbw_diabetes = ["diabetes", "mellitus", "hipertensión", "hipertension", "cardiovasculares", "obesidad", "osteoporosis", "degenerativas", "enfermedades", "hipercolesterolemia", "cardíacas", "cardiacas", "diabéticos", "diabeticos", "insulinodependiente", "enfermedad", "arterial", "cardiopatías", "cardiopatias", "cardiopatía", "cardiopatia", "infartos", "cardiovascular", "sobrepeso", "dislipidemia", "cirrosis", "diabética", "diabetica", "arteriosclerosis", "padecimiento", "isquémica", "isquemica", "diabéticas", "diabeticas", "arterioesclerosis", "cerebrovasculares", "Diabetes", "artritis"]

keywords_sbw_ebola = ["ébola", "ebola", "gripe", "Lassa", "legionelosis", "leptospirosis", "neumocócica", "neumococica", "epidémico", "epidemico", "pandemia", "meningocócica", "meningococica", "dengue", "exantemático", "exantematico", "influenza", "pandémico", "pandemico", "virus", "chikunguña", "hantavirus", "epidemia", "meningitis", "Chikungunya", "leishmaniasis", "infección", "infeccion", "brote", "hemorrágica", "hemorragica", "contagios", "poliovirus", "aviar", "tularemia", "SARS", "infectada"]

keywords_sbw_gripe = ["gripe", "aviar", "influenza", "ahdigito", "pandémica", "pandemica", "Gripe", "Influenza", "pandemia", "epidémico", "epidemico", "aviaria", "varicela", "virus", "patógena", "patogena", "pandémico", "pandemico", "meningitis", "gripales", "contagios", "aftosa", "gripes", "epidemia", "infección", "infeccion", "salmonelosis", "dengue", "hiperpatógena", "hiperpatogena", "epidémica", "epidemica", "ébola", "hepatitis", "vacuna", "sars", "gripa"]

keywords_sbw_hepatitis = ["hepatitis", "meningitis", "infección", "infeccion", "parotiditis", "VHB", "citomegalovirus", "VHC", "toxoplasmosis", "meningococo", "paperas", "rubéola", "rubeola", "rubeola", "infecciones", "sífilis", "sifilis", "influenzae", "haemophilus", "varicela", "tifoidea", "zóster", "zoster", "tuberculosis", "virus", "Haemophilus", "haemophilus", "herpes", "neumocócica", "neumococica", "estreptocócica", "estreptococica", "meningocócica", "meningococica", "rotavirus", "sarampión", "sarampion", "tosferina", "Neumococo", "neumococo"]

keywords_sbw_obesidad = ["obesidad", "sobrepeso", "diabetes", "hipertensión", "hipertension", "tabaquismo", "sedentarismo", "cardiovasculares", "osteoporosis", "obesos", "mellitus", "hipercolesterolemia", "degenerativas", "anorexia", "mórbida", "morbida", "dislipidemia", "desnutrición", "desnutricion", "bulimia", "enfermedades", "morbilidad", "prediabetes", "Obesidad", "dislipemias", "malnutrición", "malnutricion", "padecimiento", "hiperlipidemia", "ferropénica", "ferropenica", "cardiopatías", "cardipatias", "diabéticos", "diabeticos", "obesas", "prediabéticos", "prediabeticos", "dislipidemias"]

keywords_sbw_otitis = ["otitis", "sinusitis", "conjuntivitis", "faringitis", "osteomielitis", "rinofaringitis", "epistaxis", "bronquiolitis", "amigdalitis", "otorrea", "supuración", "supuracion", "traqueítis", "traqueitis", "queratitis", "neumonías", "neumonias", "candidiasis", "mastoiditis", "bacteremia", "enteritis", "uveítis", "uveitis", "laringotraqueobronquitis", "esplenomegalia", "meningoencefalitis", "colangitis", "sobreinfección", "sobreinfeccion", "endocarditis", "bronquitis", "esclerosante", "eccema2", "neumonitis", "impetigo", "impétigo"]

keywords_sbw_resfriado = ["resfriado", "catarro", "resfrío", "resfrio", "faringitis", "gripa", "bronquitis", "sinusitis", "gripes", "gastroenteritis", "resfriados", "neumonía", "neumonia", "amigdalitis", "tos", "rinofaringitis", "diarrea", "rinitis", "gripales", "catarros", "estreptocócica", "estreptococica", "conjuntivitis", "reumática", "reumatica", "antitérmicos", "antitermicos", "gripe", "ronquera", "vómito", "vomito", "laringitis", "constipado", "anginas", "varicela", "broncoespasmo", "estomacal"]

keywords_sbw_sarampion = ["sarampion", "sarampión", "tétanos", "tetanos", "poliomielitis", "difteria", "rubéola", "rubeola", "paperas", "ferina", "parotiditis", "inmunización", "inminizacion", "tétano", "tetano", "tosferina", "vacunación", "vacunacion", "polio", "meningitis", "pertusis", "antipoliomielítica", "antipoliomelitica", "neumococo", "rotavirus", "inmunizar", "viruela", "DPTDIGITO", "vacunados", "varicela", "hepatitis", "hib", "antitetánica", "antitetanica", "neonatal", "inmunizados", "vacuna"]

keywords_sbw_sida = ["sida", "vih", "tuberculosis", "malaria", "inmunodeficiencia", "seropositivos", "pandemia", "paludismo", "antisida", "epidemia", "inmunodeficiencia", "hepatitis", "onusida", "antiretrovirales", "retrovirales", "antirretrovirales", "cáncer", "cancer", "onusida", "seropositivas", "hiv", "neumocócica", "neumococica", "infecciosas", "infección", "infeccion", "coinfección", "coinfeccion", "infecciones", "antirretroviral", "virus", "antirretrovírico", "antirretrovirico", "multirresistente"]

keywords_sbw_varicela = ["varicela", "meningitis", "zóster", "zoster", "herpes", "bronquiolitis", "hepatitis", "rubeola", "paperas", "sarampión", "sarampion", "rotavirus", "gripales", "infección", "infeccion", "encefalitis", "tosferina", "influenza", "neumonías", "neumonias", "gripe", "rubéola", "rubeola", "parotiditis", "tétano", "tetano", "gripa", "estreptocócica", "estreptococica", "diarrea", "neumocócica", "neumococica", "infecciones", "gastroenteritis", "dengue", "salmonelosis", "toxoplasmosis", "difteria", "ferina"]

keywords_sbw_es = [keywords_sbw_alzheimer, keywords_sbw_anorexia, keywords_sbw_apendicitis, keywords_sbw_asma, keywords_sbw_cancer, keywords_sbw_caries, keywords_sbw_diabetes, keywords_sbw_ebola, keywords_sbw_gripe, keywords_sbw_hepatitis, keywords_sbw_obesidad, keywords_sbw_otitis, keywords_sbw_resfriado, keywords_sbw_sarampion, keywords_sbw_sida, keywords_sbw_varicela]

# INDEXNAMES
indexname_sbw_ebola = 'twitter_sbw_ebola'
indexname_sbw_gripe = 'twitter_sbw_gripe'
indexname_sbw_resfriado = 'twitter_sbw_resfriado'
indexname_sbw_cancer = 'twitter_sbw_cancer'
indexname_sbw_asma = 'twitter_sbw_asma'
indexname_sbw_hepatitis = 'twitter_sbw_hepatitis'
indexname_sbw_otitis = 'twitter_sbw_otitis'
indexname_sbw_diabetes = 'twitter_sbw_diabetes'
indexname_sbw_caries = 'twitter_sbw_caries'
indexname_sbw_anorexia = 'twitter_sbw_anorexia'
indexname_sbw_obesidad = 'twitter_sbw_obesidad'
indexname_sbw_alzheimer = 'twitter_sbw_alzheimer'
indexname_sbw_sida = 'twitter_sbw_sida'
indexname_sbw_varicela = 'twitter_sbw_varicela'
indexname_sbw_sarampion = 'twitter_sbw_sarampion'
indexname_sbw_apendicitis = 'twitter_sbw_apendicitis'

indexname_sbw_es = [indexname_sbw_ebola, indexname_sbw_gripe, indexname_sbw_resfriado, indexname_sbw_cancer, indexname_sbw_asma, indexname_sbw_hepatitis, indexname_sbw_otitis, indexname_sbw_diabetes, indexname_sbw_caries, indexname_sbw_anorexia, indexname_sbw_obesidad, indexname_sbw_alzheimer, indexname_sbw_sida, indexname_sbw_varicela, indexname_sbw_sarampion, indexname_sbw_apendicitis]

# SBW
keywords_cat_sbw_sida = ["VIH","SIDA","Sida","tuberculosi","malària","Immunodeficiència","seropositius","pandèmia","paludisme","antisida","epidèmia","immunodeficiència","hepatitis","Onusida","antiretrovirals","retrovirals","antiretrovirals","càncer","ONUSIDA","seropositives","HIV","pneumocòccica","infeccioses","infecció","coinfecció","infeccions","antiretroviral","virus","antiretrovíric","multiresistent"]

keywords_cat_sbw_cancer = ["càncer", "mama","pròstata","colorectal","leucèmia","pulmó","càncers","melanoma","còlon","tumor","pàncrees","limfoma","carcinoma","cervicouterino","malaltia","cancer","metastàtic","tumors","mieloma","diabetis","uterí","metàstasi","cèrvico","quimioteràpia","pancreàtic","cirrosi","mesotelioma","mamari","sarcoma","hepatocarcinoma","metastatizado"]

keywords_cat_sbw_sarampion = ["tètanus","poliomielitis","diftèria","rubèola","galteres","ferina","parotiditis","immunització","rubèola","tètan","tos ferina","vacunació","pòlio","meningitis","pertussis","antipoliomielítica","pneumococ","rotavirus","immunitzar","verola","DPTDIGITO","vacunats","varicel·la","xarampió","hepatitis","Hib","antitetànica","neonatal","immunitzats","vacuna"]

keywords_cat_sbw_obesidad = ["sobrepès","diabetis","hipertensió","tabaquisme","sedentarisme","cardiovasculars","osteoporosi","obesos","mellitus","hipercolesterolèmia","degeneratives","anorèxia","mòrbida","dislipidèmia","desnutrició","bulímia","malalties","morbiditat","prediabetis","obesitat","dislipèmies","malnutrició","patiment","hiperlipidèmia","ferropènica","cardiopaties","diabètics","obeses","prediabètics","dislipidèmies"]

keywords_cat_sbw_alzheimer = ["Alzheimer","Parkinson","Alzheimer","demència","parkinson","esclerosi","neurodegeneratives","neurodegenerativa","demències","senil","malaltia","esquizofrènia","alzheimer","neurodegeneratius","Parkinson","degenerativa","autisme","degeneratives","diabetis","invidència","neurodegeneratiu","leucèmia","Crohn","fibrosi","ictus","amiotròfica","epilèpsia","càncer","Alzheimer","arteriosclerosi"]

keywords_cat_sbw_caries = ["gingivitis","genives","periodontals","periodontitis","fluorosi","periodontal","halitosi","bucal","dental","maloclusió","osteoporosi","dentobacteriana","dentals","bucals","gastrointestinals","desmineralització","tosca","gastritis","piorrea","remineralització","bruxisme","Carles","varius","úlceres","biofilm","pulpitis","úlceres","ferropènica","ferropènia","diabetis"]

keywords_sbw_cat_varicela = ["meningitis","zòster","herpes","bronquiolitis","hepatitis","rubèola","galteres","xarampió","rotavirus","gripals","infecció","encefalitis","tos ferina","influença","pneumònies","grip","rubèola","parotiditis","tètan","gripa","estreptocòccica","diarrea","pneumocòccica","infeccions","gastroenteritis","dengue","salmonel·losi","toxoplasmosi","diftèria","ferina"]

keywords_cat_sbw_asma = ["bronquitis","al·lèrgies","hipertensió","asmàtics","respiratòries","rinitis","sinusitis","bronquial","obstructiva","afeccions","respiratoris","broncoespasme","reumàtica","artritis","pulmonars","gastritis","cardiopaties","cardiovasculars","diabetis","pneumopaties","epilèpsia","miocarditis","tos","dispèpsia","migranyes","bronquiolitis","colitis","pèptica","al·lèrgica","rinoconjuntivitis"]

keywords_cat_sbw_gripe = ["aviària","influença","AHDIGITO","pandèmica","grip","influenza","pandèmia","epidèmic","aviària","varicel·la","virus","patògena","influença","pandèmic","meningitis","gripals","contagis","aftosa","grips","epidèmia","infecció","salmonel·losi","dengue","hiperpatógena","epidèmica","ebola","hepatitis","vacuna","SARS","gripa"]

keywords_cat_sbw_apendicitis = ["peritonitis","hèrnia","diverticulitis","apendicectomia","pneumònia","amigdalitis","tromboembòlia","reumàtica","hemorràgia","pancreatitis","colecistitis","pericarditis","úlcera","sinusitis","nefritis","cardiorespiratoris","osteomielitis","sèpsia","cervicàlgia","broncopneumònia","miocarditis","abscés","hemoptisi","adenopatia","urèmia","bursitis","abscés","colangitis","postoperatòries","endometritis"]

keywords_cat_sbw_otitis = ["sinusitis","otitis","conjuntivitis","faringitis","osteomielitis","rinofaringitis","epistaxis","bronquiolitis","amigdalitis","otorrea","supuració","traqueïtis","queratitis","pneumònies","candidiasi","mastoïditis","bacteremia","enteritis","uveïtis","laringotraqueobronquitis","esplenomegàlia","meningoencefalitis","colangitis","sobreinfecció","endocarditis","bronquitis","esclerosant","èczema","pneumonitis","impetigen"]

keywords_cat_sbw_anorexia = ["bulímia","vigorèxia","obesitat","ortorèxia","trastorns","dismórfico","premenstrual","sobrepès","diabetis","hipertensió","gastritis","somatitzacions","somatomorf","psicosomàtics","dismorfofòbia","trastorn","distímia","tabaquisme","anorèxiques","restrenyiment","febrícula","disfòric","irritabilitat","alcoholisme","vòmits","endometriosi","esquizofrènia","comorbiditats","insomni","migranyes"]


keywords_cat_sbw_resfriado = ["refredat","refredat","faringitis","gripa","bronquitis","sinusitis","grips","gastroenteritis","refredats","pneumònia","amigdalitis","tos","rinofaringitis","diarrea","rinitis","gripals","refredats","estreptocòccica","conjuntivitis","reumàtica","antitèrmics","grip","ronquera","vòmit","laringitis","constipat","angines","varicel·la","broncoespasme","estomacal"]

keywords_cat_sbw_diabetes = ["mellitus","hipertensió","cardiovasculars","obesitat","osteoporosi","degeneratives","malalties","hipercolesterolèmia","cardíaques","cardíaques","diabètics","insulinodependent","malaltia","arterial","cardiopaties","cardiopatia","infarts","cardiovascular","sobrepès","dislipidèmia","cirrosi","diabètica","arteriosclerosi","patiment","isquèmica","diabètiques","arteriosclerosi","cerebrovasculars","diabetis","artritis"]

keywords_cat_sbw_ebola = ["ébola","ebola","grip","Lassa","legionel·losi","leptospirosi","pneumocòccica","epidèmic","pandèmia","meningocòccica","dengue","exantemàtic","influença","pandèmic","virus","chikungunya","hantavirus","epidèmia","meningitis","chikungunya","leishmaniosi","infecció","brot","hemorràgica","contagis","poliovirus","aviària","tularèmia","sars","infectada"]

keywords_cat_sbw_hepatitis  = ["hepatitis","meningitis","infecció","parotiditis","VHB","citomegalovirus","VHC","toxoplasmosi","meningococ","galteres","rubèola","rubèola","infeccions","sífilis","influenzae","haemophilus","varicel·la","tifoide","zòster","tuberculosi","virus","Haemophilus","herpes","pneumocòccica","estreptocòccica","meningocòccica","rotavirus","xarampió","tos ferina","pneumococ"]

keywords_sbw_cat = [keywords_cat_sbw_sida, keywords_cat_sbw_cancer, keywords_cat_sbw_sarampion, keywords_cat_sbw_obesidad, keywords_cat_sbw_alzheimer, keywords_cat_sbw_caries, keywords_sbw_cat_varicela, keywords_cat_sbw_asma, keywords_cat_sbw_gripe, keywords_cat_sbw_apendicitis, keywords_cat_sbw_otitis, keywords_cat_sbw_anorexia, keywords_cat_sbw_resfriado, keywords_cat_sbw_diabetes, keywords_cat_sbw_ebola, keywords_cat_sbw_hepatitis]


indexname_sbw_cat_ebola = 'twittercat_sbw_ebola'
indexname_sbw_cat_gripe = 'twittercat_sbw_gripe'
indexname_sbw_cat_resfriado = 'twittercat_sbw_resfriado'
indexname_sbw_cat_cancer = 'twittercat_sbw_cancer'
indexname_sbw_cat_asma = 'twittercat_sbw_asma'
indexname_sbw_cat_hepatitis = 'twittercat_sbw_hepatitis'
indexname_sbw_cat_otitis = 'twittercat_sbw_otitis'
indexname_sbw_cat_diabetes = 'twittercat_sbw_diabetes'
indexname_sbw_cat_caries = 'twittercat_sbw_caries'
indexname_sbw_cat_anorexia = 'twittercat_sbw_anorexia'
indexname_sbw_cat_obesidad = 'twittercat_sbw_obesidad'
indexname_sbw_cat_alzheimer = 'twittercat_sbw_alzheimer'
indexname_sbw_cat_sida = 'twittercat_sbw_sida'
indexname_sbw_cat_varicela = 'twittercat_sbw_varicela'
indexname_sbw_cat_sarampion = 'twittercat_sbw_sarampion'
indexname_sbw_cat_apendicitis = 'twittercat_sbw_apendicitis'

indexname_sbw_cat = [indexname_sbw_cat_ebola, indexname_sbw_cat_gripe, indexname_sbw_cat_resfriado, indexname_sbw_cat_cancer, indexname_sbw_cat_asma, indexname_sbw_cat_hepatitis, indexname_sbw_cat_otitis, indexname_sbw_cat_diabetes, indexname_sbw_cat_caries, indexname_sbw_cat_anorexia, indexname_sbw_cat_obesidad, indexname_sbw_cat_alzheimer, indexname_sbw_cat_sida, indexname_sbw_cat_varicela, indexname_sbw_cat_sarampion, indexname_sbw_cat_apendicitis]

if (localizacion=='Madrid'):
	GEOBOX = [-4.3763,40.0642,-3.0508,40.8438]
	LOCATION = "40.41, -3.70"
elif (localizacion=='Barcelona'):
	GEOBOX = [0.5,41.04,3.07,42.18]
	LOCATION = "41.38, 2.16"
elif (localizacion=='Sevilla'):
	GEOBOX = [-6.95,36.99,-5.12,37.8]
	LOCATION = "37.39, -5.95"
elif (localizacion=='Bilbao'):
	GEOBOX = [-4.19,42.59,-1.89,43.72]
	LOCATION = "43.26, -2.93"
elif (localizacion=='Valencia'):
	GEOBOX = [-1.65,38.77,0.92,40.42]
	LOCATION = "39.45, -0.35"
elif (localizacion=='Málaga'):
	GEOBOX = [-5.434,36.4285,-3.6057,37.2511]
	LOCATION = "36.75, -4.39"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# Create Elasticsearch engine and then an Index to save the same
es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])
#es.indices.create(index=indexname, ignore=400)

mapping = {
	"mappings": {
            "tweet": {
                "properties": {
                    "created_at": {
		                "format": "EEE MMM dd HH:mm:ss Z YYYY",
		                "type": "date"
		            },
		            "id": {
		                "type": "long"
		            },
		            "id_str": {
		                "type": "string"
		            },
		            "lang": {
		                "type": "string"
		            },
                    "timestamp_ms": {
                        "type": "date"
                    },                    
                    "loc": {
                        "type": "geo_point"
                    },
                    "text": {
		                "type": "string"
		            },
		            "hts": {
		                "type": "string"
					},
					"disease":{
						"type": "string"
					},					
					"tokens":{
						"type": "string"
					},
					"city":{
						"type": "string"
					}
                }
            }
    }
}

# Creo todos los índices
for indexname in indexname_basic_es:
	exist = es.indices.exists(indexname)
	if not(exist):
		es.indices.create(index=indexname, ignore=400, body=mapping)

for indexname in indexname_basic_cat:
	exist = es.indices.exists(indexname)
	if not(exist):
		es.indices.create(index=indexname, ignore=400, body=mapping)

for indexname in indexname_wikipedia_es:
	exist = es.indices.exists(indexname)
	if not(exist):
		es.indices.create(index=indexname, ignore=400, body=mapping)

for indexname in indexname_wikipedia_cat:
	exist = es.indices.exists(indexname)
	if not(exist):
		es.indices.create(index=indexname, ignore=400, body=mapping)

for indexname in indexname_sbw_es:
	exist = es.indices.exists(indexname)
	if not(exist):
		es.indices.create(index=indexname, ignore=400, body=mapping)

for indexname in indexname_sbw_cat:
	exist = es.indices.exists(indexname)
	if not(exist):
		es.indices.create(index=indexname, ignore=400, body=mapping)

spanish_stopwords = stopwords.words('spanish')
catalan_stopwords = get_stop_words('ca')

class StreamApi(tweepy.StreamListener):
	status_wrapper = TextWrapper(width=60, initial_indent='	', subsequent_indent='	')	

	def on_status(self, status):
		str_tweet_info = json.dumps(status._json)
		json_data = json.loads(str_tweet_info)

		tweet = json_data["text"]
		lang = json_data["lang"]
		if (lang == 'und'):
			try:
				lang = detect(tweet)
			except:
				lang = 'error'

		# Filtro los tweets si tienen las keywords y es en español o catalán...
		if (lang == 'es' or lang == 'ca'):
			# Hashtags
			hts = []
			tweetfilter = ''.join(filter(lambda x: x in string.printable, tweet))
			for ht in tweetfilter.split(' '):
				if (ht.startswith('#')):
					hts.append(ht.strip(','))

			# Tokens
			tweet_tokenizer = TweetTokenizer()
			tokens = tweet_tokenizer.tokenize(tweet)
			punctuations = string.punctuation

			if (lang == 'ca'):
				stopwords_and_punctuations = set(catalan_stopwords) | set(punctuations)
				keywords_basic = keywords_basic_cat
				indexname_basic = indexname_basic_cat

				keywords_wikipedia = keywords_wikipedia_cat
				indexname_wikipedia = indexname_wikipedia_cat

				keywords_sbw = keywords_sbw_cat
				indexname_sbw = indexname_sbw_cat
			else:
				stopwords_and_punctuations = set(spanish_stopwords) | set(punctuations)
				keywords_basic = keywords_basic_es
				indexname_basic = indexname_basic_es

				keywords_wikipedia = keywords_wikipedia_es
				indexname_wikipedia = indexname_wikipedia_es

				keywords_sbw = keywords_sbw_es
				indexname_sbw = indexname_sbw_es

			tokens_without_stopwords_and_punctuations = []
			for token in tokens:
				token = token.lower() 
				if token not in stopwords_and_punctuations:
					tokens_without_stopwords_and_punctuations.append(token)

			# BASIC
			counter = 0
			for keywords in keywords_basic:
				if any(word in tweet.split() for word in keywords):
					doc1 = {
					    "created_at": json_data["created_at"],
					    "id": json_data["id"],
					    "id_str": json_data["id_str"],
					    "lang": json_data["lang"],
					    "timestamp_ms": datetime.now(),
					    "loc": LOCATION,
					    "text": tweet,
					    "hts": hts,
					    "disease": keywords[0],
					    "tokens": tokens_without_stopwords_and_punctuations,
					    "city": localizacion
					}
					es.index(index=indexname_basic[counter], doc_type="twitter", body=doc1, ignore=400)
				counter = counter+1


			# WIKIPEDIA				
			counter = 0
			for keywords in keywords_wikipedia:
				if any(word in tweet.split() for word in keywords):
					doc1 = {
						    "created_at": json_data["created_at"],
						    "id": json_data["id"],
						    "id_str": json_data["id_str"],
						    "lang": json_data["lang"],
						    "timestamp_ms": datetime.now(),
						    "loc": LOCATION,
						    "text": tweet,
						    "hts": hts,
						    "disease": keywords[0],
						    "tokens": tokens_without_stopwords_and_punctuations,
					    	"city": localizacion
					}
					es.index(index=indexname_wikipedia[counter], doc_type="twitter", body=doc1, ignore=400)
				counter = counter+1

				# SBW
				counter = 0
				for keywords in keywords_sbw:
					if any(word in tweet.split() for word in keywords):
						doc1 = {
						    "created_at": json_data["created_at"],
						    "id": json_data["id"],
						    "id_str": json_data["id_str"],
						    "lang": json_data["lang"],
						    "timestamp_ms": datetime.now(),
						    "loc": LOCATION,
						    "text": tweet,
						    "hts": hts,
						    "disease": keywords[0],
						    "tokens": tokens_without_stopwords_and_punctuations,
					    	"city": localizacion
						}
						es.index(index=indexname_sbw[counter], doc_type="twitter", body=doc1, ignore=400)
					counter = counter+1

		time.sleep(10)

	def on_error(self, status_code):
		print('Error encontrado con código:', status_code)
		time.sleep(200)
		return True
		print("Stream restarted")

while True:
	try:
		streamer = tweepy.Stream(auth=auth, listener=StreamApi(), timeout=30)
		# searching and filtering
		streamer.filter(locations=GEOBOX, async=False)
	except IncompleteRead:
		# Oh well, reconnect and keep trucking
		time.sleep(200)
		continue
	except ProtocolError:
		# Oh well, reconnect and keep trucking
		time.sleep(200)
		continue
	except KeyboardInterrupt:
		# Or however you want to exit this loop
		streamer.disconnect()
		break
