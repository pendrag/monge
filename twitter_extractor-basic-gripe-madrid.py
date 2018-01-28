import tweepy
import sys
import json
import re
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime 
from elasticsearch import Elasticsearch 

# Valores de cada índice
keywords = ["gripe", "trancazo", "influenza", "resfriado", "catarro", "enfriamiento"]
indexname = 'twitter-basic-gripe-madrid'

GEOBOX = [-4.3763,40.0642,-3.0508,40.8438]
LOCATION = "40.41, -3.70"

# GEOBOX_BARCELONA = []
# GEOBOX_SEVILLA = []
# GEOBOX_BILBAO = []
# GEOBOX_VALENCIA = []
# GEOBOX_MALAGA = []

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

es.indices.create(index=indexname, ignore=400, body=mapping)

class StreamApi(tweepy.StreamListener):
	status_wrapper = TextWrapper(width=60, initial_indent='	', subsequent_indent='	')	

	def on_data(self, data):
		json_data = json.loads(data)

		tweet = json_data["text"]
		lang = json_data["lang"]

		#print("lang:%s" % lang)

		# Filtro los tweets si tienen las keywords y es en español
		if (lang=='es') and (re.compile('|'.join(keywords),re.IGNORECASE).search(tweet)):
			#print("Entro. Tweet:%s" % tweet)

			doc1 = {
			    "created_at": json_data["created_at"],
			    "id": json_data["id"],
			    "id_str": json_data["id_str"],
			    "lang": json_data["lang"],
			    "timestamp_ms": datetime.now(),
			    "loc": LOCATION,
			    "text": tweet			    
			}

			es.index(index=indexname, doc_type="twitter", body=doc1, ignore=400)
		#return True

streamer = tweepy.Stream(auth=auth, listener=StreamApi(), timeout=30)

# searching and filtering
#streamer.filter(languages=['es'], track=keywords)
streamer.filter(locations=GEOBOX, async=False)
