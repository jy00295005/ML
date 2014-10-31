# This Python file uses the following encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans, MiniBatchKMeans
from numpy.random import RandomState
from helper import *

c_id_array = [7,136,142]

######combine each cluster documents to a big document#########
clusters_doc = []
for i,x in enumerate(c_id_array):
	cluster_doc_q = "select Title, Abstract " \
					"from clustering.cluster7UT as c JOIN clustering.RF2012 as r on c.ut = r.UT where c.c_id = %s" %x

	cluster_combine_doc = [' || '.join([title, abstract]) for i,(title, abstract) in enumerate(my_query(cluster_doc_q))]
	clusters_doc.insert(i, " && ".join(cluster_combine_doc))

print clusters_doc[0]

######
voca_q = "select cluster7UT.ut,apiword14.word,apiword14.relevance " \
		"from clustering.cluster7UT JOIN clustering.apiword14 "\
		"on clustering.cluster7UT.ut = clustering.apiword14.ut where clustering.apiword14.year = 2012 "

voca_rows = my_query(voca_q)
voca_words = [word for i,(ut,word,relenvace) in enumerate(voca_rows)]
# print voca_words[:10]
v = CountVectorizer(
	lowercase = False,
	ngram_range=(1, 2), 
	vocabulary=voca_words
)

# print v.vocabulary_[:10]
print voca_words[:10]

counts = v.fit_transform(clusters_doc)

print counts[0]
transformer = TfidfTransformer()

tfidf_s = transformer.fit_transform(counts)

print tfidf_s[0:1]




# print clusters_doc[0]

# r = 0.3

# voca_q = "SELECT * FROM clustering.cluster7_kw " \
# 			 "where relevance > %s " %r


# voca_rows = my_query(voca_q)

# voca_words = [word for i,(ut,word,relenvace) in enumerate(voca_rows)]

# cluster_doc_q = "select Title, Abstract " \
# 				"from clustering.cluster7UT as c JOIN clustering.RF2012 as r on c.ut = r.UT" 

# cluster_doc_rows = my_query(cluster_doc_q)

# cluster_combine_doc = [title + " || " + abstract for i,(title, abstract) in enumerate(cluster_doc_rows)]

# # print cluster_combine_doc[0]
				
# test_doc = ["THREE-FLAVOUR NEUTRINO OSCILLATION UPDATE || We review the present status of three-flavour neutrino oscillations, taking into account the latest available neutrino oscillation data presented at the Neutrino 2008 Conference. This includes the data released this summer by the MINOS collaboration, the data of the neutral current counter phase of the Sudbury Neutrino Observatory (SNO) solar neutrino experiment, as well as the latest KamLAND and Borexino data. We give the updated determinations of the leading 'solar' and 'atmospheric' oscillation parameters. We find from global data that the mixing angle theta(13) is consistent with zero within 0.9 sigma and we derive an upper bound of sin(2)theta(13) <= 0.035 (0.056) at 90% confidence level (CL) (3 sigma)."]

# voca_words_test = ['review','NEUTRINO OSCILLATION']
# vectorizer = CountVectorizer(
# 	# max_df=0.9,
# 	# min_df=2,
# 	# ngram_range=(1, 3),
# 	vocabulary=voca_words_test,
# 	# max_features=10000,
# 	# stop_words=stop_words
# 	# stop_words='english'
# )

# print vectorizer.fit(test_doc).vocabulary_


# print vectorizer.vocabulary_
# # transformer = TfidfTransformer()
# X_counts = vectorizer.fit_transform(test_doc)
# print X_counts
# print vectorizer.get_feature_names()

# X_tfidf = transformer.fit_transform(X_counts)
# print X_counts[0:10]
# print X_tfidf[0:10]
# print getnnz(X_tfidf[0])


# v = CountVectorizer(
# 	ngram_range=(1, 2), 
# 	vocabulary={"keeps", "keeps the", "doctor away","doctor awaya"}
# )
# print v.vocabulary_
# test_counts = v.fit_transform(["an apple a day keeps the doctor away"])

# print test_counts

