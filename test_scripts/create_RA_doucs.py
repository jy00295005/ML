# This Python file uses the following encoding: utf-8
import MySQLdb
from pony.orm import *

year = 2012

if year == 2014:
	RF_table = 'RF2014'
	c_id_array = range(1,213)
	# c_id_array = range(187,213)
	# c_id_array = [18,111]

else:
	RF_table = 'RF2012'
	c_id_array = range(1,150)
print c_id_array

conn = MySQLdb.connect(host='10.0.15.72', user='root', passwd='ct123690')

def my_query(q, connection=conn):
	cursor = connection.cursor()
	cursor.execute(q)
	return cursor.fetchall()

db = Database('mysql', host='10.0.15.72', user='root', passwd='ct123690', db='ML')


class RA_document(db.Entity):
    id = PrimaryKey(int, auto=True)
    cluster_id = Required(int)
    docs = Required(LongStr)
    year = Required(long)

db.generate_mapping(create_tables=True) 


clusters_doc = []
for i, x in enumerate(c_id_array):
	print x

	cluster_doc_q = "select Title, Abstract " \
					"from ML.clusterUT as c JOIN ML.%s as r on c.ut = r.UT where c.cid = %s and c.year=%i" %(RF_table,x,year)

	cluster_combine_doc = [' || '.join([title, abstract]) for i,(title, abstract) in enumerate(my_query(cluster_doc_q))]

	with db_session:
		RA_document(
			cluster_id = x,
			docs = " && ".join(cluster_combine_doc).encode('utf-8'),
			year = year
		)

