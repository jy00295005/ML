ML

==

**silhouette_score_curve.py** 

采用不同k值计算数据的kmeans聚类轮廓系数，找出最优的k值

== 

**nuclear_physics_nsf_fp_fulltable.py** 

使用最优k值聚类，计算两个机构比例，入库
	
	print group_count #聚类结构两个资助机构比例
	
	## 将聚类结果写入数据库，需要时打开
	# insert_results_into_mysql(doc_label_list, insert_table_name)
	
