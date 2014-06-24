# This Python file uses the following encoding: utf-8

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from math import ceil, sqrt
# Some data
labels = 'FP','NSF'
explode=(0, 0.05)

clustering_results = [
    (1, 16), (35, 44), (1, 8), (3, 4), (9, 5), (8, 21), (29, 12), (28, 22), 
    (13, 16), (10, 28), (0, 21), (5, 50), (119, 29), (4, 9), (7, 16), (3, 40), 
    (8, 25), (2, 17), (4, 39), (9, 28)
]

dimension = int(ceil(sqrt(len(clustering_results))))
print dimension

conb = [(x, y) for x in xrange(0,dimension) for y in xrange(0,dimension)]
the_grid = GridSpec(dimension, dimension)


print clustering_results[0][0]
for i, (x, y) in enumerate(conb):
    if i < 20:
        print i
        fracs = [clustering_results[i][0], clustering_results[i][1]]
        plt.subplot(the_grid[x, y], aspect=1)
        patches, texts, autotexts = plt.pie(fracs, explode=explode,
                                        labels=labels, autopct='%.0f%%',
                                        shadow=False)
        numbers_projects = clustering_results[i][0]+clustering_results[i][1]
        title = "%s|%s" %(i, numbers_projects)
        # title = "c%s" %(i)
        # print title
        plt.title(title)
        autotexts[0].set_color('y')



plt.show()