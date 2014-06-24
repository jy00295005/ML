import MySQLdb
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from numpy.random import RandomState


def my_query(conn,q):
	cursor = conn.cursor()
	cursor.execute(q)
	return cursor.fetchall()

stop_word = [
	'to', 'a', 'can', 'could', 'do', 'did', 'does', 'may', 'might', 'would', 'should', 'must', 'will', 'ought',
	'shall', 'need', 'is', 'am', 'are', 'about', 'according', 'after', 'against', 'all', 'almost', 'also', 'although',
	'among', 'an', 'and', 'anothr', 'any', 'anthing', 'as', 'asked', 'at', 'back', 'because', 'before', 'before', 'beside',
	'between', 'both', 'but', 'by', 'called', 'each', 'enen', 'every', 'for', 'he', 'her', 'his', 'how', 'however',
	'i', 'in', 'it', 'its', 'just', 'last', 'like', 'many', 'maybe', 'most', 'my', 'no', 'not', 'off',
	'only', 'our', 'perhaps', 'regarding', 'she', 'sice', 'so', 'some', 'somehow', 'that', 'the', 'they', 'this', 'those',
	'to', 'under', 'unless', 'we', 'what', 'whatever', 'when', 'where', 'without', 'you', 'your', 'english', 'who', 'with',
	'within', 'very', 'across', 'be', 'been', 'being', 'better', '000', '10', '100', '1000', '115', '12', '120', '13', '130'
	'13th', '17', '20', '2007', '2011', '2014', '2020', '20th', '21st', '22', '23', '24', '25', '29', '2d', '31', '33ka',
	'5th', '639', 'of', 'us', 'use', 'around', 'based', '2012', 'through', 'their', 'years', 'xxxvi', '13th', 'collaborative_research'
]


myVoca=['abelian_varieties', 'abrupt_climatic_transitions', 'acrylic_resins_product', 'activated_fouling_reversal', 'active_layer',
		'active_viscoelastic_mixture', 'adic_arithmetic_geometry', 'adsorbate_interactions', 'advanced_switching_control',
		'advantage_conference_phd', 'affine_crystals', 'affine_schubert_calculus', 'african_american_students', ''
		, 'aftershock_imaging', 'age_related_disabilities', 'age_western_sicily', 'agriscience_technician_training',
		'aid_visually_impaired', 'airborne_detector', 'alaskan_athabascan_grammar', 'alaskan_precipitation_variability',
		'albertine_rift', 'alene_online', 'algal_production', 'algebraic_geometry', 'algorithmic_dna_self',
		'biodiversity_conservation', 'biological_evaluation', 'biomechanical_rehabilitation_engineering', 'biophotonic_chips']
#get data from mysql
conn = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')
q = "SELECT * FROM clustering.cluster_table LIMIT 500"
rows = my_query(conn, q)

#insert data into a list
data_all = []
data_title = []
i = 0
for row in rows:
	String = row[2] + ' - ' + row[2] + ' - ' + row[2] + ' - ' + row[2] + ' - ' + \
			 row[2] + ' - ' + row[2] + ' - ' + row[2] + ' - ' + row[2] + ' - ' + \
			 row[2] + ' --- ' + row[3]

	data_all.insert(i, String.decode('latin-1'))
	data_title.insert(i, row[2])
	i += 1

n_feathers = 100

all_vectorizer = TfidfVectorizer(
	max_df=0.9,
	min_df=2,
	# ngram_range=(2,4),
	max_features=n_feathers,
	stop_words='english',
	use_idf=True
)

title_vectorizer = TfidfVectorizer(
	max_df=1.0,
	# min_df=0.003,
	# ngram_range=(1,2),
	vocabulary=myVoca,
	max_features=n_feathers,
	stop_words=stop_word,
	use_idf=True
)

X_title = title_vectorizer.fit_transform(data_title)
km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1, verbose=False, random_state=RandomState(42))
X_kmean = km.fit(X_title)

print(len(title_vectorizer.get_feature_names()))
print(title_vectorizer.get_feature_names())
print(X_kmean.labels_)
X_kmean.cluster_centers_
print metrics.silhouette_score(X_title, X_kmean.labels_, metric='euclidean')


labels = {}
title_dict = {}
for p in range(0, 5):
	labels[p] = [i for i, x in enumerate(X_kmean.labels_) if x == p]
	pos_i = 0
	title_list = []
	for pos in labels[p]:
		title_list.insert(pos_i, data_title[pos])
		pos_i += 1
	title_dict[p] = title_list

print title_dict[0]
print title_dict[1]
print title_dict[2]
print title_dict[3]
print title_dict[4]