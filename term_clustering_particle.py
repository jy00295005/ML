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


################## SETTING #########################
doc_q = "SELECT * FROM clustering.particle " \
		"where not ( " \
		"title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%'" \
		")"

voca_q = "SELECT keyword FROM clustering.particle_keywords " \
			 "where keyword!='' and relevance > 0.85 group by keyword"
stop_words = get_stop_words()
k = 50
####################################################

voca_rows = my_query(voca_q)
doc_rows = my_query(doc_q)

myVoca = []
for i, row in enumerate(voca_rows):
	myVoca.insert(i, row[0])

document_data = []
myLabel = []
for i, row in enumerate(doc_rows):
	document_data.insert(i, (row[1] + ' || ' + row[2]).decode('latin-1'))
	myLabel.insert(i, row[3])

document_data = clean_test_data(document_data)
vectorizer = CountVectorizer(
	vocabulary=myVoca,
	stop_words=stop_words
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(document_data)
X_tfidf = transformer.fit_transform(X_counts)

features = vectorizer.get_feature_names()
print len(features)
km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
X_kmean = km.fit(X_tfidf)
doc_label_list = [
	(doc, label)
	for doc, label
	in zip(document_data, km.labels_)
]

connection = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')
cursor = connection.cursor()

for i, (d,l) in enumerate(doc_label_list):
	sql = "INSERT INTO %s (data, \
			label) \
			VALUES (\"%s\",\"%d\")" % \
			("clustering.particle_clustring_085_50k", d.replace('"', ''), l)

	try:
		# 执行sql语句
		cursor.execute(sql)
		# 提交到数据库执行
		connection.commit()
		print 'commit %d' %i

	except:
		# 发生错误时回滚
		connection.rollback()
		print 'rollback %d' %i
connection.close()



