import tweepy
import sys
import json
import re
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime 
from elasticsearch import Elasticsearch 

# Valores de cada índice
keywords_ebola = ["ebola", "ébola"]
keywords_gripe = ["gripe", "trancazo", "influenza"]
keywords_resfriado = ["resfriado", "catarro", "constipado", "enfriamiento", "resfriamiento", "romadizo"]
keywords_cancer = ["cáncer", "cancer", "tumor", "carcinoma", "granuloma", "epitelioma", "sarcoma", "neoplasia", "cefaloma"]
keywords_asma = ["asma", "disnea", "sofoco", "asfixia", "ahogo"]
keywords_hepatitis = ["hepatitis"]
keywords_otitis= ["otitis"]
keywords_diabetes = ["diabetes" "glucosuria"]
keywords_caries = ["caries", "picadura", "úlcera", "perforación", "horadación"]
keywords_anorexia = ["anorexia", "desgana", "inapetencia"]
keywords_obesidad = ["obesidad", "corpulencia", "gordura", "adiposidad", "humanidad", "grosor"]
keywords_alzheimer = ["alzheimer"]
keywords_sida = ["sida", "vih"]
keywords_varicela = ["varicela"]
keywords_sarampion = ["sarampion", "sarampión"]
keywords_apendicitis = ["apendicitis"]

indexname_ebola = 'twitter-ebola'
indexname_gripe = 'twitter-gripe'
indexname_resfriado = 'twitter-resfriado'
indexname_cancer = 'twitter-cancer'
indexname_asma = 'twitter-asma'
indexname_hepatitis = 'twitter-hepatitis'
indexname_otitis = 'twitter-otitis'
indexname_diabetes = 'twitter-diabetes'
indexname_caries = 'twitter-caries'
indexname_anorexia = 'twitter-anorexia'
indexname_obesidad = 'twitter-obesidad'
indexname_alzheimer = 'twitter-alzheimer'
indexname_sida = 'twitter-sida'
indexname_varicela = 'twitter-varicela'
indexname_sarampion = 'twitter-sarampion'
indexname_apendicitis = 'twitter-apendicitis'

localizacion=sys.argv[1]

if (localizacion=='madrid'):
	GEOBOX = [-4.3763,40.0642,-3.0508,40.8438]
	LOCATION = "40.41, -3.70"	
elif (localizacion=='barcelona'):
	GEOBOX = [0.5,41.04,3.07,42.18]
	LOCATION = "41.38, 2.16"
elif (localizacion=='sevilla'):
	GEOBOX = [-6.95,36.99,-5.12,37.8]
	LOCATION = "37.39, -5.95"
elif (localizacion=='barcelona'):
	GEOBOX = [-4.19,42.59,-1.89,43.72]
	LOCATION = "43.26, -2.93"
elif (localizacion=='barcelona'):
	GEOBOX = [-1.65,38.77,0.92,40.42]
	LOCATION = "39.45, -0.35"
elif (localizacion=='barcelona'):
	GEOBOX = [-5.434,36.4285,-3.6057,37.2511]
	LOCATION = "36.75, -4.39"

# Create authentication via Oauth2 twitter
consumer_key = 'vL6P3Os6WC2apkRX7OkkESy3w' 
consumer_secret = 'QjZbAJZb7X0DAbfFSKTsahTxnE7bZyygcbH52hP6JYiUGltWyi' 
access_token = '264311475-p9QtIPEa7VfKpR0LCoyYYk8StStRQetryLu1LQrV' 
access_secret = '9AACyHDcdnEOJak6RszdnEdQ79wCEK5wScZRRmV8k2tZi' 

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
		            }
                }
            }
    }
}

es.indices.create(index=indexname_ebola, ignore=400, body=mapping)
es.indices.create(index=indexname_gripe, ignore=400, body=mapping)
es.indices.create(index=indexname_resfriado, ignore=400, body=mapping)
es.indices.create(index=indexname_cancer, ignore=400, body=mapping)
es.indices.create(index=indexname_asma, ignore=400, body=mapping)
es.indices.create(index=indexname_hepatitis, ignore=400, body=mapping)
es.indices.create(index=indexname_otitis, ignore=400, body=mapping)
es.indices.create(index=indexname_diabetes, ignore=400, body=mapping)
es.indices.create(index=indexname_caries, ignore=400, body=mapping)
es.indices.create(index=indexname_anorexia, ignore=400, body=mapping)
es.indices.create(index=indexname_obesidad, ignore=400, body=mapping)
es.indices.create(index=indexname_alzheimer, ignore=400, body=mapping)
es.indices.create(index=indexname_sida, ignore=400, body=mapping)
es.indices.create(index=indexname_varicela, ignore=400, body=mapping)
es.indices.create(index=indexname_sarampion, ignore=400, body=mapping)
es.indices.create(index=indexname_apendicitis, ignore=400, body=mapping)


class StreamApi(tweepy.StreamListener):
	status_wrapper = TextWrapper(width=60, initial_indent='	', subsequent_indent='	')	

	def on_data(self, data):
		json_data = json.loads(data)

		tweet = json_data["text"]
		lang = json_data["lang"]

		# Filtro los tweets si tienen las keywords y es en español
		if (lang=='es'):
			if (re.compile('|'.join(keywords_apendicitis),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_apendicitis, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_sarampion),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_sarampion, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_varicela),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_varicela, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_sida),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_sida, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_alzheimer),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_alzheimer, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_obesidad),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_obesidad, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_anorexia),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_anorexia, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_caries),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_caries, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_diabetes),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_diabetes, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_otitis),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_otitis, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_hepatitis),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_hepatitis, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_asma),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_asma, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_cancer),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_cancer, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_resfriado),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_resfriado, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_gripe),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_gripe, doc_type="twitter", body=doc1, ignore=400)
			elif (re.compile('|'.join(keywords_ebola),re.IGNORECASE).search(tweet)):
				doc1 = {
				    "created_at": json_data["created_at"],
				    "id": json_data["id"],
				    "id_str": json_data["id_str"],
				    "lang": json_data["lang"],
				    "timestamp_ms": datetime.now(),
				    "loc": LOCATION,
				    "text": tweet			    
				}
				es.index(index=indexname_ebola, doc_type="twitter", body=doc1, ignore=400)
		

streamer = tweepy.Stream(auth=auth, listener=StreamApi(), timeout=30)

# searching and filtering
streamer.filter(locations=GEOBOX, async=False)
