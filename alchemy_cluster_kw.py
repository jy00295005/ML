# This Python file uses the following encoding: utf-8
import MySQLdb
from alchemyapi import AlchemyAPI
from pony.orm import *
year = 2012

if year == 2014:
	RF_table = 'RF2014'
	c_id_array = range(1,213)

else:
	RF_table = 'RF2012'
	c_id_array = range(1,150)


conn = MySQLdb.connect(host='10.0.15.72', user='root', passwd='ct123690')


def my_query(q, connection=conn):
	cursor = connection.cursor()
	cursor.execute(q)
	return cursor.fetchall()


db = Database('mysql', host='10.0.15.72', user='root', passwd='ct123690', db='ML')

clusters_doc = []
for i,x in enumerate(c_id_array):
	print "start cluster %i" %i

	cluster_doc_q = "select docs " \
					"from ML.ra_document where cluster_id = %s and year=%i" %(x,year)

	cluster_combine_doc = my_query(cluster_doc_q)[0][0]
	clusters_doc.insert(i, cluster_combine_doc)




class alchemy_api_cluster_keyword_new(db.Entity):
    id = PrimaryKey(int, auto=True)
    cluster_id = Required(int)
    word = Required(LongStr)
    relevance = Required(float)
    year = Required(int)

class alchemy_api_cluster_concept_new(db.Entity):
    id = PrimaryKey(int, auto=True)
    cluster_id = Required(int)
    concept = Required(LongStr)
    relevance = Required(float)
    year = Required(int)
    

db.generate_mapping(create_tables=True) 

alchemyapi = AlchemyAPI()

######combine each cluster documents to a big document#########

print "doucment ready for api"

for index, doc in enumerate(clusters_doc):
	print index
	response = alchemyapi.keywords('text', doc, {'keywordExtractMode':'strict','maxRetrieve':60})
	if response['status'] == 'OK':
		for keyword in response['keywords']:
			with db_session:
				alchemy_api_cluster_keyword_new(
					cluster_id = c_id_array[index],
					word = keyword['text'].encode('utf-8'),
					relevance = keyword['relevance'],
					year = year
				)

	else:
		print("doc number keyword %i") %index

	concepts_response = alchemyapi.concepts('text', doc, {'maxRetrieve':20})
	if concepts_response['status'] == 'OK':
		for concept in concepts_response['concepts']:
			# print concepts_response
			with db_session:
				alchemy_api_cluster_concept_new(
					cluster_id = c_id_array[index],
					concept = concept['text'].encode('utf-8'),
					relevance = concept['relevance'],
					year = year
				)
	else:
		print("doc number concepts %i") %index