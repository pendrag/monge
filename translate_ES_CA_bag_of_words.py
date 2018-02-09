# Usage: python3 translate_ES_CA_bag_of_words.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author SINAI, Universidad de Jaén
@created_at enero 2018
'''
import sys
import codecs
import argparse
import os
from googletrans import Translator
import time


def translate_bags_of_words_to_catalan(input_dir_es, output_dir_ca):

	translator = Translator()

	for directory in os.listdir(input_dir_es):
		output_dir_ca_model = os.path.join(output_dir_ca, directory)
		if not os.path.exists(output_dir_ca_model):
			os.makedirs(output_dir_ca_model)
		path_folder_es = os.path.join(input_dir_es, directory)

		for file_es in os.listdir(path_folder_es):
			listWordsEs = []
			file_read = open(os.path.join(path_folder_es, file_es), 'r', encoding='latin-1')
			for line in file_read:
				listWordsEs.append(line)
			file_cat = os.path.join(output_dir_ca_model, file_es)
			
			with open(file_cat, 'w') as output_file:
				for word in listWordsEs:
					try:
						word_cat = translator.translate(word, src='es',  dest='ca').text
						line = word_cat + "\n"
						output_file.write(line)
						time.sleep(5)
					except:
						time.sleep(10)
						continue

if __name__ == '__main__':
	
	# Set sys.stdout encoding	
	sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
	
	# Parser for command line options
	parser = argparse.ArgumentParser(description='Translate bag of words to catalan')
	parser.add_argument('-i','--input_dir', help='Directory with the bags of words to be translated', required=True)
	parser.add_argument('-o','--output_dir', help='Directory to save the translated bags of words', required=True)
	
	# Parse the command line options
	args = parser.parse_args()
	input_dir_es = args.input_dir
	output_dir_ca = args.output_dir

	# Translate bags of words
	translate_bags_of_words_to_catalan(input_dir_es, output_dir_ca)
	
