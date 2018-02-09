# -*- coding: utf-8 -*-
# Example of use: python3 generate_bag_of_words_using_word_embeddings.py -s ../seeds.txt -m ../word2vec_models/SBW-vectors-300-min5.bin.gz -f binary -n 30 -o ../bag_of_words
'''
Created on 22/01/2018

@author: SINAI, Universidad de Jaén
'''
import sys
import codecs
import argparse
import gensim
import os

def get_seeds_list(seeds_file):
	seeds_list = []
	with open(seeds_file, 'r') as f:
		lines = f.readlines()
		for line in lines:
			seeds_list.append(line.strip())
	
	return seeds_list

def save_bag_of_words_most_similar(tuple_list, seed, output_dir):
	output_file = os.path.join(output_dir, seed + '.txt')
	with open(output_file, 'w') as f:
		for word, similarity in tuple_list:
			f.write(word + '\n')
				

if __name__ == '__main__':
	
	# Set sys.stdout encoding	
	sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
	
	# Parser for command line options
	parser = argparse.ArgumentParser(description='Generate bags of words with the most similar words to the given seeds using a Word2Vec model')
	parser.add_argument('-s','--seeds_file', help='File with the seeds that are going to be used to generate the bags of words', required=True)
	parser.add_argument('-m','--model', help='Word2Vec model file', required=True)
	parser.add_argument('-f','--model_format', help='Format of the model: binary format or text format', required=True)
	parser.add_argument('-n','--topn', help='Top n most similar words to find (default 10)', required=False)
	parser.add_argument('-o','--output_dir', help='Directory to save the generated bags of words', required=True)
	
	# Parse the command line options
	print('Parsing command line options...')
	args = parser.parse_args()
	seeds_file = args.seeds_file
	word2vec_model_file = args.model
	if (args.model_format == 'binary'):
		binary_format = True
	else:
		binary_format = False
	topn = 10
	if (args.topn):
		topn = int(args.topn)
	output_dir = args.output_dir
		
	# Get the list of seeds
	print('Reading list of seeds...')
	seeds_list = get_seeds_list(seeds_file)
	
	# Get the most similar words to the given seeds using a Word2Vec model and save them	
	model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_file, binary=binary_format)
	for seed in seeds_list:
		if seed in model.wv.vocab:
			print('Getting the most similar words to ' + seed)
			tuple_list = model.most_similar(positive=[seed], topn=topn)
			save_bag_of_words_most_similar(tuple_list, seed, output_dir)
