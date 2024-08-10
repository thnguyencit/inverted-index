# from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from asyncore import write
# from semantic_check import *
import os
import tachtu
import json
import time
import string
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm
from datetime import datetime


today = datetime.today()
time = today.strftime("%H") + "h" + today.strftime("%M")
date = today.strftime("%Y-%m-%d")
dateVN = today.strftime("%d-%m-%Y")


fileName = "VI_StopWord.txt" #Các từ dừng trong tiếng Việt
file_input = open(fileName, "r+", encoding="utf-8")
read_file = file_input.read()
stopword = read_file.split("\n")


def text_preprocess(text):
    # remove punctuations
    trans = str.maketrans('', '', string.punctuation)
    text = text.translate(trans)
    # lowercase the text
    text = text.lower()
    # remove stopwords
    cleaned_text = ""
    for word in text.split():
        if word not in stopword:
            cleaned_text += word + " " 
    return cleaned_text

def run_baseline_test(tfidf):
    start_time = datetime.now() 
    pairwise_similarity = round(tfidf * tfidf.T, 3)
    pairwise_similarity = pairwise_similarity.toarray()
    end_time = datetime.now() 
    time_passed = end_time-start_time
    return pairwise_similarity, time_passed


def generate_inverted_index(data: list):
	# data_wt_stopword = []
	# for doc in data:
	# 	data_wt_stopword.append(text_preprocess(doc))
	inv_idx_dict = {}
	for index, doc_text in enumerate(data):
		for word in doc_text.split():
			# if(word.isalnum() == False):
			# 	continue
			if word not in inv_idx_dict.keys():
				inv_idx_dict[word.lower()] = [index]
			elif index not in inv_idx_dict[word]:
				inv_idx_dict[word].append(index)
	return dict(sorted(inv_idx_dict.items()))

def retrieve_vectors(data):
    docvectors = TfidfVectorizer(analyzer='word').fit_transform(data).toarray()
    return docvectors


def find_similarity(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def simplify_data(data):
    # nltk_turkish_stopwords = stopwords.words('turkish')
    # cv = CountVectorizer(max_df=0.3)
    cv = CountVectorizer()
    word_count_vector = cv.fit_transform(data)
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    
    def tfidf_top50(text):
        feature_names_out = cv.get_feature_names_out()
        tf_idf_vector = tfidf_transformer.transform(cv.transform([text]))
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        keywords = extract_topn_from_vector(feature_names_out,sorted_items, int(len(text)))
        # print(keywords)
        # keywords = extract_topn_from_vector(feature_names_out,sorted_items, 5)
        new_text = ""
        for keyword in keywords:
            new_text += keyword + " "
        return new_text

    temp_data = []
    for doc in data:
    	temp_data.append(tfidf_top50(doc))
    # print(temp_data)
    return temp_data

def openFile(filePath):
    fileOpen = open(filePath, "r", encoding='utf-8-sig')
    fileContent = fileOpen.read()
    return fileContent

def cutFileName(fileName):
    idx1 = fileName.find('/')
    idx2 = fileName.rfind('/')

    return idx1+1, idx2
