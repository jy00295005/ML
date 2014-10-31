from pony.orm import *
import sklearn
import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import scipy

db = Database('mysql', host='10.0.15.72', user='root', passwd='ct123690', db='ML')
conn = MySQLdb.connect(host='10.0.15.72', user='root', passwd='ct123690')
# sql_debug(True) 

def my_query(q, connection=conn):
        cursor = connection.cursor()
        cursor.execute(q)
        return cursor.fetchall()

class Tfidf_results(db.Entity):
        id = PrimaryKey(int, auto=True)
        cluster_id = Required(int)
        word = Required(LongStr)
        tfidf = Required(float)
        relevance = Required(float)

db.generate_mapping(create_tables=True) 

# conn = MySQLdb.connect(host='10.0.15.72', user='root', passwd='ct123690')


c_id_array = [7,136,142]
r = 0.5

clusters_doc = []
for i,x in enumerate(c_id_array):
        cluster_doc_q = "select Title, Abstract " \
                        "from ML.cluster7UT as c JOIN ML.RF2012 as r on c.ut = r.UT where c.c_id = %s" %x

        cluster_combine_doc = [' || '.join([title, abstract]) for i,(title, abstract) in enumerate(my_query(cluster_doc_q))]
        clusters_doc.insert(i, " && ".join(cluster_combine_doc))


voca_q = "select cluster7UT.ut,apiword14.word,apiword14.relevance " \
                "from ML.cluster7UT JOIN ML.apiword14 "\
                "on ML.cluster7UT.ut = ML.apiword14.ut where ML.apiword14.year = 2012 and relevance > %s group by apiword14.word" %r

voca_rows = my_query(voca_q)
print voca_rows[1]
voca_words = [word for i,(ut,word,relenvace) in enumerate(voca_rows)]


# print voca_words[:10]
v = CountVectorizer(
        lowercase = False,
        ngram_range=(1, 5),
        vocabulary=voca_words
)

counts = v.fit_transform(clusters_doc).toarray()

# print counts
transformer = TfidfTransformer()
print v.get_feature_names()
tfidf_s = transformer.fit_transform(counts)

# print type(tfidf_s)
cx = scipy.sparse.coo_matrix(tfidf_s)
for i,j,v in zip(cx.row, cx.col, cx.data):
        with db_session:
                Tfidf_results(
                        cluster_id = c_id_array[i],
                        word = voca_rows[j][1],
                        tfidf = v,
                        relevance = r
                )


