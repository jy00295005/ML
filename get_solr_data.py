import requests
from pony.orm import *

##define the mysql database and the table Truth with pony
db = Database('mysql', host='localhost', user='root', passwd='ct123690', db='clustering')
# sql_debug(True) 
db.generate_mapping(create_tables=True) 
class Truth(db.Entity):
	id = PrimaryKey(int, auto=True)
	systemid = Required(LongStr)
	RefCode = Required(str)
	Title = Required(str)
	Abstract = Optional(LongStr)
	label = Required(int)

## solr query and write results into a tuple
solr_base_url = 'http://10.0.15.232:8080/solrprj3/select/'
rows = 100
words = ['higgs','Neutrino*','dark matter']
iter_number = 2 ##manually change iter number of seerach key words
params=[
	('q','(PSShortName_Group:NSF OR PSShortName_Group:FP) AND Title:(%s)' % words[iter_number] ), 
	('start',0), 
	('rows',rows), 
	('wt','python')
]
r = requests.get(solr_base_url, params=params)
rsp = eval( r.text )
# print rsp['response']['numFound']
data = [
	(doc['id'],doc['RefCode'],doc['Title'],doc['Abstract'] ) 
	for doc in rsp['response']['docs'] if 'Abstract' in doc
]
# print len(data)

## insert tuple into Truth table
with db_session:
	for (id, RefCode, Title, Abstract) in data:
		Truth(
			systemid = id,
			RefCode = RefCode,
			Title = Title,
			Abstract = Abstract,
			label = iter_number
		)