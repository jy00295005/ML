# This Python file uses the following encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from numpy.random import RandomState
from helper import *

#vars
num_k = 8
r = 0.4
# doc_q = "SELECT * FROM clustering.nuclear_physics_full_table_new " \
# 		"WHERE (" \
# 		"(" \
# 		"PSShortName_Group = 'NSF' and Sponser = 'Division of Physics' " \
# 		"and not (title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%')" \
# 		") or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )" \
# 		") AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009)" \
# 		"GROUP BY Title"

voca_q = "SELECT keyword FROM clustering.lhc_term_words " \
			 "where keyword!='' and relevance > %s group by keyword" %r
voca_rows = my_query(voca_q)

# doc_q = "SELECT * FROM clustering.nuclear_physics_full_table_new " \
# 		"WHERE " \
# 		"(" \
# 		"title like '%Large Hadron Collider%' " \
# 		"or title like 'LHC' " \
# 		"or abstract like '%Large Hadron Collider%' " \
# 		"or abstract like 'LHC'" \
# 		") " \
# 		"and " \
# 		"(" \
# 		"(" \
# 		"PSShortName_Group = 'NSF' " \
# 		"and not (title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%') " \
# 		"or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )" \
# 		") " \
# 		"AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009) " \
# 		"AND (RefCode != 254410 AND RefCode != 0903536 AND RefCode != 235230 AND RefCode != 264564 " \
# 		"AND RefCode != 1004320 AND RefCode != 1111317 AND RefCode != 1210244 AND RefCode != 1020885 AND RefCode != 1068420) " \
# 		")" \
# 		"GROUP BY Title"

doc_q = "SELECT * FROM clustering.lhc_data";

data_fields = {"title": 2, "abstract": 7, "ref_code": 1, "pbid": 0, "group": 4}
stop_words = get_stop_words()
# insert_table_name = 'clustering.2groups_%dk_phydivision_results_stopword_clean' % num_k
insert_table_name = 'clustering.LHC_clustering_term11k'
# insert_table_name = 'clustering.LHC_clustering%dk' %num_k
# insert_table_name = 'clustering.LHC_clustering_clean%dk' %num_k

#fatch data from mysql
doc_rows = my_query(doc_q)
document_data, document_ref_code, document_pbid, document_group = parse_mysql_data(doc_rows, data_fields)

myVoca = []
for i, row in enumerate(voca_rows):
	myVoca.insert(i, row[0])

print len(document_data)
print "data list created"
document_data = clean_data(document_data)

#特征特征
vectorizer = CountVectorizer(
	max_df=0.9,
	min_df=2,
	# ngram_range=(1, 2),
	# vocabulary=myVoca,
	# max_features=10000,
	stop_words=stop_words
	# stop_words='english'
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(document_data)
X_tfidf = transformer.fit_transform(X_counts)
print X_tfidf[0]
print type(X_tfidf)
# print len(vectorizer.get_feature_names())

# print vectorizer.get_feature_names()[0:1050]
print len(vectorizer.get_feature_names())
print "X_tfidf vectorizer created"

##k-means聚类
km = KMeans(n_clusters=num_k, init='k-means++', max_iter=800, n_init=400)
X_kmean = km.fit(X_tfidf)
# print km.labels_

# ##计算聚类簇中得组成部分，NSF FP
# doc_label_list = [
# 	(pbid, refcode, doc, label, group)
# 	for pbid, refcode, doc, label, group
# 	in zip(document_data, km.labels_, document_ref_code, document_pbid, document_group)
# ]

# print doc_label_list[1]
# # print len(doc_label_list)
# group_count = counts_between_groups(num_k, doc_label_list)
# print len(group_count)

# # 将聚类结果写入数据库
# # insert_results_into_mysql(doc_label_list, insert_table_name)

# # print group_count
# # group_count = [(8, 14), (12, 27), (21, 16), (2, 24), (8, 13), (1, 17), (5, 17), (1, 11)]
# # plot pie charts
# plot_pie(group_count)