import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState


#TODO 1 find test projects ids
#TODO 2 use title and abstract words as vocabulary list
#TODO 3 use vocaulary list to do documents vectorizer and clutering
#TODO 4 use real data test clutering


def my_query(connection, q):
	cursor = connection.cursor()
	cursor.execute(q)
	return cursor.fetchall()

conn = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')

voca_q = "SELECT text FROM clustering.test_vocab where text !='' group by text"
voca_rows = my_query(conn, voca_q)

doc_q = "SELECT * FROM clustering.test_clustering_projects"
doc_rows = my_query(conn, doc_q)

myVoca = []
for i, row in enumerate(voca_rows):
	myVoca.insert(i, row[0])

doc_data = []
for i, row in enumerate(doc_rows):
	doc_data.insert(i, (row[2] + row[3]).decode('latin-1'))

n_feathers = 32000

vectorizer = CountVectorizer(
	max_df=0.9,
	# min_df=0.003,
	# ngram_range=(2, 2),
	# vocabulary=myVoca,
	max_features=1000,
	stop_words='english'
)

# print myVoca
transformer = TfidfTransformer()
print transformer
X_counts = vectorizer.fit_transform(doc_data)
X_tfidf = transformer.fit_transform(X_counts)
print(len(vectorizer.get_feature_names()))
km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(38))
X_kmean = km.fit(X_tfidf)

print X_kmean.labels_

print metrics.silhouette_score(X_tfidf, X_kmean.labels_, metric='euclidean')
