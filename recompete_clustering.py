# This Python file uses the following encoding: utf-8
import sys
reload(sys)

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState
import matplotlib.pyplot as plt
import numpy as np
from helper import *

import requests
from sklearn.metrics.pairwise import euclidean_distances


def kmean_silhouette_score_curve(max_k=10, step_k=10, X=None):
	number_k = np.linspace(2, max_k, step_k).astype(int)
	silhouette_score = np.zeros(number_k.shape)
	# print number_k

	for i, x in enumerate(number_k):
		print "start compute %s k" % x
		km_curve = KMeans(n_clusters=x, init='k-means++', max_iter=200, n_init=50)
		km_curve.fit(X)
		# silhouette = metrics.silhouette_score(X_tfidf, km_curve.labels_, metric='euclidean')
		silhouette_score[i] = silhouette

	print "loop throgh all number of k, then plot fig"

	fig, ax = plt.subplots()
	ax.plot(number_k, silhouette_score, lw=2, label='silhouette_score vs number of k')
	ax.set_xlabel('number of k')
	ax.set_ylabel('silhouette_score')

	ax.legend(loc=0)
	ax.set_xlim(0, max_k)
	ax.set_title('number of k curve')
	plt.show()

stop_words = get_stop_words()

solr_base_url = 'http://10.0.15.64:8080/solr4sci/select/'
# rows = 7611
rows = 20
iter_number = 2 ##manually change iter number of seerach key words
params=[
	('q','*:*'), 
	('start',0), 
	('rows',rows), 
	('wt','python')
]


r = requests.get(solr_base_url, params=params)
rsp = eval( r.text )
# print rsp['response']['numFound']
data = [
	(doc['id'],doc['TI'],doc['AB'] ) 
	for doc in rsp['response']['docs'] if 'AB' in doc
]

doc_data = [TI+ " || " +AB[0] for (id,TI,AB) in data]

doc_id = [id for (id,TI,AB) in data];

print doc_id[:1]

# 特征特征
vectorizer = CountVectorizer(
	max_df=0.9,
	# min_df=2,
	# ngram_range=(1, 2),
	# vocabulary=myVoca,
	max_features=10000,
	stop_words=stop_words
	# stop_words='english'
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(doc_data)
X_tfidf = transformer.fit_transform(X_counts)
# print len(vectorizer.get_feature_names())
# kmean_silhouette_score_curve(max_k=200, step_k=200/5, X=X_tfidf)
# print vectorizer.get_feature_names()[0:1050]
# print len(vectorizer.get_feature_names())
# print "X_tfidf vectorizer created"

# ##k-means聚类
km = KMeans(n_clusters=3, init='k-means++', max_iter=200, n_init=100)
X_kmean = km.fit(X_tfidf)

insert_list = [(id,label) for id,label in zip(doc_id, km.labels_)]

print km.cluster_centers_

print euclidean_distances(km.cluster_centers_)

