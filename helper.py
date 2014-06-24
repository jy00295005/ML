# This Python file uses the following encoding: utf-8
import MySQLdb
import numpy as np

conn = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')


def my_query(q, connection=conn):
	cursor = connection.cursor()
	cursor.execute(q)
	return cursor.fetchall()

def parse_mysql_data(mysql_data, fields_index):
	document_data_ = []
	document_ref_code_ = []
	document_pbid_ = []
	document_group_ = []

	for i, row in enumerate(mysql_data):
		if row[19] == 'NULL':
			document_data_.insert(i, row[fields_index['title']].decode('latin-1'))
		else:
			document_data_.insert(i, (row[fields_index['title']] + ' || ' + row[fields_index['abstract']]).decode('latin-1'))
		document_ref_code_.insert(i, row[fields_index['ref_code']])
		document_pbid_.insert(i, row[fields_index['pbid']])
		document_group_.insert(i, row[fields_index['group']])
	return (document_data_,document_ref_code_,document_pbid_,document_group_)
	

def counts_between_groups(number_k, clustering_results):
	number_label_list = np.linspace(0, number_k-1, number_k).astype(int)
	group_count_ = []
	for x in number_label_list:
		x_cluster = [i for i, row in enumerate(clustering_results) if row[1] == x]
		count_x_cluster = len(x_cluster)
		FP=0
		for cluster_index in x_cluster:
			flag = clustering_results[cluster_index][4] == 'FP'
			if flag:
				FP = FP +1 

		group_count_.insert(i, (FP, (count_x_cluster - FP))) 
	return group_count_


def insert_results_into_mysql(data, tabel_name, connection=conn):
	return_list = []
	cursor = connection.cursor()
	for i, (text_data, label, Ref_code, PBID, document_group) in enumerate(data):
		sql = "INSERT INTO %s (text_data, \
			label, Ref_code, PBID, group_name) \
			VALUES (\"%s\",\"%d\", \"%s\", \"%s\", \"%s\" )" % \
			(tabel_name, text_data.replace('"', '').decode('latin-1'), label, Ref_code, PBID, document_group)
	     	# print(sql)

		try:
			# 执行sql语句
			cursor.execute(sql)
			# 提交到数据库执行
			connection.commit()
			return_list.insert(i, '%d row inerted' %i)
			print 'commit %d' %i

		except:
			# 发生错误时回滚
			connection.rollback()
			return_list.insert(i, '%d row rollback' %i)
			print 'rollback %d' %i

	    	# print(sql)
	    	# print "-------------------------------------------------------------------"

	# 关闭数据库连接
	connection.close()
	return return_list


