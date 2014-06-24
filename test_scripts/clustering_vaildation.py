# This Python file uses the following encoding: utf-8
from sklearn.datasets import fetch_20newsgroups
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState

n_feathers = 1500

stop_word = [
	'to', 'a', 'can', 'could', 'do', 'did', 'does', 'may', 'might', 'would', 'should', 'must', 'will', 'ought',
	'shall', 'need', 'is', 'am', 'are', 'about', 'according', 'after', 'against', 'all', 'almost', 'also', 'although',
	'among', 'an', 'and', 'anothr', 'any', 'anthing', 'as', 'asked', 'at', 'back', 'because', 'before', 'before', 'beside',
	'between', 'both', 'but', 'by', 'called', 'each', 'enen', 'every', 'for', 'he', 'her', 'his', 'how', 'however',
	'i', 'in', 'it', 'its', 'just', 'last', 'like', 'many', 'maybe', 'most', 'my', 'no', 'not', 'off',
	'only', 'our', 'perhaps', 'regarding', 'she', 'sice', 'so', 'some', 'somehow', 'that', 'the', 'they', 'this', 'those',
	'to', 'under', 'unless', 'we', 'what', 'whatever', 'when', 'where', 'without', 'you', 'your', 'english'
]

categories = [
	'alt.atheism',
	'soc.religion.christian',
	'comp.graphics',
	'sci.med']

twenty_train = fetch_20newsgroups(
	subset='train',
	categories=categories,
	shuffle=True,
	random_state=42)

print 'traning data labels: '
print(twenty_train.target_names)
print '--------------------------------------'
print '共2257条文本, 显示其中一条:'
print(twenty_train.data[2])
print '--------------------------------------'
print "前20个text的类型: "
print(twenty_train.target[:20])

# Hashing + Tfidf Vectorizer => high demensional data


print '--------------------------------------'
print '--------------------------------------'
# hasher = HashingVectorizer(
# 	n_features=n_feathers,
#     stop_words=stop_word,
# 	non_negative=True,
# 	norm=None, binary=False
# )

vectorizer = TfidfVectorizer(
	max_df=0.6,
	max_features=n_feathers,
	stop_words=stop_word,
	use_idf=True
)


# vectorizer = Pipeline((
# 	('hasher', hasher),
# 	('tf_idf', TfidfTransformer())
# ))

X = vectorizer.fit_transform(twenty_train.data)
labels = twenty_train.target
true_k = np.unique(labels).shape[0]


km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
X_kmean = km.fit(X)
# print km.cluster_centers_
print '##########################'


air_score = metrics.adjusted_rand_score(twenty_train.target, km.labels_)
all_three_score = metrics.homogeneity_completeness_v_measure(twenty_train.target, km.labels_)
print air_score
print all_three_score
print metrics.silhouette_score(X, km.labels_, metric='euclidean')

# 0.172990728537
# (0.23396974800824874, 0.34894426413758112, 0.28011816442240145)
# 0.00810690704347