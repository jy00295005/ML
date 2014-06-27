# This Python file uses the following encoding: utf-8
import MySQLdb

from alchemyapi import AlchemyAPI
import json
from helper import *

# doc_q = "SELECT * FROM clustering.particle where not ( title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%')"
doc_q = "SELECT * FROM clustering.nuclear_physics_full_table_new " \
		"WHERE (" \
		"(" \
		"PSShortName_Group = 'NSF' and Sponser = 'Division of Physics' " \
		"and not (title like '%conference%' or title like '%workshop%' or title like '%host%' or title like '%REU Site%')" \
		") or (PSShortName_Group = 'FP' AND PBTC NOT LIKE '%Social Aspects%' )" \
		") AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009)" \
		"GROUP BY Title"

doc_rows = my_query(doc_q)

document_id = []
document_data = []
myLabel = []
for i, row in enumerate(doc_rows):
	document_data.insert(i, (row[17] + ' ' + row[19]))
	document_id.insert(i, row[0])
document_data = clean_test_data(document_data)
data_with_id = [(id,data) for data, id in zip(document_data, document_id)]

alchemyapi = AlchemyAPI()

conn = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')
cursor = conn.cursor()


print len(data_with_id)

for index, (i, data) in enumerate(data_with_id):
	response = alchemyapi.keywords('text', data, {'sentiment': 1})
	# if response['status'] == 'OK':
	# 	print('## Response Object ##')
 #    	print('## Keywords ##')
	for keyword in response['keywords']:
		sql = "INSERT INTO %s (pid, keyword, relevance) VALUES (\"%d\",\"%s\", \"%s\")" % ('clustering.nuclear_physics_full_table_new_kw',i, keyword['text'], keyword['relevance'])
		try:
			# 执行sql语句
			cursor.execute(sql)
			# 提交到数据库执行
			conn.commit()
			# return_list.insert(i, '%d row inerted' %i)
		except:
			# 发生错误时回滚
			conn.rollback()
			# return_list.insert(i, '%d row rollback' %i)
			print 'rollback %d' %index
	    	# print "-------------------------------------------------------------------"

		# 关闭数据库连接

	print 'commit %d' %index
conn.close()



