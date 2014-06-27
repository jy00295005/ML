# This Python file uses the following encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from numpy.random import RandomState
from sklearn import metrics
from helper import *

data_fields = {"title": 17, "abstract": 19, "ref_code": 2, "pbid": 1, "group": 3, "label":20}
doc_q = "(select *, 0 as label from clustering.nuclear_physics_full_table_new where abstract like '%dark matter%' " \
		"and (PSShortName_Group = 'FP' or PSShortName_Group = 'NSF')  " \
		"and not ((title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%') " \
		"or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )) " \
		"group by title limit 10) " \
		"union all  " \
		"(select *, 1 as label from clustering.nuclear_physics_full_table_new where abstract like '%higgs boson%' " \
		"and (PSShortName_Group = 'FP' or PSShortName_Group = 'NSF')  " \
		"and not ((title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%') " \
		"or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )) " \
		"group by title limit 10 " \
		") " \
		"union all " \
		"(select *, 2 as label from clustering.nuclear_physics_full_table_new where abstract like '%Neutrino%' " \
		"and (PSShortName_Group = 'FP' or PSShortName_Group = 'NSF')  " \
		"and not ((title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%') " \
		"or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )) " \
		"group by title limit 10 " \
		")"

stop_words = get_stop_words()
num_k = 3
#fatch data from mysql
doc_rows = my_query(doc_q)
document_data, document_ref_code, document_pbid, document_group, document_label = parse_mysql_data(doc_rows, data_fields,True)
print len(document_data)
# print document_label
print "data list created"
document_data = clean_data(document_data)

voca_q = "SELECT text FROM clustering.new_test_unclear_physics_keywords where text!='' group by text"
voca_rows = my_query(voca_q)
myVoca = []
for i, row in enumerate(voca_rows):
	myVoca.insert(i, row[0])

# print myVoca[:50]
# print len(myVoca)


#特征特征
vectorizer = CountVectorizer(
	max_df=0.7,
	# min_df=3,
	# ngram_range=(1, 2),
	# vocabulary=myVoca,
	max_features=1500,
	stop_words=stop_words
	# stop_words='english'
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(document_data)
X_tfidf = transformer.fit_transform(X_counts)


print len(vectorizer.get_feature_names())

##k-means聚类
km = KMeans(n_clusters=num_k, init='k-means++', max_iter=1000, n_init=1, verbose=False, random_state=RandomState(42))
X_kmean = km.fit(X_tfidf)
print document_label
print km.labels_
air_score = metrics.adjusted_rand_score(document_label, km.labels_)

print air_score
