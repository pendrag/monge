# uso: translate_ES_CA_bag_of_words.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author Jiménez Zafra, Salud María 
@author Plaza del Arco, Flor Miriam
@author García Cumbreras, Miguel Ángel
@created_at enero 2018
'''

import os
from googletrans import Translator


def translate_module():

	translator = Translator()


	path_es = "../../sjzafra/bag_of_words"
	path_cat = "/home/fmplaza/monge"
	

	for directory in os.listdir(path_es):
		if not os.path.exists(directory):
			os.makedirs(directory)
		path_folder_es = os.path.join(path_es, directory)

		for file_es in os.listdir(path_folder_es):
			listWordsEs = []
			file_read = open(str(os.path.join(path_folder_es, file_es)))
			for line in file_read:
				listWordsEs.append(line)
			file_cat = os.path.join(path_cat, directory, file_es)
			if(not os.path.exists(file_cat)):
				with open(file_cat, 'w') as output_file:
					for word in listWordsEs:
						print(word)
						word_cat = translator.translate(word, src='es',  dest='ca').text
						line = word_cat + "\n"
						output_file.write(line)
				output_file.close()


if __name__ == "__main__":

	translate_module()
	
