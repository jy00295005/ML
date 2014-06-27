# This Python file uses the following encoding: utf-8
import MySQLdb
import pylab as pl
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from helper import *



###############setting###########
stop_words = get_stop_words()

# doc_q = "SELECT * FROM clustering.particle " \
# 		"where not ( " \
# 		"title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%'" \
# 		")"

doc_q = "SELECT * FROM clustering.nuclear_physics_full_table_new " \
		"WHERE (" \
		"(" \
		"PSShortName_Group = 'NSF' and Sponser = 'Division of Physics' " \
		"and not (title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%')" \
		") or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )" \
		") AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009)" \
		"GROUP BY Title"

relevcance_range = [float(y)/10 for y in [ .5*x for x in range(0*2, 9*2)]][3:20]
k_range = np.linspace(2, 50, 50/3).astype(int)
grid = [(r,k) for r in relevcance_range for k in k_range]
print relevcance_range
print len(grid)
################################

# print grid
result = []
for index, (r,k) in enumerate(grid[:3]):
	print (r,k)
	# voca_q = "SELECT keyword FROM clustering.particle_keywords " \
	# 		 "where keyword!='' and relevance > %s group by keyword" %r
	voca_q = "SELECT keyword FROM clustering.nuclear_physics_full_table_new_kw " \
			 "where keyword!='' and relevance > %s group by keyword" %r
	voca_rows = my_query(voca_q)
	doc_rows = my_query(doc_q)

	myVoca = []
	for i, row in enumerate(voca_rows):
		myVoca.insert(i, row[0])
	document_data = []
	for i, row in enumerate(doc_rows):
		document_data.insert(i, (row[17] + ' ' + row[19].decode('latin-1')))

	document_data = clean_test_data(document_data)
	# print document_data[0]
	vectorizer = CountVectorizer(
		vocabulary=myVoca,
		stop_words=stop_words
	)

	transformer = TfidfTransformer()
	X_counts = vectorizer.fit_transform(document_data)
	X_tfidf = transformer.fit_transform(X_counts)

	number_of_features = len(vectorizer.get_feature_names())
	km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
	X_kmean = km.fit(X_tfidf)
	silhouette = metrics.silhouette_score(X_tfidf, km.labels_, metric='euclidean')
	result.insert(i,(r,k,silhouette,number_of_features))

sorted_reslut = sorted(result, key=lambda x: float(x[2]), reverse=True)

print sorted_reslut[:100]