# This Python file uses the following encoding: utf-8
import MySQLdb
from pony.orm import *
from alchemyapi import AlchemyAPI
import json
from helper import *

year = 2012
start = 18000
total_count = 20000
select_number = 20

db = Database('mysql', host='localhost', user='root', passwd='ct123690', db='clustering')
# sql_debug(True) 

class Apiword14(db.Entity):
	id = PrimaryKey(int, auto=True)
	ut = Required(LongStr)
	word = Required(LongStr)
	w_type = Required(str)
	sentiment = Optional(str)
	sub_type = Optional(str)
	relevance = Optional(str)
	year = Optional(int)

class Apierror(db.Entity):
	id = PrimaryKey(int, auto=True)
	ut = Required(LongStr)
	w_type = Required(str)
	year = Optional(int)

db.generate_mapping(create_tables=True) 

#todo1 select 
alchemyapi = AlchemyAPI()



#循环选出论文
for x in xrange(start,total_count,select_number):
	print('## start %i ##' %x)

	data = []
	
	#select from mysql
	q = "SELECT * FROM clustering.RF2012 LIMIT %i OFFSET %i" % (select_number, x)
	rows = my_query(q)


	#生成进入API的文本，(ut, 题名+全文)
	for i, row in enumerate(rows):
		data.insert(i,(row[1], row[2] + ' ' + row[3]))


	for index, (UT, text) in enumerate(data):
		#get keyword
		kw_response = alchemyapi.keywords('text', text, {'sentiment': 1})
		if kw_response['status'] == 'OK':
			for keyword in kw_response['keywords']:
				with db_session:
					Apiword14(
						ut = UT,
						word = keyword['text'],
						w_type = 'keyword',
						# sentiment = keyword['sentiment']['type'],
						sentiment = '',
						sub_type = '',
						relevance = keyword['relevance'],
						year = year
					)
		else:
			print("UT is %s and index is %i and type is keywords") %(UT, index)
			with db_session:
				Apierror(
					ut = UT,
					w_type = 'keyword',
					year = year,
				)
		# #get concepts
		# concepts_response = alchemyapi.concepts('text', text)
		# if concepts_response['status'] == 'OK':
		#     for concept in concepts_response['concepts']:
		# 		with db_session:
		# 			Apiword14(
		# 				ut = UT,
		# 				word = concept['text'],
		# 				w_type = 'concept',
		# 				sentiment = '',
		# 				sub_type = '',
		# 				relevance = concept['relevance'],
		# 				year = year
		# 			)
		# else:
		# 	print("UT is %s and index is %i and type is concept") %(UT, index)
		# 	with db_session:
		# 		Apierror(
		# 			ut = UT,
		# 			w_type = 'concept',
		# 			year = 2014,
		# 		)

		# #get entity
		# entities_response = alchemyapi.entities('text', text, {'sentiment': 1})
		# if entities_response['status'] == 'OK':
		# 	for entity in entities_response['entities']:
		# 		with db_session:
		# 			Apiword14(
		# 				ut = UT,
		# 				word = entity['text'],
		# 				w_type = 'entity',
		# 				sentiment = entity['sentiment']['type'],
		# 				sub_type = '',
		# 				relevance = entity['relevance'],
		# 				year = year
		# 			)
		# else:
		# 	print("UT is %s and index is %i and type is entity") %(UT, index)
		# 	with db_session:
		# 		Apierror(
		# 			ut = UT,
		# 			w_type = 'entity',
		# 			year = 2014,
		# 		)
	# pass
# print data[0]