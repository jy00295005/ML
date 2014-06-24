# This Python file uses the following encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from numpy.random import RandomState
from helper import *

#vars
num_k = 13
# doc_q = "SELECT * FROM clustering.nuclear_physics_full_table_new " \
# 		"WHERE (" \
# 		"(" \
# 		"PSShortName_Group = 'NSF' and Sponser = 'Division of Physics' " \
# 		"and not (title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%')" \
# 		") or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )" \
# 		") AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009)" \
# 		"GROUP BY Title"
doc_q = "SELECT * FROM clustering.nuclear_physics_full_table_new " \
		"WHERE " \
		"(" \
		"title like '%Large Hadron Collider%' " \
		"or title like 'LHC' " \
		"or abstract like '%Large Hadron Collider%' " \
		"or abstract like 'LHC'" \
		") " \
		"and " \
		"(" \
		"(" \
		"PSShortName_Group = 'NSF' " \
		"and not (title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%') " \
		"or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )" \
		") " \
		"AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009)" \
		")" \
		"GROUP BY Title"

data_fields = {"title":17, "abstract":19, "ref_code":2, "pbid":1, "group":3}
stop_words = get_stop_words()
# insert_table_name = 'clustering.2groups_%dk_phydivision_results_stopword' %num_k
insert_table_name = 'clustering.LHC_clustering%dk' %num_k

#fatch data from mysql
doc_rows = my_query(doc_q)
document_data, document_ref_code, document_pbid, document_group = parse_mysql_data(doc_rows, data_fields)
print len(document_data)
print document_data[0]
print "data list created"

print document_group


#特征
vectorizer = CountVectorizer(
	max_df=0.9,
	# min_df=2,
	# ngram_range=(2, 2),
	# vocabulary=myVoca,
	# max_features=10000,
	stop_words=stop_words
	# stop_words='english'
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(document_data)
X_tfidf = transformer.fit_transform(X_counts)

# print vectorizer.get_feature_names()
# print len(vectorizer.get_feature_names())
print "X_tfidf vectorizer created"

##k-means聚类
km = KMeans(n_clusters=num_k, init='k-means++', max_iter=1000, n_init=1, verbose=False, random_state=RandomState(42))
X_kmean = km.fit(X_tfidf)
# print km.labels_

##计算聚类簇中得组成部分，NSF FP
doc_label_list = [
	(pbid, refcode, doc, label, group)
	for pbid, refcode, doc, label, group
	in zip(document_data, km.labels_, document_ref_code, document_pbid, document_group)
]
print doc_label_list[1]
# print len(doc_label_list)
group_count = counts_between_groups(num_k, doc_label_list)
print group_count

## 将聚类结果写入数据库
# insert_results_into_mysql(doc_label_list, insert_table_name)

