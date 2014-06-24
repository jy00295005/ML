# This Python file uses the following encoding: utf-8
import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState

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
# voca_q = "SELECT keywords FROM clustering.three_topic_vocab where keywords!='' group by keywords"
voca_q = "SELECT keywords FROM clustering.clustering_vocab where keywords!='' group by keywords"
voca_rows = my_query(conn, voca_q)
# doc_q = "SELECT * FROM clustering.three_topic_projects"
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

features_sizes = np.linspace(10,3000,50).astype(int)
print features_sizes


AIR = np.zeros(features_sizes.shape)
MIBS = np.zeros(features_sizes.shape)
Homogeneity = np.zeros(features_sizes.shape)
completeness = np.zeros(features_sizes.shape)
V_measure = np.zeros(features_sizes.shape)
silhouette_score = np.zeros(features_sizes.shape)


for i, x in enumerate(features_sizes):
	vectorizer = CountVectorizer(
		# max_df=0.9,
		max_df=0.9,
		# min_df=2,
		# ngram_range=(1, 2),
		# vocabulary=myVoca,
		max_features=x,
		stop_words='english'
	)

	transformer = TfidfTransformer()
	X_counts = vectorizer.fit_transform(document_data)
	X_tfidf = transformer.fit_transform(X_counts)
	km = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
	X_kmean = km.fit(X_tfidf)
	air_score = metrics.adjusted_rand_score(myLabel, km.labels_)
	mutual = metrics.adjusted_mutual_info_score(myLabel, km.labels_)
	all_three_score = metrics.homogeneity_completeness_v_measure(myLabel, km.labels_)
	silhouette = metrics.silhouette_score(X_tfidf, X_kmean.labels_, metric='euclidean')
	AIR[i] = air_score
	MIBS[i] = mutual
	Homogeneity[i] = all_three_score[0]
	completeness[i] = all_three_score[1]
	V_measure[i] = all_three_score[2]
	silhouette_score[i] = silhouette

	# print "ARI 计算真实与预测的结果相似度: %s" % air_score  #相似度
	# print "Mutual Information based scores 使用labels_true和labels_pred 来计算之间的一致性: %s" % metrics.adjusted_mutual_info_score(myLabel, km.labels_)
	# # print ''
	# print "Homogeneity 同质性 每个簇中的成员只包含唯一个类型: %s" % all_three_score[0]
	# print "completeness 完整性 一个类型中得全部成员都被分配到同一个簇中: %s" % all_three_score[1]
	# print "V-measure 相等于上面的NIMI的标签熵之和的归一化 normalized by sum of label entropies: %s" % all_three_score[2]
	# print "Silhouette Coefficient 轮廓系数: %s" % metrics.silhouette_score(X_tfidf, X_kmean.labels_, metric='euclidean')


# print AIR
fig, ax = plt.subplots()
ax.plot(features_sizes, AIR, lw=2, label='ARI 计算真实与预测的结果相似度')
# ax.plot(features_sizes,MIBS,lw=2,label='ARI 计算真实与预测的结果相似度')
# ax.plot(features_sizes,Homogeneity,lw=2,label='ARI 计算真实与预测的结果相似度')
# ax.plot(features_sizes,completeness,lw=2,label='ARI 计算真实与预测的结果相似度')
# ax.plot(features_sizes,V_measure,lw=2,label='ARI 计算真实与预测的结果相似度')
# ax.plot(features_sizes,silhouette_score,lw=2,label='ARI 计算真实与预测的结果相似度')
# ax.plot(sizes,train_err_list,lw=2,label='train error')
ax.set_xlabel('number of feathers')
ax.set_ylabel('norm')

ax.legend(loc=0)
ax.set_xlim(0, 3000)
ax.set_title('AIR curve')

plt.show()
