# This Python file uses the following encoding: utf-8
import sys
import numpy
reload(sys)
sys.setdefaultencoding('utf8')
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from numpy.random import RandomState
from helper import *
from scipy.sparse import csr_matrix, coo_matrix

def kmean_silhouette_score_curve(max_k=10, step_k=10, X=None):
	number_k = np.linspace(2, max_k, step_k).astype(int)
	silhouette_score = np.zeros(number_k.shape)
	# print number_k

	for i, x in enumerate(number_k):
		print "start compute %s k" % x
		km_curve = KMeans(n_clusters=x, init='k-means++', max_iter=500, n_init=200)
		km_curve.fit(X)
		silhouette = metrics.silhouette_score(X, km_curve.labels_, metric='euclidean')
		silhouette_score[i] = silhouette

	print "loop throgh all number of k, and plotting graph"

	fig, ax = plt.subplots()
	ax.plot(number_k, silhouette_score, lw=2, label='silhouette_score vs number of k')
	ax.set_xlabel('number of k')
	ax.set_ylabel('silhouette_score')

	ax.legend(loc=0)
	ax.set_xlim(0, max_k)
	ax.set_title('number of k curve')
	plt.show()


def convert(term_dict):
    # Create the appropriate format for the COO format.
    data = []
    row = []
    col = []
    for i, (k, v) in enumerate(term_dict.items()):
        r = int(k[0])
        c = int(k[1])
        data.append(v)
        row.append(r-1)
        col.append(c-1)
    # Create the COO-matrix
    coo = coo_matrix((data,(row,col)))
    # Let Scipy convert COO to CSR format and return
    return csr_matrix(coo)

doc_q = "SELECT * FROM clustering.scimap where c > 20";
data = my_query(doc_q)
sparse_m = dict(
	((a,b),s) for i, (a,b,s) in enumerate(data)
)

# print sparse_m
clustering_sparse  =  convert(sparse_m)


kmean_silhouette_score_curve(max_k=20, step_k=20, X=clustering_sparse)
# print clustering_sparse

# # print clustering_sparse
# for y in xrange(8,21):
# 	km = KMeans(n_clusters=y, init='k-means++', max_iter=400, n_init=200)
# 	X_kmean = km.fit(clustering_sparse)
# 	for i, x in enumerate(X_kmean.labels_):
# 		print "%i,%i,%s" % (y,i+1,x)

# km = KMeans(n_clusters=20, init='k-means++', max_iter=400, n_init=200)
# X_kmean = km.fit(clustering_sparse)

# # print X_kmean.labels_

# for i, x in enumerate(X_kmean.labels_):
# 	print "%i,%s" % (i+1,x)