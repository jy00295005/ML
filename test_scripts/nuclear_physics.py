# This Python file uses the following encoding: utf-8
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  
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


def my_query(connection, q):
	cursor = connection.cursor()
	cursor.execute(q)
	return cursor.fetchall()


def kmean_silhouette_score_curve(max_k=10, step_k=10):
	number_k = np.linspace(2, max_number_k, step_k).astype(int)
	silhouette_score = np.zeros(number_k.shape)

	print number_k

	for i, x in enumerate(number_k):
		print "start compute %s k" % x
		km_curve = KMeans(n_clusters=x, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
		# km_curve.labels_
		X_curve_kmean = km_curve.fit(X_tfidf)
		silhouette = metrics.silhouette_score(X_tfidf, km_curve.labels_, metric='euclidean')
		silhouette_score[i] = silhouette

	print "loop throgh all number of k, then plot fig"

	fig, ax = plt. subplots()
	ax.plot(number_k, silhouette_score, lw=2, label='silhouette_score vs number of k')
	ax.set_xlabel('number of k')
	ax.set_ylabel('silhouette_score')

	ax.legend(loc=0)
	ax.set_xlim(0, max_number_k)
	ax.set_title('number of k curve')
	plt.show()

conn = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')

doc_q = "SELECT * FROM clustering.nuclear_physics_full_table WHERE (PSShortName_Group ='NSF' or PSShortName_Group = 'FP')"
doc_rows = my_query(conn, doc_q)


document_data = []
document_ref_code = []
document_pbid = []
for i, row in enumerate(doc_rows):
	if row[11] == 'NULL':
		document_data.insert(i, row[9].decode('latin-1')) # + row[3]
	else:
		document_data.insert(i, (row[9].decode('latin-1') + ' || ' + row[6]).decode('latin-1')) # + row[3]
	document_ref_code.insert(i, row[2])
	document_pbid.insert(i, row[1])


	

print document_data[1000]
print len(document_data)
print "data list created"

vectorizer = CountVectorizer(
	# max_df=1.095
	max_df=0.95,
	# min_df=2,
	# ngram_range=(2, 2),
	# vocabulary=myVoca,
	# max_features=2500,
	stop_words='english'
)

transformer = TfidfTransformer()
X_counts = vectorizer.fit_transform(document_data)
X_tfidf = transformer.fit_transform(X_counts)

print "X_tfidf vectorizer created"

max_number_k = 200

## 验证多少个k
kmean_silhouette_score_curve(max_k=max_number_k, step_k=max_number_k/4)
# km = KMeans(n_clusters=159, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
# km.fit(X_tfidf)
# print km.labels_
#
# doc_label_list = [(pbid, refcode, doc, label) for pbid, refcode, doc, label in zip(document_data, km.labels_, document_ref_code, document_pbid)]
#
# print doc_label_list[13]
# print doc_label_list[0]
# print doc_label_list[2]
# print len(doc_label_list)

# cursor = conn.cursor()
#
# for i, (text_data, label, Ref_code, PBID) in enumerate(doc_label_list):
# 	sql = "INSERT INTO clustering.159k_projects(text_data, \
# 		label, Ref_code, PBID) \
# 		VALUES (\"%s\",\"%d\", \"%s\", \"%s\" )" % \
# 		(text_data.replace('"', '\\"').decode('latin-1'), label, Ref_code, PBID)
#      	# print(sql)
#
# 	try:
# 	   	# 执行sql语句
# 	   	cursor.execute(sql)
# 	   	# 提交到数据库执行
# 	   	conn.commit()
# 	   	print 'commit %d' %i
# 	except:
# 	   	# 发生错误时回滚
# 	   	conn.rollback()
# 	   	print 'rollback %d' %i
#      	# print(sql)
#      	# print "-------------------------------------------------------------------"
#
# # 关闭数据库连接
# conn.close()