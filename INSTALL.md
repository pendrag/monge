1. Instalar ELK (ElasticSearch, Logstash y Kibana)

    1.1. Instalar Java JDK

>> Para instalar JDK añadiremos el repositorio ppa, actualizaremos repositorios e instalaremos java, para ellos ejecutaremos:  

```bash
add-apt-repository ppa:webupd8team/java  
apt-get update  
apt-get install oracle-java8-installer  
java -version  
```

- Instalar Elasticsearch
Elasticsearch es un motor de búsqueda y análisis distribuido, para instalarlo añadiremos el repositorio de Elastic y procederemos con la instalación:  
 wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -  
 echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list  
 apt-get update  
 apt-get install elasticsearch     
 systemctl start elasticsearch  
 systemctl enable elasticsearch  

- Instalar Kibana
Kibana te permite explorar, visualizar o descubrir datos. Además podemos obtener gráficas o colocar datos geográficos en cualquier mapa, para instalar Kibana:  
apt-get install kibana  

Como Kibana corre sobre un servidor web, necesitaremos tener instalado un servidor web (Apache, nginx, etc.)

- Instalar Logstash
Logstash nos permite centralizar, transformar y almacenar nuestros datos. En el siguiente artículo os enseñamos más ejemplos de filtros. Para instalar Logstash ejecutaremos:  
apt-get install logstash  
systemctl start logstash  
systemctl enable logstash  

2. Instalar python
Para los distintos scripts necesitaremos tener instalado Python, en su versión 3 o superior  
sudo apt-get install python3.4  

3. Instalar librerías
Algunos scripts de python hacen uso de librerías, y si no las tenemos instaladas al lanzarlo nos lo indicará y habrá que instalarlas, tal como tweepy, nltk, gensim, googletrans, langdetect, stop_words, textwrap, elasticsearch  
pip install tweepy  
pip install nltk  
pip install gensim  
pip install googletrans  
pip install langdetect  
pip install stop_words  
pip install textwrap  
pip install elasticsearch  
