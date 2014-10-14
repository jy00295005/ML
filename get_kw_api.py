from pony.orm import *

db = Database('mysql', host='localhost', user='root', passwd='ct123690', db='clustering')

sql_debug(True) 
db.generate_mapping(create_tables=True) 
with db_session:
	print db.select("* from clustering.truth")[0]