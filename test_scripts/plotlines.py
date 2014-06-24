import MySQLdb
import matplotlib.pyplot as plt


# def my_query(connection, q):
# 	cursor = connection.cursor()
# 	cursor.execute(q)
# 	return cursor.fetchall()

# conn = MySQLdb.connect(host='localhost', user='root', passwd='ct123690')

# NSF_sql = "select StartYear, count(StartYear), sum(TotalFunding), PSShortName_Group " \
# 	  "from clustering.2groups_20k_phydivision_results as g left join clustering.nuclear_physics_full_table_new as t " \
# 	  "on g.Ref_code = t.RefCode " \
# 	  "where label = 12" \
# 	  " AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009) " \
# 	  "AND (group_name = 'NSF') " \
# 	  "GROUP BY StartYear"


# FP_sql = "select StartYear, count(StartYear), sum(TotalFunding), PSShortName_Group " \
# 	  "from clustering.2groups_20k_phydivision_results as g left join clustering.nuclear_physics_full_table_new as t " \
# 	  "on g.Ref_code = t.RefCode " \
# 	  "where label = 12" \
# 	  " AND (StartYear = 2011 or StartYear = 2012 or StartYear = 2013 or StartYear = 2010 or StartYear = 2009) " \
# 	  "AND (group_name = 'FP') " \
# 	  "GROUP BY StartYear"


# NSF_doc_rows = my_query(conn, NSF_sql)

# FP_doc_rows = my_query(conn, FP_sql)


# print [[year, count] for i, (year, count, funding, group) in enumerate(NSF_doc_rows)]

NSF_year = [2009, 2010, 2011, 2012, 2013]
NSF_count = [9, 4, 3, 3, 3]

fig, ax = plt.subplots()
ax.plot(NSF_year, NSF_count, lw=2, label='silhouette_score vs number of k')
ax.set_xlabel('number of k')
ax.set_ylabel('silhouette_score')

ax.set_xlim(0, len(NSF_year))
ax.set_title('number of k curve')
plt.show()






