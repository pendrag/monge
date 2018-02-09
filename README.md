# monge
Monitor geográfico de enfermedades

Las redes sociales se han convertido en un medio de comunicación personal esencial en cualquier aspecto, incluyendo malestares y enfermedades. El procesamiento y la explotación de dicha información, aplicando las TLH, supone un gran avance y permite mostrar información procesada en un formato visual. Monge aplica estas técnicas y herramientas, y muestra al mundo esta información procesada, y en tiempo real.

El uso de la información publicada en medios sociales permite grandes avances en el seguimiento de enfermedades y en la generación de alarmas médicas, aunque quedan algunos retos por resolver. Actualmente no existe un sistema en español similar que haga uso de la red social Twitter.

Monge es un prototipo de un monitor geográfico de enfermedades basado en tweets. Recuperando tweets localizados en distintas ciudades españolas, tanto en español como en catalán, y procesando y analizando la información con técnicas y herramientas de Tecnologías del Lenguaje Humano (TLH) permite predecir posibles brotes epidémicos de distintas enfermedades de interés general (gripe, cáncer, asma, etc.). 

A partir de distintas bolsas de palabras utilizando sinónimos de WordReference, embeddings creados a partir de Wikipedia en español (Arturo Montejo-Ráez et al. Proceedings of TASS 2016) y embeddings creados a partir del Spanish Billion Word Corpus (http://crscardellino.me/SBWCE/), realizamos consultas en tiempo real en Twitter, procesamos los tweets obtenidos aplicando TLH, filtrando por localización y almacenando dichos datos en ElasticSearch. Por último, mostramos los datos procesados en una interfaz visual con distintos widgets.

Si bien el uso léxico de las bolsas de palabras es un recurso más utilizado en TLH, un recurso muy novedoso en este sentido es el uso de word embeddings. Desde un punto de vista semántico, podemos obtener palabras relacionadas con cada enfermedad, utilizando para esto corpus de distintos orígenes.
