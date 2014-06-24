# This Python file uses the following encoding: utf-8
import MySQLdb
import numpy as np

import pylab as pl
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


#TODO 1 find test projects ids
#TODO 2 use title and abstract words as vocabulary list
#TODO 3 use vocaulary list to do documents vectorizer and clutering
#TODO 4 use real data test clutering


def my_query(connection, q):
	cursor = connection.cursor()
	cursor.execute(q)
	return cursor.fetchall()

conn = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')
voca_q = "SELECT keywords FROM clustering.clustering_vocab where keywords!='' group by keywords"
voca_rows = my_query(conn, voca_q)
doc_q = "SELECT * FROM clustering.clustring_projects"
doc_rows = my_query(conn, doc_q)

myVoca = []
for i, row in enumerate(voca_rows):
	myVoca.insert(i, row[0])

document_data = []
myLabel = []
for i, row in enumerate(doc_rows):
	document_data.insert(i, (row[2] + ' ' + row[3]).decode('latin-1')) # + row[3]
	myLabel.insert(i, row[4])


vectorizer = CountVectorizer(
	# max_df=1.095
	max_df=0.9,
	# min_df=2,
	# ngram_range=(2, 2),
	# vocabulary=myVoca,
	# max_features=1000,
	stop_words='english'
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(document_data)
X_tfidf = transformer.fit_transform(X_counts)
# print vectorizer.get_feature_names()
# print len(vectorizer.get_feature_names())
km = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
X_kmean = km.fit(X_tfidf)
X_kmean_r = X_kmean.transform(X_tfidf)

# print(X_kmean_r)
# print X_kmean.labels_
# print X_kmean.labels_
print km.labels_
print np.asarray(myLabel, dtype=np.int)

air_score = metrics.adjusted_rand_score(myLabel, km.labels_)
all_three_score = metrics.homogeneity_completeness_v_measure(myLabel, km.labels_)

print "ARI 计算真实与预测的结果相似度: %s" % air_score  #相似度
print "Mutual Information based scores 使用labels_true和labels_pred 来计算之间的一致性: %s" % metrics.adjusted_mutual_info_score(myLabel, km.labels_)
# print ''
print "Homogeneity 同质性 每个簇中的成员只包含唯一个类型: %s" % all_three_score[0]
print "completeness 完整性 一个类型中得全部成员都被分配到同一个簇中: %s" % all_three_score[1]
print "V-measure 相等于上面的NIMI的标签熵之和的归一化 normalized by sum of label entropies: %s" % all_three_score[2]
print "Silhouette Coefficient 轮廓系数: %s" % metrics.silhouette_score(X_tfidf, np.asarray(myLabel, dtype=np.int), metric='euclidean')
pl.figure()
fig, ax = pl.subplots()

for c, i, in zip("rgb", [0, 1, 2]):
	pl.scatter(X_kmean_r[np.asarray(X_kmean.labels_) == i, 1], X_kmean_r[np.asarray(X_kmean.labels_) == i, 2], c=c,label='Dimension 1 vs Dimension2')
	ax.set_xlabel('Dimension 1 ')
	ax.set_ylabel('Dimension 2 ')
	ax.set_title('scatter plot of 3 cluster Dimension 1 vs Dimension 2')

pl.show()
