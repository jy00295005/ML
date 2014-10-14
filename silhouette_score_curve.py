# This Python file uses the following encoding: utf-8
import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState
import matplotlib.pyplot as plt
import numpy as np
from helper import *

max_number_k = 20
step_k = max_number_k
stop_words = get_stop_words()
data_fields = {"title":17, "abstract":19, "ref_code":2, "pbid":1, "group":3}


def kmean_silhouette_score_curve(max_k=10, step_k=10, X=None):
	number_k = np.linspace(2, max_k, step_k).astype(int)
	silhouette_score = np.zeros(number_k.shape)
	# print number_k

	for i, x in enumerate(number_k):
		print "start compute %s k" % x
		km_curve = KMeans(n_clusters=x, init='k-means++', max_iter=500, n_init=200)
		km_curve.fit(X)
		silhouette = metrics.silhouette_score(X_tfidf, km_curve.labels_, metric='euclidean')
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

# doc_q = "SELECT * FROM clustering.nuclear_physics_full_table_new " \
# 		"WHERE (" \
# 		"(" \
# 		"PSShortName_Group = 'NSF' and Sponser = 'Division of Physics' " \
# 		"and not (title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%')" \
# 		") or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )" \
# 		") AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009)" \
# 		"GROUP BY Title"

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
# 		"AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009)" \
# 		")" \
# 		"GROUP BY Title"
# doc_q = "SELECT * FROM clustering.particle where not ( title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%')"

# doc_q = "SELECT * FROM clustering.truth"
# doc_q = "SELECT * FROM clustering.truth"
doc_q = "SELECT * FROM clustering.lhc_data";

# data_fields = {"title": 2, "abstract": 3, "ref_code": 1, "pbid": 0, "group": 4}
doc_rows = my_query(doc_q)
document_data = []

# document_data, document_ref_code, document_pbid, document_group = parse_mysql_data(doc_rows, data_fields)
for i, row in enumerate(doc_rows):
	document_data.insert(i, (row[2] + ' ' + row[7]).decode('latin-1')) # + row[3]
	# document_data.insert(i, (row[3] + ' ' + row[6]).decode('latin-1')) # + row[3]

document_data = clean_test_data(document_data)


# print len(document_data)
print document_data[0]
print "data list created"
vectorizer = CountVectorizer(
	max_df=0.9,
	min_df=2,
	# ngram_range=(2, 2),
	# vocabulary=myVoca,
	# max_features=10000,
	stop_words=stop_words
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(document_data)
X_tfidf = transformer.fit_transform(X_counts)

print len(vectorizer.get_feature_names())


print "X_tfidf vectorizer created"


## 验证多少个k
kmean_silhouette_score_curve(max_k=max_number_k, step_k=step_k, X=X_tfidf)