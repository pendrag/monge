# -*- coding: utf-8 -*-
# Example of use: python3 get_most_similar_words.py -w gripe -m ../word2vec_models/SBW-vectors-300-min5.bin.gz -f binary -n 10
'''
Created on 18/01/2018

@author: Salud María Jiménez Zafra
'''
import sys
import codecs
import argparse
import gensim

if __name__ == '__main__':
	
	# Set sys.stdout encoding	
	sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
	
	# Parser for command line options
	parser = argparse.ArgumentParser(description='Get the most similar words to the given word using a Word2Vec model')
	parser.add_argument('-w','--word', help='Word from which you want to fin the most simialr words', required=True)
	parser.add_argument('-m','--model', help='Word2Vec model file', required=True)
	parser.add_argument('-f','--model_format', help='Format of the model: binary format or text format', required=True)
	parser.add_argument('-n','--topn', help='Top n most similar words to find (default 10)', required=False)
	
	# Parse the command line options
	args = parser.parse_args()
	word = args.word
	word2vec_model_file = args.model
	if (args.model_format == 'binary'):
		binary_format = True
	else:
		binary_format = False
	topn = 10
	if (args.topn):
		topn = int(args.topn)
	
	# Get the most similar words to the given word using a Word2Vec model
	model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_model_file, binary=binary_format)
	print('Getting ' + str(topn) + ' most similar words to the word ' + word)
	tuple_list = model.most_similar(positive=[word], topn=topn)
	print('Most similar words using cosine similarity between a simple mean of the projection weight vectors of the given words and the vectors for each word in the model')
	print(tuple_list)
	tuple_list_cosmul = model.most_similar_cosmul(positive=[word], topn=topn)
	print('Most similar words using the multiplicative combination objective proposed by Omer Levy and Yoav Goldberg')
	print(tuple_list_cosmul)