def get_stop_words():
	stop_words = [
		'all', 'six', 'less', 'being', 'indeed', 'over', 'move', 'anyway', 'four', 'not', 'own', 'through', 'yourselves', 'fify', 'where', 'mill', 'only',
		'find', 'before', 'one', 'whose', 'system', 'how', 'somewhere', 'with', 'thick', 'show', 'had', 'enough', 'should', 'to', 'must', 'whom', 'seeming', 
		'under', 'ours', 'has', 'might', 'thereafter', 'latterly', 'do', 'them', 'his', 'around', 'than', 'get', 'very', 'de', 'none', 'cannot', 'every', 
		'whether', 'they', 'front', 'during', 'thus', 'now', 'him', 'nor', 'name', 'several', 'hereafter', 'always', 'who', 'cry', 'whither', 'this', 'someone', 
		'either', 'each', 'become', 'thereupon', 'sometime', 'side', 'two', 'therein', 'twelve', 'because', 'often', 'ten', 'our', 'eg', 'some', 'back', 'up', 
		'go', 'namely', 'towards', 'are', 'further', 'beyond', 'ourselves', 'yet', 'out', 'even', 'will', 'what', 'still', 'for', 'bottom', 'mine', 'since', 
		'please', 'forty', 'per', 'its', 'everything', 'behind', 'un', 'above', 'between', 'it', 'neither', 'seemed', 'ever', 'across', 'she', 'somehow', 'be', 
		'we', 'full', 'never', 'sixty', 'however', 'here', 'otherwise', 'were', 'whereupon', 'nowhere', 'although', 'found', 'alone', 're', 'along', 'fifteen', 
		'by', 'both', 'about', 'last', 'would', 'anything', 'via', 'many', 'could', 'thence', 'put', 'against', 'keep', 'etc', 'amount', 'became', 'ltd', 'hence', 
		'onto', 'or', 'con', 'among', 'already', 'co', 'afterwards', 'formerly', 'within', 'seems', 'into', 'others', 'while', 'whatever', 'except', 'down', 
		'hers', 'everyone', 'done', 'least', 'another', 'whoever', 'moreover', 'couldnt', 'throughout', 'anyhow', 'yourself', 'three', 'from', 'her', 'few', 
		'together', 'top', 'there', 'due', 'been', 'next', 'anyone', 'eleven', 'much', 'call', 'therefore', 'interest', 'then', 'thr', 'themselves', 'hundred', 
		'was', 'sincere', 'empty', 'more', 'himself', 'elsewhere', 'mostly', 'on', 'fire', 'am', 'becoming', 'hereby', 'amongst', 'else', 'part', 'everywhere', 
		'too', 'herself', 'former', 'those', 'he', 'me', 'myself', 'made', 'twenty', 'these', 'bill', 'cant', 'us', 'until', 'besides', 'nevertheless', 'below', 
		'anywhere', 'nine', 'can', 'of', 'your', 'toward', 'my', 'something', 'and', 'whereafter', 'whenever', 'give', 'almost', 'wherever', 'is', 'describe', 
		'beforehand', 'herein', 'an', 'as', 'itself', 'at', 'have', 'in', 'seem', 'whence', 'ie', 'any', 'fill', 'again', 'hasnt', 'inc', 'thereby', 'thin', 'no', 
		'perhaps', 'latter', 'meanwhile', 'when', 'detail', 'same', 'wherein', 'beside', 'also', 'that', 'other', 'take', 'which', 'becomes', 'yo', 'if', 
		'nobody', 'see', 'though', 'may', 'after', 'upon', 'most', 'hereupon', 'eight', 'but', 'serious', 'nothing', 'such', 'why', 'a', 'off', 'whereby', 
		'third', 'i', 'whole', 'noone', 'sometimes', 'well', 'amoungst', 'yours', 'their', 'rather', 'without', 'so', 'five', 'the', 'first', 'whereas', 'once'
		'LHC' , 'collider' ,'facility' ,'group'
		'able', 'absolute', 'absolutely', 'academic', 'academics', 'academy', 'achievement', 'achievements', 'actively', 'activities', 'activity',
		'actual', 'actually', 'addressed', 'addresses', 'adept', 'advice', 'advise', 'advised', 'adviser', 'advising', 'advisor', 'april',
		'began', 'begin', 'beginning', 'begins', 'begun', 'student', 'students', 'studied', 'studies', 'study', 'studying',
		'train', 'trained', 'trainees', 'training', 'trains','support', 'supports', 'collaborative' , 'career' , 'careers', 'anduniversity',
		'universitat', 'universite', 'universities', 'university', u'universit\xe9', 'young', 'younger', 'youngest', 'youth', 'youthful',
		'use', 'used', 'useful', 'usefulness', 'user', 'users', 'uses',  'using', 'usual', 'usually','word', 'words', 'work', 'workable', 'worked', 'workers',
		'000', '001', '007hf', '01', '02', '03', '048', '08', '10', '100', '1000','1015', 'summer','train','training'
		'1053399', '1064468', '11', '1134052', '1138729', '1138737', '1138766', '1140018', 
		'115', '1156065', '11second', '11th', '11w5114', '12', '120', '120oc', '1231393', '1236746', '1238877', '1245659', '125', '1250', '126', 
		'12th', '13', '130', '1336073', '1336269', '1336716', '1338130', '134', '136', '139', '13c', '13t', '14', '140', '144', '144ce', '145', 
		'15', '150', '1500', '1510s', '1513', '152', '1530s', '1545', '1555', '158', '16', '160', '1600', '16th', 
		'17', '1721', '174', '18', '180', '1800', '18o', '18th', '19', '1940', '1950', '1950s', '1963', '1967', '1970s', '1975', '1980s', '1984', 
		'1986', '1990', '1992', '1996', '1997', '1998', '19th', '1s', '1st', '1x1x20', '20', '200', '2000', 
		'2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '200a', '200ps', '2010', '2011', '2012', '2013', '2014', '2015', 
		'2016', '2017', '2020', '209', '20th', '21', '213', '21cm', '21st', '21th', '22', '22na', '22nd', '23', '230', '24', '240', '24th', '25', 
		'250', '2500', '25t', '26', '26al', '27', '28', '29', '29306', '2b', '2clo4', '2d', '2deg', '2df', '2khg', '2m', '2mass', '2p', '2s', 
		'2theta_13',  '30', '300', '3000', '31', '32', '33', '330', '34', '341', '35', '36', '360', '376', '38', '39', '395', '39ar', '3d', 
		'3rd', '3x10', '3x3', '40', '400', '40m', '43', '44', '45', '450', '46', '466', '47', '473', '48', 
		'49', '493', '499','4th', '50', '500', '5000', '500kg', '507', '50s', '51', '53', '54', 
		'55', '5659', '568', '57', '570', '57fe', '58', '59', '5b', '60', '600', '6000', '60000', '63', '64', '653', '660', '67', '68', '6th', 
		'70', '700', '72', '73', '75', '750', '76', '7623', '76ge', '78', '7be', '7th', '7x10', '80', '800', '807', '81', '810', '82', 
		'8217', '8220', '8221', '8226', '8232', '83', '8364', '85', '86', '8722', '886', '90', '900', '930', '948', '95', '957', '96', 
		'98', '99', 'a2', 'aaas', 'aas', 'ab', 'ab2o4'
	]
	return stop_words